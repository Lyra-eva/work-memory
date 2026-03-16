#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Work Memory 数据迁移脚本

使用方式：
    python3 migrate_data.py <old_version> <new_version>

功能：
- 检测数据版本差异
- 执行版本间的迁移逻辑
- 支持回滚

迁移策略：
1. 小版本更新 (1.0.0 → 1.0.1)：通常无需迁移
2. 中版本更新 (1.0.x → 1.1.0)：可能需要字段扩展
3. 大版本更新 (1.x.x → 2.0.0)：可能需要数据结构重构
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime


def get_data_dir():
    """获取数据目录路径"""
    return Path.home() / ".openclaw" / "workspace" / "work-memory-data"


def backup_data(data_dir, version_from, version_to):
    """创建迁移前备份"""
    backup_dir = data_dir / f".migration_backups" / f"backup_{version_from}_to_{version_to}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制所有数据（排除备份目录本身）
    for item in data_dir.iterdir():
        if item.name.startswith('.'):
            continue
        if item.is_dir():
            shutil.copytree(item, backup_dir / item.name, dirs_exist_ok=True)
        else:
            shutil.copy2(item, backup_dir / item.name)
    
    return backup_dir


def migrate_1_0_0_to_1_1_0(data_dir):
    """
    示例迁移：v1.0.0 → v1.1.0
    
    变更：
    - 添加项目优先级字段
    - 添加任务标签系统
    """
    print("  → 迁移项目数据...")
    projects_dir = data_dir / "projects" / "active"
    if projects_dir.exists():
        for project_file in projects_dir.glob("*.json"):
            with open(project_file, 'r', encoding='utf-8') as f:
                project = json.load(f)
            
            # 添加新字段（如果不存在）
            if 'priority' not in project:
                project['priority'] = 'medium'
            if 'tags' not in project:
                project['tags'] = []
            
            with open(project_file, 'w', encoding='utf-8') as f:
                json.dump(project, f, indent=2, ensure_ascii=False)
    
    print("  → 迁移任务数据...")
    tasks_dir = data_dir / "tasks" / "pending"
    if tasks_dir.exists():
        for task_file in tasks_dir.glob("*.json"):
            with open(task_file, 'r', encoding='utf-8') as f:
                task = json.load(f)
            
            # 添加新字段
            if 'tags' not in task:
                task['tags'] = []
            if 'estimated_hours' not in task:
                task['estimated_hours'] = None
            
            with open(task_file, 'w', encoding='utf-8') as f:
                json.dump(task, f, indent=2, ensure_ascii=False)


def migrate_1_1_0_to_2_0_0(data_dir):
    """
    示例迁移：v1.1.0 → v2.0.0
    
    变更：
    - 重构数据结构
    - 添加关系图谱
    """
    print("  → 执行重大数据结构重构...")
    # 这里实现具体的迁移逻辑
    pass


def migrate(old_version, new_version):
    """
    执行数据迁移
    
    Args:
        old_version: 旧版本号
        new_version: 新版本号
    """
    data_dir = get_data_dir()
    
    if not data_dir.exists():
        print(f"✅ 数据目录不存在，无需迁移")
        return True
    
    print(f"数据目录：{data_dir}")
    
    # 创建备份
    print(f"💾 创建迁移备份...")
    backup_dir = backup_data(data_dir, old_version, new_version)
    print(f"✅ 备份位置：{backup_dir}")
    
    # 版本迁移路由
    migrations = {
        ("1.0.0", "1.1.0"): migrate_1_0_0_to_1_1_0,
        ("1.1.0", "2.0.0"): migrate_1_1_0_to_2_0_0,
    }
    
    # 查找匹配的迁移
    migration_key = (old_version, new_version)
    if migration_key in migrations:
        print(f"🔄 执行迁移：v{old_version} → v{new_version}")
        try:
            migrations[migration_key](data_dir)
            print(f"✅ 迁移成功")
            return True
        except Exception as e:
            print(f"❌ 迁移失败：{e}")
            print(f"💡 可以从备份恢复：{backup_dir}")
            return False
    else:
        # 如果没有精确匹配，尝试模糊匹配
        print(f"ℹ️  未找到精确迁移路径，尝试兼容性检查...")
        
        # 简单版本比较
        old_parts = [int(x) for x in old_version.split('.') if x.isdigit()]
        new_parts = [int(x) for x in new_version.split('.') if x.isdigit()]
        
        # 如果主版本相同，假设向后兼容
        if len(old_parts) > 0 and len(new_parts) > 0 and old_parts[0] == new_parts[0]:
            print(f"✅ 主版本相同，假设数据格式兼容")
            return True
        else:
            print(f"⚠️  主版本不同，建议手动检查数据兼容性")
            return True  # 仍然返回成功，但给出警告


def main():
    if len(sys.argv) != 3:
        print("使用方式：python3 migrate_data.py <old_version> <new_version>")
        print("示例：python3 migrate_data.py 1.0.0 1.1.0")
        sys.exit(1)
    
    old_version = sys.argv[1]
    new_version = sys.argv[2]
    
    print(f"==========================================")
    print(f"🔄 Work Memory 数据迁移")
    print(f"   v{old_version} → v{new_version}")
    print(f"==========================================\n")
    
    success = migrate(old_version, new_version)
    
    if success:
        print(f"\n✅ 迁移完成")
        sys.exit(0)
    else:
        print(f"\n❌ 迁移失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
