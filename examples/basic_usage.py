#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作记忆系统使用示例
"""

from work_memory import WorkMemory


def example_basic_usage():
    """基础使用示例"""
    print("=" * 70)
    print("工作记忆系统 - 基础使用示例")
    print("=" * 70)
    
    # 初始化
    wm = WorkMemory(root_dir="~/work_memory_demo")
    
    # 创建项目
    wm.create_project("proj_001", {
        'name': '进化引擎 5.0',
        'description': '下一代进化引擎',
        'priority': 'high',
        'start_date': '2026-03-01'
    })
    
    # 创建任务
    wm.create_task("task_001", {
        'title': '实现图谱关系',
        'description': '建立 DERIVED_FROM/DEPENDS_ON 关系',
        'priority': 1,
        'due_date': '2026-03-15',
        'project_id': 'proj_001'
    })
    
    # 添加技能
    wm.add_skill("python_advanced", {
        'level': 'expert',
        'description': '高级 Python 编程'
    }, category='technical')
    
    # 保存文档
    wm.save_document(
        doc_id="python_tips",
        content="# Python 技巧\n\n使用列表推导式...\n",
        category="technical",
        metadata={'title': 'Python 技巧', 'tags': 'python,tips'}
    )
    
    # 保存会议记录
    wm.save_meeting_note("meeting_001", {
        'title': '项目启动会',
        'date': '2026-03-13',
        'attendees': ['张三', '李四'],
        'notes': '讨论了项目范围和时间表',
        'action_items': ['完成需求文档', '制定开发计划']
    })
    
    # 保存日报
    wm.save_daily_log("2026-03-13", {
        'tasks_completed': ['实现工作记忆系统', '编写测试'],
        'issues': ['无重大问题'],
        'notes': '进展顺利'
    })
    
    # 查看统计
    stats = wm.get_stats()
    print(f"\n统计信息:")
    print(f"  项目数：{stats['projects']['active']} 个进行中")
    print(f"  任务数：{stats['tasks']['pending']} 个待办")
    print(f"  技能数：{stats['skills']} 个")
    print(f"  文档数：{stats['documents']} 个")
    
    # 打印目录树
    print(f"\n目录结构:")
    wm.print_tree(max_depth=2)
    
    # 备份
    backup_path = wm.backup()
    print(f"\n备份路径：{backup_path}")


def example_project_workflow():
    """项目工作流示例"""
    print("\n" + "=" * 70)
    print("项目工作流示例")
    print("=" * 70)
    
    wm = WorkMemory(root_dir="~/work_memory_project_demo")
    
    # 1. 项目启动
    wm.create_project("proj_new", {
        'name': '新客户项目',
        'priority': 'high'
    })
    
    # 2. 创建任务
    wm.create_task("task_req", {
        'title': '需求分析',
        'priority': 1,
        'project_id': 'proj_new'
    })
    
    # 3. 会议记录
    wm.save_meeting_note("meeting_kickoff", {
        'title': '项目启动会',
        'attendees': ['客户', '项目经理'],
        'action_items': ['完成需求文档']
    })
    
    # 4. 完成任务
    wm.complete_task("task_req")
    
    # 5. 项目完成
    wm.update_project_status("proj_new", "completed")
    
    # 6. 查看统计
    stats = wm.get_stats()
    print(f"已完成项目：{stats['projects']['completed']} 个")


def example_skill_tracking():
    """技能追踪示例"""
    print("\n" + "=" * 70)
    print("技能追踪示例")
    print("=" * 70)
    
    wm = WorkMemory(root_dir="~/work_memory_skills_demo")
    
    # 添加技能
    wm.add_skill("kubernetes", {
        'level': 'beginner',
        'started_at': '2026-03-01',
        'resources': ['K8s 官方文档']
    }, category='technical')
    
    # 保存学习笔记
    wm.save_document(
        doc_id="k8s_notes",
        content="# Kubernetes 学习笔记\n\n## Pod 概念\n...",
        category="technical",
        metadata={'tags': 'k8s,devops'}
    )
    
    # 关联技能和文档
    wm.link_items("k8s_notes", "kubernetes", "supports")
    
    # 查看技能
    skills = wm.get_skills()
    print(f"已记录技能：{len(skills)} 个")
    for skill_name, skill_data in skills.items():
        print(f"  - {skill_name}: {skill_data.get('level', 'N/A')}")


if __name__ == '__main__':
    # 运行示例
    example_basic_usage()
    example_project_workflow()
    example_skill_tracking()
    
    print("\n" + "=" * 70)
    print("✅ 所有示例运行完成")
    print("=" * 70)
