#!/usr/bin/env python3
"""
Lily 记忆系统 - 健康检查模块

提供系统健康状态检查，包括：
- 数据库连接
- 数据库大小
- 数据统计
- 备份状态
- 系统资源
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))
from memory.database import get_database
from memory.logger import logger, log_operation


class HealthChecker:
    """健康检查器"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = '/home/admin/.openclaw/workspace/lily/data/lily.db'
        self.db_path = db_path
        self.backup_dir = '/home/admin/.openclaw/workspace/lily/backups'
    
    def check_all(self) -> Dict[str, Any]:
        """执行所有健康检查"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'checks': {}
        }
        
        # 1. 数据库连接检查
        db_check = self.check_database()
        results['checks']['database'] = db_check
        if db_check['status'] != 'healthy':
            results['status'] = 'unhealthy'
        
        # 2. 数据统计检查
        stats_check = self.check_statistics()
        results['checks']['statistics'] = stats_check
        
        # 3. 备份状态检查
        backup_check = self.check_backups()
        results['checks']['backups'] = backup_check
        
        # 4. 文件系统检查
        fs_check = self.check_filesystem()
        results['checks']['filesystem'] = fs_check
        
        # 5. 系统资源检查
        resource_check = self.check_resources()
        results['checks']['resources'] = resource_check
        
        # 记录日志
        log_operation('health_check', {
            'status': results['status'],
            'checks_passed': sum(1 for c in results['checks'].values() if c['status'] == 'healthy'),
            'total_checks': len(results['checks'])
        })
        
        return results
    
    def check_database(self) -> Dict[str, Any]:
        """检查数据库状态"""
        result = {
            'status': 'healthy',
            'message': 'Database connection successful',
            'details': {}
        }
        
        try:
            db = get_database(self.db_path)
            stats = db.get_stats()
            db.close()
            
            result['details'] = {
                'path': self.db_path,
                'size_bytes': stats['database_size_bytes'],
                'size_kb': round(stats['database_size_bytes'] / 1024, 2),
                'episode_count': stats['episodic_memory'],
                'semantic_count': stats['semantic_memory'],
                'capability_count': stats['capabilities'],
                'working_memory_count': stats['working_memory']
            }
            
            # 检查数据库文件是否存在
            if not Path(self.db_path).exists():
                result['status'] = 'unhealthy'
                result['message'] = 'Database file not found'
            
            # 检查数据库大小 (超过 100MB 告警)
            if stats['database_size_bytes'] > 100 * 1024 * 1024:
                result['status'] = 'warning'
                result['message'] = 'Database size exceeds 100MB'
            
        except Exception as e:
            result['status'] = 'unhealthy'
            result['message'] = f'Database connection failed: {str(e)}'
        
        return result
    
    def check_statistics(self) -> Dict[str, Any]:
        """检查数据统计"""
        result = {
            'status': 'healthy',
            'message': 'Statistics check passed',
            'details': {}
        }
        
        try:
            db = get_database(self.db_path)
            
            # 检查最近的事件
            recent_episodes = db.query_episodes(limit=1)
            if recent_episodes:
                result['details']['last_episode'] = recent_episodes[0].get('created_at', 'unknown')
            
            # 检查工作记忆
            working_memories = db.query_semantic(limit=1)
            result['details']['has_semantic_memory'] = len(working_memories) > 0
            
            db.close()
            
        except Exception as e:
            result['status'] = 'warning'
            result['message'] = f'Statistics check failed: {str(e)}'
        
        return result
    
    def check_backups(self) -> Dict[str, Any]:
        """检查备份状态"""
        result = {
            'status': 'healthy',
            'message': 'Backup check passed',
            'details': {}
        }
        
        try:
            backup_path = Path(self.backup_dir)
            
            if not backup_path.exists():
                backup_path.mkdir(parents=True, exist_ok=True)
                result['details']['backup_dir_created'] = True
            
            # 查找最近的备份
            backup_files = list(backup_path.glob('*.db'))
            if backup_files:
                latest_backup = max(backup_files, key=lambda f: f.stat().st_mtime)
                result['details']['latest_backup'] = {
                    'file': latest_backup.name,
                    'size_bytes': latest_backup.stat().st_size,
                    'created_at': datetime.fromtimestamp(latest_backup.stat().st_mtime).isoformat()
                }
            else:
                result['status'] = 'warning'
                result['message'] = 'No backup files found'
                result['details']['backup_count'] = 0
            
        except Exception as e:
            result['status'] = 'warning'
            result['message'] = f'Backup check failed: {str(e)}'
        
        return result
    
    def check_filesystem(self) -> Dict[str, Any]:
        """检查文件系统"""
        result = {
            'status': 'healthy',
            'message': 'Filesystem check passed',
            'details': {}
        }
        
        try:
            # 检查关键目录
            required_dirs = [
                '/home/admin/.openclaw/workspace/lily/data',
                '/home/admin/.openclaw/workspace/lily/config',
                '/home/admin/.openclaw/workspace/lily/core',
                '/home/admin/.openclaw/workspace/lily/logs',
                '/home/admin/.openclaw/workspace/lily/backups'
            ]
            
            missing_dirs = []
            for dir_path in required_dirs:
                if not Path(dir_path).exists():
                    missing_dirs.append(dir_path)
            
            if missing_dirs:
                result['status'] = 'warning'
                result['message'] = f'Missing directories: {", ".join(missing_dirs)}'
            
            result['details']['required_dirs'] = len(required_dirs)
            result['details']['missing_dirs'] = len(missing_dirs)
            
        except Exception as e:
            result['status'] = 'warning'
            result['message'] = f'Filesystem check failed: {str(e)}'
        
        return result
    
    def check_resources(self) -> Dict[str, Any]:
        """检查系统资源"""
        result = {
            'status': 'healthy',
            'message': 'Resource check passed',
            'details': {}
        }
        
        try:
            # 磁盘空间
            stat = os.statvfs('/home')
            free_gb = (stat.f_bavail * stat.f_frsize) / (1024 ** 3)
            result['details']['disk_free_gb'] = round(free_gb, 2)
            
            if free_gb < 1:
                result['status'] = 'warning'
                result['message'] = 'Low disk space (<1GB)'
            
            # 内存使用 (简单检查)
            try:
                with open('/proc/meminfo', 'r') as f:
                    meminfo = f.readlines()
                
                for line in meminfo:
                    if line.startswith('MemAvailable:'):
                        available_kb = int(line.split()[1])
                        available_mb = available_kb / 1024
                        result['details']['memory_available_mb'] = round(available_mb, 2)
                        
                        if available_mb < 100:
                            result['status'] = 'warning'
                            result['message'] = 'Low memory (<100MB)'
                        break
            except:
                result['details']['memory_available_mb'] = 'unknown'
            
        except Exception as e:
            result['status'] = 'warning'
            result['message'] = f'Resource check failed: {str(e)}'
        
        return result
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """生成健康报告"""
        lines = [
            "=" * 60,
            "🏥 Lily 记忆系统健康检查报告",
            "=" * 60,
            f"检查时间：{results['timestamp']}",
            f"总体状态：{self._status_emoji(results['status'])} {results['status'].upper()}",
            "",
            "检查项详情:"
        ]
        
        for check_name, check_result in results['checks'].items():
            emoji = self._status_emoji(check_result['status'])
            lines.append(f"  {emoji} {check_name}: {check_result['status']}")
            
            if 'details' in check_result:
                for key, value in check_result['details'].items():
                    if isinstance(value, dict):
                        lines.append(f"      - {key}:")
                        for k, v in value.items():
                            lines.append(f"          - {k}: {v}")
                    else:
                        lines.append(f"      - {key}: {value}")
        
        lines.append("=" * 60)
        return "\n".join(lines)
    
    def _status_emoji(self, status: str) -> str:
        """状态转 emoji"""
        emojis = {
            'healthy': '✅',
            'warning': '⚠️',
            'unhealthy': '❌'
        }
        return emojis.get(status, '❓')


def health_check() -> Dict[str, Any]:
    """便捷函数：执行健康检查"""
    checker = HealthChecker()
    return checker.check_all()


if __name__ == '__main__':
    print("🏥 执行健康检查...\n")
    
    checker = HealthChecker()
    results = checker.check_all()
    
    # 打印报告
    report = checker.generate_report(results)
    print(report)
    
    # 保存 JSON 报告
    report_path = '/home/admin/.openclaw/workspace/lily/logs/health-report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 详细报告已保存：{report_path}")
    
    # 退出码 (用于 cron/监控)
    if results['status'] == 'healthy':
        sys.exit(0)
    else:
        sys.exit(1)
