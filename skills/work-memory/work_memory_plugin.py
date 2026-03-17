#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Work Memory OpenClaw 插件 - 轻薄包装器

这是 Work Memory 核心库的 OpenClaw 集成层。
所有业务逻辑都在 work-memory PyPI 包中。

使用方式：
    from work_memory_plugin import WorkMemoryPlugin
    plugin = WorkMemoryPlugin()
    plugin.create_project("项目名称")

核心库：
    from work_memory import WorkMemory
    wm = WorkMemory()
"""

import os
from typing import Dict, List, Optional

# 导入核心库（PyPI 包）
try:
    from work_memory import WorkMemory
except ImportError:
    print("⚠️ 请先安装 Work Memory 核心库:")
    print("   pip install work-memory")
    print("   或开发模式：cd ~/.openclaw/workspace/work-memory-project && pip install -e .")
    raise


class WorkMemoryPlugin:
    """
    Work Memory OpenClaw 插件 - 轻薄包装器
    
    这个类只是核心库的简单包装，提供 OpenClaw 友好的接口。
    所有业务逻辑都在 WorkMemory 核心类中。
    """
    
    def __init__(self, root_dir: str = None):
        """
        初始化插件
        
        Args:
            root_dir: 数据目录，默认 ~/.openclaw/workspace/memory/work-memory/
        """
        if root_dir is None:
            root_dir = os.path.expanduser("~/.openclaw/workspace/memory/work-memory")
        
        self.root_dir = root_dir
        self.wm = WorkMemory(root_dir=root_dir)
        print(f"✅ Work Memory 插件已加载：{self.root_dir}")
    
    # ============================================================
    # 项目管理（直接委托给核心库）
    # ============================================================
    
    def create_project(self, name: str, **kwargs) -> Dict:
        """创建项目"""
        import uuid
        project_id = f"proj_{uuid.uuid4().hex[:8]}"
        self.wm.create_project(project_id, {'name': name, **kwargs})
        return {'success': True, 'project_id': project_id, 'name': name}
    
    def list_projects(self, status: str = 'active') -> List[Dict]:
        """列出项目"""
        return self.wm.list_projects(status)
    
    def complete_project(self, project_id: str) -> Dict:
        """完成项目"""
        success = self.wm.update_project_status(project_id, 'completed')
        return {'success': success, 'project_id': project_id}
    
    # ============================================================
    # 任务管理（直接委托给核心库）
    # ============================================================
    
    def create_task(self, title: str, **kwargs) -> Dict:
        """创建任务"""
        import uuid
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        self.wm.create_task(task_id, {'title': title, **kwargs})
        return {'success': True, 'task_id': task_id, 'title': title}
    
    def complete_task(self, task_id: str) -> Dict:
        """完成任务"""
        self.wm.complete_task(task_id)
        return {'success': True, 'task_id': task_id}
    
    def get_pending_tasks(self, project_id: str = None) -> List[Dict]:
        """获取待办任务"""
        return self.wm.get_pending_tasks(project_id)
    
    # ============================================================
    # 工作日志（直接委托给核心库）
    # ============================================================
    
    def save_daily_log(self, date: str = None, **kwargs) -> Dict:
        """保存日报"""
        if date is None:
            from datetime import datetime
            date = datetime.now().strftime('%Y-%m-%d')
        self.wm.save_daily_log(date, kwargs)
        return {'success': True, 'date': date}
    
    # ============================================================
    # 技能管理（直接委托给核心库）
    # ============================================================
    
    def add_skill(self, skill_name: str, **kwargs) -> Dict:
        """添加技能"""
        self.wm.add_skill(skill_name, kwargs)
        return {'success': True, 'skill_name': skill_name}
    
    def get_skills(self, category: str = None) -> Dict:
        """获取技能列表"""
        skills = self.wm.get_skills(category)
        return {'count': len(skills), 'skills': skills}
    
    # ============================================================
    # 统计信息（直接委托给核心库）
    # ============================================================
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.wm.get_stats()
    
    # ============================================================
    # 备份（直接委托给核心库）
    # ============================================================
    
    def backup(self, backup_path: str = None) -> Dict:
        """备份"""
        path = self.wm.backup(backup_path)
        return {'success': True, 'backup_path': path}


# ============================================================
# 命令处理（OpenClaw 技能兼容）
# ============================================================

def handle_wm_command(command: str, args: List[str]) -> str:
    """
    处理 Work Memory 命令（OpenClaw 技能兼容）
    
    使用方式：
        handle_wm_command('project', ['create', '测试项目'])
        handle_wm_command('stats', [])
    """
    plugin = WorkMemoryPlugin()
    
    if command == 'project' and args and args[0] == 'create':
        name = args[1] if len(args) > 1 else '未命名项目'
        result = plugin.create_project(name)
        return f"✅ 已创建项目：{name}\n项目 ID: {result['project_id']}"
    
    elif command == 'task' and args and args[0] == 'add':
        title = ' '.join(args[1:]) if len(args) > 1 else '未命名任务'
        result = plugin.create_task(title)
        return f"✅ 已创建任务：{title}\n任务 ID: {result['task_id']}"
    
    elif command == 'stats':
        stats = plugin.get_stats()
        return (
            f"📊 Work Memory 统计\n"
            f"项目：{stats['projects']['active']} 进行中\n"
            f"任务：{stats['tasks']['pending']} 待办\n"
            f"技能：{stats['skills']['count']} 个"
        )
    
    elif command == 'log' and args and args[0] == 'daily':
        result = plugin.save_daily_log()
        return f"✅ 已保存日报：{result['date']}"
    
    else:
        return "❌ 未知命令。可用：/wm project create, /wm task add, /wm stats, /wm log daily"


# ============================================================
# 向后兼容（保留旧 API）
# ============================================================

# 如果旧代码使用 WorkMemoryPlugin，这个文件提供兼容
# 新代码应该直接使用：from work_memory import WorkMemory

__all__ = ['WorkMemoryPlugin', 'handle_wm_command']
