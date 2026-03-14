#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Work Memory OpenClaw 技能

这是 Work Memory 核心库的 OpenClaw 技能包装器。
所有业务逻辑都在核心库 (work-memory PyPI 包) 中实现。
"""

import os
import sys
from typing import Dict, List, Optional

# 导入核心库
try:
    from work_memory import WorkMemory
except ImportError:
    print("⚠️ 请先安装 Work Memory 核心库：pip install work-memory")
    print("   或开发模式：cd ~/.openclaw/workspace/work-memory-project && pip install -e .")
    sys.exit(1)


class WorkMemorySkill:
    """
    Work Memory OpenClaw 技能
    
    这是核心库的轻薄包装器，只处理命令路由和用户交互。
    所有业务逻辑都在 WorkMemory 核心库中。
    """
    
    def __init__(self, data_dir: str = None):
        """
        初始化技能
        
        Args:
            data_dir: 数据目录，默认从 TOOLS.md 读取或使用默认值
        """
        if data_dir is None:
            data_dir = self._read_config_from_tools_md()
            if data_dir is None:
                data_dir = os.path.expanduser("~/.openclaw/workspace/work-memory-data")
        
        self.data_dir = data_dir
        self.wm = WorkMemory(root_dir=data_dir)
        print(f"✅ Work Memory 技能已加载：{self.data_dir}")
    
    def _read_config_from_tools_md(self) -> Optional[str]:
        """从 TOOLS.md 读取配置"""
        tools_md_path = os.path.expanduser("~/.openclaw/workspace/TOOLS.md")
        
        if not os.path.exists(tools_md_path):
            return None
        
        with open(tools_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找 Work Memory 配置段落
        in_work_memory_section = False
        
        for line in content.split('\n'):
            if '### Work Memory' in line or '### work-memory' in line:
                in_work_memory_section = True
                continue
            
            if in_work_memory_section:
                if line.startswith('###'):  # 新的段落
                    break
                
                if '数据目录' in line or 'data_dir' in line:
                    if ':' in line:
                        path = line.split(':', 1)[1].strip().strip('`"\'')
                        return os.path.expanduser(path)
        
        return None
    
    # ============================================================
    # 命令处理
    # ============================================================
    
    def handle_command(self, command: str, args: List[str]) -> str:
        """
        处理 Work Memory 命令
        
        Args:
            command: 子命令 (project/task/log/stats)
            args: 命令参数
        
        Returns:
            str: 响应消息
        """
        # 命令路由
        if command == 'project':
            return self._handle_project_command(args)
        elif command == 'task':
            return self._handle_task_command(args)
        elif command == 'log':
            return self._handle_log_command(args)
        elif command == 'stats':
            return self._handle_stats_command(args)
        else:
            return f"❌ 未知命令：{command}\n可用命令：project, task, log, stats"
    
    def _handle_project_command(self, args: List[str]) -> str:
        """处理项目命令"""
        if not args:
            return "用法：/wm project <create|list|complete> [参数]"
        
        action = args[0]
        
        if action == 'create':
            # /wm project create "项目名称" --priority high
            if len(args) < 2:
                return "用法：/wm project create <名称> [--priority high|medium|low]"
            
            name = args[1].strip('"\'')
            priority = 'medium'
            
            # 解析 --priority
            if '--priority' in args:
                idx = args.index('--priority')
                if idx + 1 < len(args):
                    priority = args[idx + 1]
            
            import uuid
            project_id = f"proj_{uuid.uuid4().hex[:8]}"
            
            self.wm.create_project(project_id, {
                'name': name,
                'priority': priority
            })
            
            return f"✅ 已创建项目：{name}\n项目 ID: {project_id}"
        
        elif action == 'list':
            # /wm project list --status active
            status = 'active'
            
            if '--status' in args:
                idx = args.index('--status')
                if idx + 1 < len(args):
                    status = args[idx + 1]
            
            projects = self.wm.list_projects(status)
            
            if not projects:
                return f"📊 没有{status}状态的项目"
            
            result = [f"📋 {status} 状态的项目 ({len(projects)} 个):"]
            for pid in projects:
                project = self.wm.get_project(pid)
                if project:
                    name = project.get('name', pid)
                    priority = project.get('priority', 'medium')
                    result.append(f"  - {pid}: {name} (优先级：{priority})")
            
            return '\n'.join(result)
        
        elif action == 'complete':
            if len(args) < 2:
                return "用法：/wm project complete <项目 ID>"
            
            project_id = args[1]
            success = self.wm.update_project_status(project_id, 'completed')
            
            if success:
                return f"✅ 项目已完成：{project_id}"
            else:
                return f"❌ 项目不存在：{project_id}"
        
        else:
            return f"❌ 未知的项目操作：{action}\n可用操作：create, list, complete"
    
    def _handle_task_command(self, args: List[str]) -> str:
        """处理任务命令"""
        if not args:
            return "用法：/wm task <add|list|complete> [参数]"
        
        action = args[0]
        
        if action == 'add':
            # /wm task add "任务标题" --project proj_001
            if len(args) < 2:
                return "用法：/wm task add <标题> [--project <项目 ID>]"
            
            title = args[1].strip('"\'')
            project_id = None
            
            if '--project' in args:
                idx = args.index('--project')
                if idx + 1 < len(args):
                    project_id = args[idx + 1]
            
            import uuid
            task_id = f"task_{uuid.uuid4().hex[:8]}"
            
            self.wm.create_task(task_id, {
                'title': title,
                'project_id': project_id,
                'priority': 3
            })
            
            msg = f"✅ 已创建任务：{title}"
            if project_id:
                msg += f"\n所属项目：{project_id}"
            msg += f"\n任务 ID: {task_id}"
            
            return msg
        
        elif action == 'list':
            # /wm task list --status pending
            status = 'pending'
            
            if '--status' in args:
                idx = args.index('--status')
                if idx + 1 < len(args):
                    status = args[idx + 1]
            
            tasks = self.wm.get_pending_tasks()
            
            if not tasks:
                return f"✅ 没有待办任务"
            
            result = [f"📋 待办任务 ({len(tasks)} 个):"]
            for task in tasks[:10]:  # 只显示前 10 个
                title = task.get('title', '未命名')
                priority = task.get('priority', 3)
                project_id = task.get('project_id', None)
                
                line = f"  - {title} (优先级：{priority})"
                if project_id:
                    line += f" [项目：{project_id}]"
                result.append(line)
            
            if len(tasks) > 10:
                result.append(f"  ... 还有 {len(tasks) - 10} 个任务")
            
            return '\n'.join(result)
        
        elif action == 'complete':
            if len(args) < 2:
                return "用法：/wm task complete <任务 ID>"
            
            task_id = args[1]
            self.wm.complete_task(task_id)
            
            return f"✅ 任务已完成：{task_id}"
        
        else:
            return f"❌ 未知的任务操作：{action}\n可用操作：add, list, complete"
    
    def _handle_log_command(self, args: List[str]) -> str:
        """处理日志命令"""
        if not args:
            return "用法：/wm log <daily|weekly>"
        
        log_type = args[0]
        
        if log_type == 'daily':
            # /wm log daily --tasks "任务 1,任务 2" --notes "备注"
            from datetime import datetime
            date = datetime.now().strftime('%Y-%m-%d')
            
            tasks_completed = []
            issues = []
            notes = ''
            
            # 解析 --tasks
            if '--tasks' in args:
                idx = args.index('--tasks')
                if idx + 1 < len(args):
                    tasks_str = args[idx + 1].strip('"\'')
                    tasks_completed = [t.strip() for t in tasks_str.split(',')]
            
            # 解析 --issues
            if '--issues' in args:
                idx = args.index('--issues')
                if idx + 1 < len(args):
                    issues_str = args[idx + 1].strip('"\'')
                    issues = [i.strip() for i in issues_str.split(',')]
            
            # 解析 --notes
            if '--notes' in args:
                idx = args.index('--notes')
                if idx + 1 < len(args):
                    notes = args[idx + 1].strip('"\'')
            
            self.wm.save_daily_log(date, {
                'tasks_completed': tasks_completed,
                'issues': issues,
                'notes': notes
            })
            
            return f"✅ 已保存日报：{date}\n完成的任务：{len(tasks_completed)} 个"
        
        elif log_type == 'weekly':
            return "🚧 周报功能开发中，请使用 /wm log daily"
        
        else:
            return f"❌ 未知的日志类型：{log_type}\n可用类型：daily, weekly"
    
    def _handle_stats_command(self, args: List[str]) -> str:
        """处理统计命令"""
        stats = self.wm.get_stats()
        
        # 格式化输出
        lines = [
            "📊 Work Memory 统计",
            "",
            f"📁 数据目录：{self.data_dir}",
            "",
            "📋 项目:",
            f"  - 进行中：{stats['projects']['active']} 个",
            f"  - 已完成：{stats['projects']['completed']} 个",
            f"  - 已归档：{stats['projects']['archived']} 个",
            "",
            "✅ 任务:",
            f"  - 待办：{stats['tasks']['pending']} 个",
            f"  - 进行中：{stats['tasks']['in_progress']} 个",
            f"  - 已完成：{stats['tasks']['completed']} 个",
            "",
            f"🎯 技能：{stats['skills']['count']} 个",
            f"📄 文档：{stats['documents']} 个",
            "",
            f"💾 总大小：{stats['total_size_kb']} KB"
        ]
        
        return '\n'.join(lines)
    
    # ============================================================
    # 便捷方法
    # ============================================================
    
    def create_project(self, name: str, priority: str = 'medium') -> str:
        """快速创建项目"""
        import uuid
        project_id = f"proj_{uuid.uuid4().hex[:8]}"
        self.wm.create_project(project_id, {'name': name, 'priority': priority})
        return f"✅ 已创建项目：{name}\n项目 ID: {project_id}"
    
    def create_task(self, title: str, project_id: str = None) -> str:
        """快速创建任务"""
        import uuid
        task_id = f"task_{uuid.uuid4().hex[:8]}"
        self.wm.create_task(task_id, {'title': title, 'project_id': project_id})
        return f"✅ 已创建任务：{title}\n任务 ID: {task_id}"
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.wm.get_stats()


# ============================================================
# OpenClaw 技能入口
# ============================================================

def handle_wm_command(command: str, args: List[str]) -> str:
    """
    OpenClaw 技能入口函数
    
    使用方式：
    在技能中调用：handle_wm_command('project', ['create', '测试项目'])
    """
    skill = WorkMemorySkill()
    return skill.handle_command(command, args)


# ============================================================
# 测试
# ============================================================

if __name__ == '__main__':
    print("=" * 70)
    print("🧪 Work Memory 技能测试")
    print("=" * 70)
    
    skill = WorkMemorySkill()
    
    # 测试 1: 创建项目
    print("\n【1】创建项目...")
    msg = skill.handle_command('project', ['create', '测试项目', '--priority', 'high'])
    print(msg)
    
    # 测试 2: 列出项目
    print("\n【2】列出项目...")
    msg = skill.handle_command('project', ['list'])
    print(msg)
    
    # 测试 3: 添加任务
    print("\n【3】添加任务...")
    msg = skill.handle_command('task', ['add', '测试任务', '--project', 'proj_001'])
    print(msg)
    
    # 测试 4: 查看统计
    print("\n【4】查看统计...")
    msg = skill.handle_command('stats', [])
    print(msg)
    
    print("\n" + "=" * 70)
    print("✅ 测试完成")
    print("=" * 70)
