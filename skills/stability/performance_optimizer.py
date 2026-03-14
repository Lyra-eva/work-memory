#!/usr/bin/env python3
"""
性能优化器 - 系统性能管理和缓存清理
属于 Stability System 核心功能
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class PerformanceOptimizer:
    """性能优化器"""
    
    def __init__(self):
        """初始化性能优化器"""
        self.cache_dirs = [
            '/root/.cache/huggingface',
            '/root/.cache/lancedb',
            '/tmp',
        ]
        self.workspace = Path('/root/.openclaw/workspace')
    
    def check_system_resources(self) -> Dict:
        """检查系统资源"""
        resources = {
            'memory': self._check_memory(),
            'disk': self._check_disk(),
            'processes': self._check_processes(),
            'cache_size': self._check_cache_size(),
        }
        return resources
    
    def _check_memory(self) -> Dict:
        """检查内存使用"""
        try:
            result = subprocess.run(
                ['free', '-h'],
                capture_output=True,
                text=True
            )
            lines = result.stdout.split('\n')
            mem_line = lines[1].split()
            return {
                'total': mem_line[1],
                'used': mem_line[2],
                'available': mem_line[6],
                'usage_percent': self._parse_percent(mem_line[2], mem_line[1])
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _check_disk(self) -> Dict:
        """检查磁盘使用"""
        try:
            result = subprocess.run(
                ['df', '-h', '/root'],
                capture_output=True,
                text=True
            )
            lines = result.stdout.split('\n')
            disk_line = lines[1].split()
            return {
                'total': disk_line[1],
                'used': disk_line[2],
                'available': disk_line[3],
                'usage_percent': disk_line[4].replace('%', '')
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _check_processes(self) -> Dict:
        """检查 Python 进程"""
        try:
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True
            )
            processes = [
                line for line in result.stdout.split('\n')
                if 'python3' in line and 'grep' not in line
            ]
            return {
                'python_count': len(processes),
                'total_count': len(result.stdout.split('\n')) - 1
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _check_cache_size(self) -> Dict:
        """检查缓存大小"""
        cache_sizes = {}
        for cache_dir in self.cache_dirs:
            path = Path(cache_dir)
            if path.exists():
                size = sum(
                    f.stat().st_size for f in path.glob('**/*')
                    if f.is_file()
                )
                cache_sizes[cache_dir] = size
            else:
                cache_sizes[cache_dir] = 0
        return cache_sizes
    
    def cleanup_cache(self, clean_huggingface: bool = True,
                     clean_lancedb: bool = True,
                     clean_tmp: bool = True) -> Dict:
        """
        清理缓存
        
        Args:
            clean_huggingface: 是否清理 HuggingFace 缓存
            clean_lancedb: 是否清理 LanceDB 缓存
            clean_tmp: 是否清理临时文件
            
        Returns:
            清理结果
        """
        results = {
            'cleaned': [],
            'errors': [],
            'freed_space': 0
        }
        
        if clean_huggingface:
            result = self._clean_dir(
                '/root/.cache/huggingface',
                'HuggingFace 缓存'
            )
            results['cleaned'].append(result)
            results['freed_space'] += result.get('freed', 0)
        
        if clean_lancedb:
            result = self._clean_dir(
                '/root/.cache/lancedb',
                'LanceDB 缓存'
            )
            results['cleaned'].append(result)
            results['freed_space'] += result.get('freed', 0)
        
        if clean_tmp:
            result = self._clean_dir(
                '/tmp',
                '临时文件'
            )
            results['cleaned'].append(result)
            results['freed_space'] += result.get('freed', 0)
        
        return results
    
    def _clean_dir(self, dir_path: str, name: str) -> Dict:
        """清理目录"""
        try:
            path = Path(dir_path)
            if not path.exists():
                return {
                    'name': name,
                    'status': 'not_found',
                    'freed': 0
                }
            
            # 计算清理前大小
            before_size = sum(
                f.stat().st_size for f in path.glob('**/*')
                if f.is_file()
            )
            
            # 清理文件
            for item in path.glob('*'):
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            
            return {
                'name': name,
                'status': 'success',
                'freed': before_size,
                'freed_mb': round(before_size / 1024 / 1024, 2)
            }
        except Exception as e:
            return {
                'name': name,
                'status': 'error',
                'error': str(e),
                'freed': 0
            }
    
    def clear_system_cache(self) -> Dict:
        """清理系统缓存 (drop_caches)"""
        try:
            # 需要 root 权限
            subprocess.run(
                ['sync'],
                check=True
            )
            subprocess.run(
                ['sh', '-c', 'echo 3 > /proc/sys/vm/drop_caches'],
                check=True
            )
            return {
                'status': 'success',
                'message': '系统缓存已清理'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def optimize(self, auto: bool = True) -> Dict:
        """
        执行性能优化
        
        Args:
            auto: 是否自动模式（只清理过期缓存）
            
        Returns:
            优化结果
        """
        print("🧹 开始性能优化...")
        
        # 检查资源
        resources = self.check_system_resources()
        
        # 清理缓存
        cleanup_result = self.cleanup_cache(
            clean_huggingface=not auto,
            clean_lancedb=True,
            clean_tmp=True
        )
        
        # 清理系统缓存
        system_cache_result = self.clear_system_cache()
        
        # 生成报告
        report = {
            'timestamp': datetime.now().isoformat(),
            'resources_before': resources,
            'cleanup_result': cleanup_result,
            'system_cache_result': system_cache_result,
            'total_freed_mb': round(
                cleanup_result['freed_space'] / 1024 / 1024, 2
            )
        }
        
        print(f"✅ 优化完成！释放空间：{report['total_freed_mb']} MB")
        
        return report
    
    def get_optimization_schedule(self) -> List[Dict]:
        """获取优化计划"""
        return [
            {
                'name': '每日清理',
                'frequency': 'daily',
                'tasks': ['clean_tmp', 'clean_lancedb']
            },
            {
                'name': '每周清理',
                'frequency': 'weekly',
                'tasks': ['clean_huggingface', 'clean_tmp', 'clean_lancedb']
            },
            {
                'name': '每月优化',
                'frequency': 'monthly',
                'tasks': ['full_cleanup', 'system_cache', 'optimize_db']
            }
        ]


# 全局实例
_optimizer = None


def get_optimizer() -> PerformanceOptimizer:
    """获取性能优化器实例"""
    global _optimizer
    if _optimizer is None:
        _optimizer = PerformanceOptimizer()
    return _optimizer


def optimize_performance(auto: bool = True) -> Dict:
    """快速执行性能优化"""
    optimizer = get_optimizer()
    return optimizer.optimize(auto)


if __name__ == '__main__':
    print("=" * 60)
    print("🧹 Performance Optimizer 测试")
    print("=" * 60)
    
    optimizer = get_optimizer()
    
    # 检查资源
    print("\n📊 系统资源:")
    resources = optimizer.check_system_resources()
    print(f"   内存：{resources['memory']}")
    print(f"   磁盘：{resources['disk']}")
    print(f"   进程：{resources['processes']}")
    
    # 执行优化
    print("\n🧹 执行优化:")
    result = optimizer.optimize(auto=True)
    print(f"   释放空间：{result['total_freed_mb']} MB")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成!")
    print("=" * 60)
