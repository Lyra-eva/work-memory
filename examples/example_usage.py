#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Work Memory 使用示例

展示如何在 OpenClaw 技能中使用 Work Memory 插件
"""

from work_memory_plugin import WorkMemoryPlugin


# ============================================================
# 示例 1: 项目管理
# ============================================================

def example_project_management():
    """项目管理示例"""
    print("=" * 70)
    print("📋 项目管理示例")
    print("=" * 70)
    
    plugin = WorkMemoryPlugin()
    
    # 创建项目
    result = plugin.create_project(
        name="A 股交易智能体系统",
        description="基于强化学习的量化交易系统",
        priority="high",
        tags=["quant", "trading", "ai"]
    )
    print(f"✅ {result['message']}")
    project_id = result['project_id']
    
    # 列出项目
    projects = plugin.list_projects('active')
    print(f"📊 当前有 {len(projects)} 个进行中项目")
    
    # 完成项目
    # plugin.complete_project(project_id)
    
    return project_id


# ============================================================
# 示例 2: 任务管理
# ============================================================

def example_task_management(project_id: str = None):
    """任务管理示例"""
    print("\n" + "=" * 70)
    print("✅ 任务管理示例")
    print("=" * 70)
    
    plugin = WorkMemoryPlugin()
    
    # 创建多个任务
    tasks = [
        ("数据验证模块", 1, "2026-03-15"),
        ("策略回测引擎", 2, "2026-03-20"),
        ("风险控制模块", 1, "2026-03-18"),
        ("可视化界面", 3, "2026-03-25"),
    ]
    
    for title, priority, due_date in tasks:
        result = plugin.create_task(
            title=title,
            project_id=project_id,
            priority=priority,
            due_date=due_date,
            description=f"实现{title}功能"
        )
        print(f"✅ {result['message']}")
    
    # 获取待办任务
    pending = plugin.get_pending_tasks(project_id)
    print(f"\n📊 当前有 {len(pending)} 个待办任务")
    
    # 完成任务
    if pending:
        task_id = list(pending[0].keys())[0]  # 获取第一个任务 ID
        # plugin.complete_task(task_id)


# ============================================================
# 示例 3: 工作日志
# ============================================================

def example_daily_log():
    """工作日志示例"""
    print("\n" + "=" * 70)
    print("📝 工作日志示例")
    print("=" * 70)
    
    plugin = WorkMemoryPlugin()
    
    # 写日报
    result = plugin.save_daily_log(
        tasks_completed=[
            "完成数据验证模块",
            "编写单元测试",
            "修复 3 个 bug"
        ],
        issues=[
            "API 限流问题",
            "数据格式不一致"
        ],
        notes="今天进展顺利，明天开始做策略回测"
    )
    print(f"✅ {result['message']}")


# ============================================================
# 示例 4: 技能管理
# ============================================================

def example_skill_tracking():
    """技能管理示例"""
    print("\n" + "=" * 70)
    print("🎯 技能管理示例")
    print("=" * 70)
    
    plugin = WorkMemoryPlugin()
    
    # 添加技能
    skills = [
        ("Python 高级编程", "expert", "technical"),
        ("量化分析", "intermediate", "technical"),
        ("机器学习", "intermediate", "technical"),
        ("项目管理", "advanced", "soft"),
    ]
    
    for name, level, category in skills:
        result = plugin.add_skill(
            skill_name=name,
            level=level,
            category=category,
            description=f"{name} - {level}水平"
        )
        print(f"✅ {result['message']}")
    
    # 获取技能统计
    stats = plugin.get_skills()
    print(f"\n📊 共有 {stats['count']} 个技能")


# ============================================================
# 示例 5: 统计信息
# ============================================================

def example_stats():
    """统计信息示例"""
    print("\n" + "=" * 70)
    print("📊 统计信息示例")
    print("=" * 70)
    
    plugin = WorkMemoryPlugin()
    
    stats = plugin.get_stats()
    
    print(f"""
📈 工作记忆统计

📁 数据目录：{stats['data_dir']}

📋 项目:
  - 进行中：{stats['projects']['active']} 个
  - 已完成：{stats['projects']['completed']} 个
  - 已归档：{stats['projects']['archived']} 个

✅ 任务:
  - 待办：{stats['tasks']['pending']} 个
  - 进行中：{stats['tasks']['in_progress']} 个
  - 已完成：{stats['tasks']['completed']} 个

🎯 技能：{stats['skills']['count']} 个

📄 文档：{stats['documents']} 个

💾 总大小：{stats['total_size_kb']} KB
""")


# ============================================================
# 示例 6: 命令处理
# ============================================================

def example_commands():
    """命令处理示例"""
    print("\n" + "=" * 70)
    print("⌨️  命令处理示例")
    print("=" * 70)
    
    from work_memory_plugin import handle_wm_command
    
    # 模拟用户输入命令
    commands = [
        ('stats', []),
        ('project', ['create', '测试项目']),
        ('task', ['add', '测试任务']),
        ('log', ['daily']),
    ]
    
    for cmd, args in commands:
        print(f"\n用户输入：/wm {cmd} {' '.join(args)}")
        response = handle_wm_command(cmd, args)
        print(f"AI 回复：{response}")


# ============================================================
# 示例 7: 在 OpenClaw 技能中使用
# ============================================================

def example_in_skill():
    """在 OpenClaw 技能中使用示例"""
    print("\n" + "=" * 70)
    print("🧩 在 OpenClaw 技能中使用")
    print("=" * 70)
    
    # 这是一个模拟的 OpenClaw 技能
    class MyOpenClawSkill:
        """示例技能：项目助手"""
        
        def __init__(self):
            self.wm = WorkMemoryPlugin()
        
        def handle_user_request(self, user_message: str) -> str:
            """处理用户请求"""
            
            if "创建项目" in user_message:
                # 提取项目名称（简化版）
                project_name = user_message.replace("创建项目", "").strip()
                if not project_name:
                    project_name = "未命名项目"
                
                result = self.wm.create_project(project_name)
                return f"✅ {result['message']}\n需要我帮你添加任务吗？"
            
            elif "添加任务" in user_message:
                task_title = user_message.replace("添加任务", "").strip()
                if not task_title:
                    task_title = "未命名任务"
                
                result = self.wm.create_task(task_title)
                return f"✅ {result['message']}"
            
            elif "查看进度" in user_message:
                stats = self.wm.get_stats()
                return (
                    f"📊 当前进度：\n"
                    f"- {stats['projects']['active']} 个项目进行中\n"
                    f"- {stats['tasks']['pending']} 个任务待办"
                )
            
            else:
                return "我可以帮你：创建项目、添加任务、查看进度"
    
    # 测试技能
    skill = MyOpenClawSkill()
    
    test_messages = [
        "创建项目 A 股智能体",
        "添加任务 数据验证",
        "查看进度"
    ]
    
    for msg in test_messages:
        print(f"\n用户：{msg}")
        response = skill.handle_user_request(msg)
        print(f"AI: {response}")


# ============================================================
# 主函数
# ============================================================

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Work Memory 使用示例")
    print("=" * 70)
    
    try:
        # 运行所有示例
        project_id = example_project_management()
        example_task_management(project_id)
        example_daily_log()
        example_skill_tracking()
        example_stats()
        example_commands()
        example_in_skill()
        
        print("\n" + "=" * 70)
        print("✅ 所有示例运行完成！")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        print("\n提示：请先安装 work_memory:")
        print("  cd ~/.openclaw/workspace/work-memory-project")
        print("  pip install -e .")
