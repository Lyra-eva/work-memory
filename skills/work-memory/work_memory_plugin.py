#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Work Memory OpenClaw 插件层

提供与 OpenClaw 的集成接口，通过技能/插件方式调用工作记忆系统
不影响 OpenClaw 核心代码，框架升级不受影响
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

# 导入工作记忆核心库
try:
    from work_memory import WorkMemory
except ImportError:
    print("⚠️ 请先安装 work_memory: pip install -e ~/.openclaw/workspace/work-memory-project")
    raise


class WorkMemoryPlugin:
    """
    Work Memory OpenClaw 插件
    
    使用方式：
    1. 在技能中导入：from work_memory_plugin import WorkMemoryPlugin
    2. 初始化插件：plugin = WorkMemoryPlugin()
    3. 调用方法：plugin.create_project(...)
    """
    
    def __init__(self, data_dir: str = None):
        """
        初始化插件
        
        Args:
            data_dir: 数据目录，默认 ~/.openclaw/workspace/work-memory-data/
        """
        if data_dir is None:
            # 从 TOOLS.md 读取配置，或使用默认值
            data_dir = self._read_config_from_tools_md()
            if data_dir is None:
                data_dir = os.path.expanduser("~/.openclaw/workspace/work-memory-data")
        
        self.data_dir = data_dir
        self.wm = WorkMemory(root_dir=data_dir)
        print(f"✅ Work Memory 插件已初始化：{self.data_dir}")
    
    def _read_config_from_tools_md(self) -> Optional[str]:
        """从 TOOLS.md 读取配置"""
        tools_md_path = os.path.expanduser("~/.openclaw/workspace/TOOLS.md")
        
        if not os.path.exists(tools_md_path):
            return None
        
        with open(tools_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找 Work Memory 配置段落
        in_work_memory_section = False
        data_dir = None
        
        for line in content.split('\n'):
            if '### Work Memory' in line or '### work-memory' in line:
                in_work_memory_section = True
                continue
            
            if in_work_memory_section:
                if line.startswith('###'):  # 新的段落
                    break
                
                if '数据目录' in line or 'data_dir' in line:
                    # 解析路径
                    if ':' in line:
                        path = line.split(':', 1)[1].strip().strip('`"\'')
                        data_dir = os.path.expanduser(path)
                        break
        
        return data_dir
    
    # ============================================================
    # 项目管理
    # ============================================================
    
    def create_project(self, name: str, description: str = '', 
                      priority: str = 'medium', **kwargs) -> Dict:
        """
        创建项目
        
        Args:
            name: 项目名称
            description: 项目描述
            priority: 优先级 (high/medium/low)
            **kwargs: 其他项目属性
        
        Returns:
            Dict: 项目信息
        
        示例：
        >>> plugin.create_project("A 股智能体", "量化交易系统", priority="high")
        """
        import uuid
        project_id = f"proj_{uuid.uuid4().hex[:8]}"
        
        project_data = {
            'name': name,
            'description': description,
            'priority': priority,
            **kwargs
        }
        
        self.wm.create_project(project_id, project_data)
        
        return {
            'success': True,
            'project_id': project_id,
            'name': name,
            'message': f"✅ 已创建项目：{name}"
        }
    
    def list_projects(self, status: str = 'active') -> List[Dict]:
        """
        列出项目
        
        Args:
            status: 状态 (active/completed/archived)
        
        Returns:
            List[Dict]: 项目列表
        """
        project_ids = self.wm.list_projects(status)
        projects = []
        
        for pid in project_ids:
            project = self.wm.get_project(pid)
            if project:
                project['id'] = pid
                projects.append(project)
        
        return projects
    
    def complete_project(self, project_id: str) -> Dict:
        """完成项目"""
        success = self.wm.update_project_status(project_id, 'completed')
        return {
            'success': success,
            'message': f"✅ 项目已完成：{project_id}" if success else f"❌ 项目不存在：{project_id}"
        }
    
    # ============================================================
    # 任务管理
    # ============================================================
    
    def create_task(self, title: str, project_id: str = None,
                   priority: int = 3, due_date: str = None,
                   description: str = '', **kwargs) -> Dict:
        """
        创建任务
        
        Args:
            title: 任务标题
            project_id: 所属项目 ID（可选）
            priority: 优先级 (1-5, 1 最高)
            due_date: 截止日期 (YYYY-MM-DD)
            description: 任务描述
            **kwargs: 其他任务属性
        
        Returns:
            Dict: 任务信息
        
        示例：
        >>> plugin.create_task("数据验证", project_id="proj_001", priority=1)
        """
        import uuid
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        
        task_data = {
            'title': title,
            'priority': priority,
            'description': description,
            **kwargs
        }
        
        if project_id:
            task_data['project_id'] = project_id
        
        if due_date:
            task_data['due_date'] = due_date
        
        self.wm.create_task(task_id, task_data)
        
        return {
            'success': True,
            'task_id': task_id,
            'title': title,
            'message': f"✅ 已创建任务：{title}"
        }
    
    def complete_task(self, task_id: str) -> Dict:
        """完成任务"""
        self.wm.complete_task(task_id)
        return {
            'success': True,
            'message': f"✅ 任务已完成：{task_id}"
        }
    
    def get_pending_tasks(self, project_id: str = None) -> List[Dict]:
        """获取待办任务"""
        return self.wm.get_pending_tasks(project_id)
    
    # ============================================================
    # 工作日志
    # ============================================================
    
    def save_daily_log(self, date: str = None, 
                      tasks_completed: List[str] = None,
                      issues: List[str] = None,
                      notes: str = '', **kwargs) -> Dict:
        """
        保存日报
        
        Args:
            date: 日期（默认今天）
            tasks_completed: 完成的任务列表
            issues: 遇到的问题列表
            notes: 备注
        
        Returns:
            Dict: 保存结果
        
        示例：
        >>> plugin.save_daily_log(
        ...     tasks_completed=["完成数据验证", "编写测试"],
        ...     issues=["API 限流"],
        ...     notes="进展顺利"
        ... )
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        log_data = {
            'tasks_completed': tasks_completed or [],
            'issues': issues or [],
            'notes': notes,
            **kwargs
        }
        
        self.wm.save_daily_log(date, log_data)
        
        return {
            'success': True,
            'date': date,
            'message': f"✅ 已保存日报：{date}"
        }
    
    # ============================================================
    # 技能管理
    # ============================================================
    
    def add_skill(self, skill_name: str, level: str = 'beginner',
                 category: str = 'technical', description: str = '',
                 **kwargs) -> Dict:
        """
        添加技能
        
        Args:
            skill_name: 技能名称
            level: 水平 (beginner/intermediate/expert)
            category: 分类 (technical/soft/certifications)
            description: 技能描述
        
        Returns:
            Dict: 添加结果
        """
        skill_data = {
            'level': level,
            'description': description,
            'learned_at': datetime.now().isoformat(),
            **kwargs
        }
        
        self.wm.add_skill(skill_name, skill_data, category=category)
        
        return {
            'success': True,
            'skill_name': skill_name,
            'message': f"✅ 已添加技能：{skill_name} ({level})"
        }
    
    def get_skills(self, category: str = None) -> Dict:
        """获取技能列表"""
        skills = self.wm.get_skills(category)
        return {
            'count': len(skills),
            'skills': skills
        }
    
    # ============================================================
    # 统计信息
    # ============================================================
    
    def get_stats(self) -> Dict:
        """
        获取统计信息
        
        Returns:
            Dict: 统计信息
        
        示例：
        >>> stats = plugin.get_stats()
        >>> print(f"项目数：{stats['projects']['active']}")
        >>> print(f"任务数：{stats['tasks']['pending']}")
        """
        stats = self.wm.get_stats()
        
        # 格式化返回
        return {
            'data_dir': self.data_dir,
            'projects': stats['projects'],
            'tasks': stats['tasks'],
            'skills': stats['skills'],  # 现在是字典格式
            'contacts': stats['contacts'],
            'documents': stats['documents'],
            'total_size_kb': stats['total_size_kb']
        }
    
    # ============================================================
    # 备份
    # ============================================================
    
    def backup(self, backup_dir: str = None) -> Dict:
        """备份工作记忆"""
        backup_path = self.wm.backup(backup_dir)
        return {
            'success': True,
            'backup_path': backup_path,
            'message': f"✅ 已备份到：{backup_path}"
        }
    
    # ============================================================
    # 便捷方法
    # ============================================================
    
    def quick_start(self, project_name: str, task_title: str) -> Dict:
        """
        快速开始：创建项目 + 添加任务
        
        Args:
            project_name: 项目名称
            task_title: 第一个任务标题
        
        Returns:
            Dict: 项目 + 任务信息
        """
        # 创建项目
        project_result = self.create_project(project_name)
        project_id = project_result['project_id']
        
        # 创建任务
        task_result = self.create_task(task_title, project_id=project_id)
        
        return {
            'success': True,
            'project': project_result,
            'task': task_result,
            'message': f"✅ 已创建项目 '{project_name}' 和任务 '{task_title}'"
        }


# ============================================================
# OpenClaw 命令处理器（可选）
# ============================================================

def handle_wm_command(command: str, args: List[str]) -> str:
    """
    处理 Work Memory 命令
    
    使用方式：
    - /wm project create "项目名称"
    - /wm task add "任务标题"
    - /wm stats
    
    Args:
        command: 子命令 (project/task/log/stats)
        args: 命令参数
    
    Returns:
        str: 响应消息
    """
    plugin = WorkMemoryPlugin()
    
    if command == 'project' and args and args[0] == 'create':
        name = args[1] if len(args) > 1 else '未命名项目'
        result = plugin.create_project(name)
        return result['message']
    
    elif command == 'task' and args and args[0] == 'add':
        title = ' '.join(args[1:]) if len(args) > 1 else '未命名任务'
        result = plugin.create_task(title)
        return result['message']
    
    elif command == 'stats':
        stats = plugin.get_stats()
        return (
            f"📊 工作记忆统计\n"
            f"项目：{stats['projects']['active']} 进行中\n"
            f"任务：{stats['tasks']['pending']} 待办\n"
            f"技能：{stats['skills']['count']} 个\n"
            f"文档：{stats['documents']} 个"
        )
    
    elif command == 'log' and args and args[0] == 'daily':
        result = plugin.save_daily_log()
        return result['message']
    
    else:
        return "❌ 未知命令。可用命令：/wm project create, /wm task add, /wm stats, /wm log daily"


# ============================================================
# 测试
# ============================================================

if __name__ == '__main__':
    print("=" * 70)
    print("🧪 Work Memory 插件测试")
    print("=" * 70)
    
    plugin = WorkMemoryPlugin()
    
    # 测试 1: 快速开始
    print("\n【1】快速开始...")
    result = plugin.quick_start("测试项目", "第一个任务")
    print(f"  {result['message']}")
    
    # 测试 2: 获取统计
    print("\n【2】统计信息...")
    stats = plugin.get_stats()
    print(f"  项目数：{stats['projects']['active']}")
    print(f"  任务数：{stats['tasks']['pending']}")
    print(f"  技能数：{stats['skills']['count']}")
    
    # 测试 3: 命令处理
    print("\n【3】命令处理...")
    msg = handle_wm_command('stats', [])
    print(f"  {msg}")
    
    print("\n" + "=" * 70)
    print("✅ 测试完成")
    print("=" * 70)
