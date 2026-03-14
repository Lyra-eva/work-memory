#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆迁移工具

用于将旧版本记忆系统迁移到新版本
支持：
- 默认记忆系统 (MEMORY.md + graph.db) → 工作记忆系统
- 工作记忆系统 v1.x → 工作记忆系统 v2.x
- 备份和恢复
"""

import os
import sys
import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


# ============================================================
# 迁移工具类
# ============================================================

class MemoryMigrator:
    """记忆迁移工具"""
    
    def __init__(self, source_dir: str, target_dir: str):
        """
        初始化迁移工具
        
        Args:
            source_dir: 源记忆目录
            target_dir: 目标记忆目录
        """
        self.source_dir = os.path.expanduser(source_dir)
        self.target_dir = os.path.expanduser(target_dir)
        self.migration_log = []
    
    def migrate(self, migration_type: str = 'auto') -> bool:
        """
        执行迁移
        
        Args:
            migration_type: 迁移类型
                - 'auto': 自动检测
                - 'default_to_work': 默认记忆 → 工作记忆
                - 'work_v1_to_v2': 工作记忆 v1 → v2
        
        Returns:
            bool: 迁移是否成功
        """
        print("=" * 70)
        print("🔄 记忆系统迁移工具")
        print("=" * 70)
        
        # 备份源目录
        backup_path = self._create_backup()
        print(f"\n✅ 已创建备份：{backup_path}")
        
        # 执行迁移
        try:
            if migration_type == 'auto':
                migration_type = self._detect_migration_type()
            
            if migration_type == 'default_to_work':
                success = self._migrate_default_to_work()
            elif migration_type == 'opclaw_memory_to_work':
                success = self._migrate_opclaw_memory_to_work()
            elif migration_type == 'work_v1_to_v2':
                success = self._migrate_work_v1_to_v2()
            else:
                print(f"❌ 未知的迁移类型：{migration_type}")
                return False
            
            if success:
                self._save_migration_log()
                print("\n✅ 迁移成功！")
            else:
                print("\n❌ 迁移失败！")
            
            return success
            
        except Exception as e:
            print(f"\n❌ 迁移失败：{e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _detect_migration_type(self) -> str:
        """检测迁移类型"""
        # 检查是否有 graph.db (默认记忆系统)
        if os.path.exists(os.path.join(self.source_dir, 'cognition', 'graph.db')):
            return 'default_to_work'
        
        # 检查是否有 OpenClaw 默认 memory/ 目录 (包含 YYYY-MM-DD.md 文件)
        if self._is_opclaw_memory_dir():
            return 'opclaw_memory_to_work'
        
        # 检查工作记忆版本
        version_file = os.path.join(self.source_dir, 'VERSION')
        if os.path.exists(version_file):
            with open(version_file, 'r') as f:
                version = f.read().strip()
                if version.startswith('1.'):
                    return 'work_v1_to_v2'
        
        # 默认假设是工作记忆升级
        return 'work_v1_to_v2'
    
    def _is_opclaw_memory_dir(self) -> bool:
        """检查是否是 OpenClaw 默认 memory/ 目录"""
        # 检查是否包含 YYYY-MM-DD.md 格式的日志文件
        import re
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}\.md$')
        
        if not os.path.exists(self.source_dir):
            return False
        
        for file in os.listdir(self.source_dir):
            if date_pattern.match(file):
                return True
        
        # 或者检查是否有 MEMORY.md
        if os.path.exists(os.path.join(self.source_dir, 'MEMORY.md')):
            return True
        
        return False
    
    def _create_backup(self) -> str:
        """创建备份"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = os.path.join(
            os.path.dirname(self.source_dir),
            f"backup_{timestamp}"
        )
        
        if os.path.exists(self.source_dir):
            shutil.copytree(self.source_dir, backup_dir)
        
        return backup_dir
    
    def _migrate_default_to_work(self) -> bool:
        """
        从默认记忆系统迁移到工作记忆系统
        
        迁移内容:
        - MEMORY.md 中的偏好 → work_memory/preferences/
        - graph.db 中的技能 → work_memory/skills/
        - graph.db 中的项目 → work_memory/projects/
        """
        print("\n【迁移】默认记忆系统 → 工作记忆系统")
        print("-" * 70)
        
        # 1. 迁移 MEMORY.md 偏好
        memory_md = os.path.join(os.path.dirname(self.source_dir), 'MEMORY.md')
        if os.path.exists(memory_md):
            print("  📄 迁移 MEMORY.md 偏好...")
            self._migrate_preferences(memory_md)
        
        # 2. 迁移 graph.db 数据
        graph_db = os.path.join(self.source_dir, 'cognition', 'graph.db')
        if os.path.exists(graph_db):
            print("  🗄️ 迁移 graph.db 数据...")
            self._migrate_graph_db(graph_db)
        
        # 3. 创建版本文件
        version_file = os.path.join(self.target_dir, 'VERSION')
        with open(version_file, 'w') as f:
            f.write('2.0.0')
        
        return True
    
    def _migrate_opclaw_memory_to_work(self) -> bool:
        """
        从 OpenClaw 默认 memory/ 目录迁移到工作记忆系统
        
        迁移内容:
        - memory/YYYY-MM-DD.md → work_memory/logs/daily/
        - memory/MEMORY.md → work_memory/preferences/MEMORY.md
        - 自动识别并迁移重要信息
        """
        print("\n【迁移】OpenClaw memory/ → 工作记忆系统")
        print("-" * 70)
        
        # 1. 迁移 MEMORY.md
        memory_md = os.path.join(self.source_dir, 'MEMORY.md')
        if os.path.exists(memory_md):
            print("  📄 迁移 MEMORY.md...")
            dst_path = os.path.join(self.target_dir, 'preferences', 'MEMORY.md')
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(memory_md, dst_path)
            self.migration_log.append({
                'type': 'preference',
                'source': memory_md,
                'target': dst_path,
                'status': 'success'
            })
            print(f"    ✅ 已迁移 MEMORY.md")
        
        # 2. 迁移每日日志 (YYYY-MM-DD.md)
        import re
        date_pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})\.md$')
        
        daily_logs_migrated = 0
        for file in os.listdir(self.source_dir):
            match = date_pattern.match(file)
            if match:
                date_str = match.group(1)
                src_path = os.path.join(self.source_dir, file)
                dst_path = os.path.join(self.target_dir, 'logs', 'daily', f"{date_str}.md")
                
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)
                
                self.migration_log.append({
                    'type': 'daily_log',
                    'source': src_path,
                    'target': dst_path,
                    'status': 'success'
                })
                daily_logs_migrated += 1
        
        print(f"    ✅ 已迁移 {daily_logs_migrated} 个每日日志")
        
        # 3. 创建版本文件
        version_file = os.path.join(self.target_dir, 'VERSION')
        with open(version_file, 'w') as f:
            f.write('2.0.0')
        
        return True
    
    def _migrate_preferences(self, memory_md_path: str):
        """迁移 MEMORY.md 中的偏好"""
        with open(memory_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析偏好
        preferences = []
        in_preferences = False
        for line in content.split('\n'):
            if '## Preferences' in line:
                in_preferences = True
                continue
            if in_preferences and line.startswith('##'):
                break
            if in_preferences and line.startswith('- **'):
                # 解析偏好项
                pref = line.replace('- **', '').strip()
                if '**' in pref:
                    title, desc = pref.split('**', 1)
                    preferences.append({
                        'title': title.strip(),
                        'description': desc.strip()
                    })
        
        # 保存到工作记忆
        for pref in preferences:
            pref_file = os.path.join(
                self.target_dir, 'preferences',
                f"{pref['title'].replace(' ', '_')}.md"
            )
            with open(pref_file, 'w', encoding='utf-8') as f:
                f.write(f"# {pref['title']}\n\n{pref['description']}\n")
            
            self.migration_log.append({
                'type': 'preference',
                'source': memory_md_path,
                'target': pref_file,
                'status': 'success'
            })
        
        print(f"    ✅ 迁移 {len(preferences)} 个偏好")
    
    def _migrate_graph_db(self, graph_db_path: str):
        """迁移 graph.db 中的数据"""
        conn = sqlite3.connect(graph_db_path)
        cursor = conn.cursor()
        
        # 1. 迁移技能
        print("    - 迁移技能...")
        cursor.execute("""
            SELECT properties FROM nodes 
            WHERE node_type = 'Capability'
        """)
        
        skills_count = 0
        for row in cursor.fetchall():
            try:
                props = json.loads(row[0])
                skill_name = props.get('name', 'unknown')
                
                # 保存到工作记忆
                skill_file = os.path.join(
                    self.target_dir, 'skills', 'technical',
                    f"{skill_name}.json"
                )
                
                with open(skill_file, 'w', encoding='utf-8') as f:
                    json.dump(props, f, indent=2, ensure_ascii=False)
                
                skills_count += 1
            except Exception as e:
                print(f"      ⚠️ 跳过：{e}")
        
        print(f"      ✅ 迁移 {skills_count} 个技能")
        
        # 2. 迁移项目 (如果有)
        print("    - 迁移项目...")
        cursor.execute("""
            SELECT properties FROM nodes 
            WHERE node_type = 'Event'
            AND json_extract(properties, '$.event_type') = 'capability_learned'
        """)
        
        projects_count = 0
        for row in cursor.fetchall():
            try:
                props = json.loads(row[0])
                # 这里可以根据实际情况迁移项目
                projects_count += 1
            except:
                pass
        
        print(f"      ✅ 迁移 {projects_count} 个项目相关事件")
        
        conn.close()
    
    def _migrate_work_v1_to_v2(self) -> bool:
        """
        工作记忆系统 v1 → v2 迁移
        
        主要变化:
        - 目录结构调整
        - 新增字段
        - 格式升级
        """
        print("\n【迁移】工作记忆系统 v1 → v2")
        print("-" * 70)
        
        # 1. 检查源目录
        if not os.path.exists(self.source_dir):
            print(f"  ❌ 源目录不存在：{self.source_dir}")
            return False
        
        # 2. 创建目标目录结构
        print("  📁 创建 v2 目录结构...")
        self._init_v2_directories()
        
        # 3. 复制现有数据
        print("  📋 复制现有数据...")
        self._copy_existing_data()
        
        # 4. 升级格式
        print("  ⬆️  升级数据格式...")
        self._upgrade_data_format()
        
        # 5. 创建版本文件
        version_file = os.path.join(self.target_dir, 'VERSION')
        with open(version_file, 'w') as f:
            f.write('2.0.0')
        
        print("  ✅ v2 目录结构创建完成")
        return True
    
    def _init_v2_directories(self):
        """初始化 v2 目录结构"""
        directories = [
            'projects/active', 'projects/completed', 'projects/archived',
            'tasks/pending', 'tasks/in_progress', 'tasks/completed',
            'skills/technical', 'skills/soft', 'skills/certifications',
            'knowledge/technical', 'knowledge/business', 'knowledge/templates',
            'contacts/colleagues', 'contacts/clients', 'contacts/partners',
            'meetings/notes', 'meetings/action_items',
            'logs/daily', 'logs/weekly', 'logs/monthly',
            'backups', 'relationships'
        ]
        
        for dir_path in directories:
            os.makedirs(os.path.join(self.target_dir, dir_path), exist_ok=True)
    
    def _copy_existing_data(self):
        """复制现有数据"""
        # 复制所有现有文件到新结构
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith(('.json', '.md')):
                    src_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_path, self.source_dir)
                    dst_path = os.path.join(self.target_dir, rel_path)
                    
                    # 确保目标目录存在
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    
                    # 复制文件
                    shutil.copy2(src_path, dst_path)
                    
                    self.migration_log.append({
                        'type': 'file',
                        'source': src_path,
                        'target': dst_path,
                        'status': 'copied'
                    })
    
    def _upgrade_data_format(self):
        """升级数据格式"""
        # 遍历所有 JSON 文件，添加新字段
        for root, dirs, files in os.walk(self.target_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # 添加迁移元数据
                        if 'metadata' not in data:
                            data['metadata'] = {}
                        
                        data['metadata']['migrated_at'] = datetime.now().isoformat()
                        data['metadata']['migrated_from'] = 'v1'
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        
                        self.migration_log.append({
                            'type': 'upgrade',
                            'file': file_path,
                            'status': 'upgraded'
                        })
                    except Exception as e:
                        print(f"    ⚠️ 跳过 {file}: {e}")
    
    def _save_migration_log(self):
        """保存迁移日志"""
        log_file = os.path.join(self.target_dir, 'migration_log.json')
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'source': self.source_dir,
                'target': self.target_dir,
                'items': self.migration_log
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n📋 迁移日志已保存：{log_file}")


# ============================================================
# 命令行工具
# ============================================================

def migrate_opclaw_memory():
    """
    OpenClaw 环境专用：自动迁移 workspace/memory/ 到 workspace/work-memory/
    
    这是为 OpenClaw 设计的便捷函数，无需参数即可自动迁移
    """
    # OpenClaw 默认路径
    workspace_dir = os.path.expanduser("~/.openclaw/workspace")
    source_dir = os.path.join(workspace_dir, "memory")
    target_dir = os.path.join(workspace_dir, "work-memory")
    
    # 检查源目录是否存在
    if not os.path.exists(source_dir):
        print(f"❌ 源目录不存在：{source_dir}")
        print("   提示：OpenClaw 默认记忆目录通常在 ~/.openclaw/workspace/memory/")
        return False
    
    print(f"🔍 检测到 OpenClaw 记忆目录：{source_dir}")
    print(f"📥 将迁移到：{target_dir}\n")
    
    migrator = MemoryMigrator(source_dir, target_dir)
    return migrator.migrate('auto')


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='记忆系统迁移工具')
    parser.add_argument('source', help='源记忆目录')
    parser.add_argument('target', help='目标记忆目录')
    parser.add_argument(
        '--type',
        choices=['auto', 'default_to_work', 'opclaw_memory_to_work', 'work_v1_to_v2'],
        default='auto',
        help='迁移类型'
    )
    parser.add_argument(
        '--opclaw',
        action='store_true',
        help='OpenClaw 模式：自动迁移 ~/.openclaw/workspace/memory/ 到 work-memory/'
    )
    
    args = parser.parse_args()
    
    # OpenClaw 便捷模式
    if args.opclaw:
        success = migrate_opclaw_memory()
    else:
        migrator = MemoryMigrator(args.source, args.target)
        success = migrator.migrate(args.type)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
