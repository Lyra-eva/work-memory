#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作记忆系统 (WorkMemory)

借鉴 memU 文件系统设计理念，专为工作场景设计的记忆系统

功能:
- 项目管理记忆
- 工作任务记忆
- 技能成长记忆
- 文档知识记忆
- 人际关系记忆
- 会议记录记忆

版本：1.0.0
创建：2026-03-13
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


# ============================================================
# 工作记忆系统
# ============================================================

class WorkMemory:
    """
    工作记忆系统
    
    专为工作场景设计的文件系统记忆架构
    """
    
    def __init__(self, root_dir: str = "~/openclaw/workspace/work_memory"):
        """
        初始化工作记忆系统
        
        Args:
            root_dir: 记忆根目录
        """
        self.root_dir = os.path.expanduser(root_dir)
        self._init_directories()
        print(f"✅ 工作记忆系统已初始化：{self.root_dir}")
    
    def _init_directories(self):
        """初始化目录结构"""
        # 核心工作目录
        directories = [
            # 项目管理
            "projects/active",       # 进行中项目
            "projects/completed",    # 已完成项目
            "projects/archived",     # 已归档项目
            
            # 工作任务
            "tasks/pending",         # 待办任务
            "tasks/in_progress",     # 进行中任务
            "tasks/completed",       # 已完成任务
            
            # 技能成长
            "skills/technical",      # 技术技能
            "skills/soft",           # 软技能
            "skills/certifications", # 证书资质
            
            # 文档知识
            "knowledge/technical",   # 技术文档
            "knowledge/business",    # 业务知识
            "knowledge/templates",   # 模板文档
            
            # 人际关系
            "contacts/colleagues",   # 同事
            "contacts/clients",      # 客户
            "contacts/partners",     # 合作伙伴
            
            # 会议记录
            "meetings/notes",        # 会议笔记
            "meetings/action_items", # 会议待办
            
            # 工作日志
            "logs/daily",            # 日报
            "logs/weekly",           # 周报
            "logs/monthly",          # 月报
            
            # 系统目录
            "backups",               # 备份
            "relationships"          # 关系索引
        ]
        
        for dir_path in directories:
            full_path = os.path.join(self.root_dir, dir_path)
            os.makedirs(full_path, exist_ok=True)
        
        print(f"✅ 已创建 {len(directories)} 个工作目录")
    
    # ============================================================
    # 项目管理
    # ============================================================
    
    def create_project(self, project_id: str, project_data: Dict):
        """
        创建项目
        
        Args:
            project_id: 项目 ID
            project_data: 项目数据 {name, description, start_date, status, ...}
        """
        project_file = os.path.join(
            self.root_dir, "projects", "active", f"{project_id}.json"
        )
        
        # 添加元数据
        project_data['metadata'] = {
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        with open(project_file, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 已创建项目：{project_data.get('name', project_id)}")
        return project_file
    
    def get_project(self, project_id: str) -> Optional[Dict]:
        """获取项目"""
        # 在 active/completed/archived 中查找
        for status in ['active', 'completed', 'archived']:
            path = os.path.join(
                self.root_dir, "projects", status, f"{project_id}.json"
            )
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        return None
    
    def update_project_status(self, project_id: str, new_status: str):
        """
        更新项目状态
        
        Args:
            project_id: 项目 ID
            new_status: 新状态 (active/completed/archived)
        """
        # 查找项目
        project_data = self.get_project(project_id)
        if not project_data:
            print(f"❌ 项目不存在：{project_id}")
            return False
        
        # 删除旧文件
        for status in ['active', 'completed', 'archived']:
            old_path = os.path.join(
                self.root_dir, "projects", status, f"{project_id}.json"
            )
            if os.path.exists(old_path):
                os.remove(old_path)
        
        # 保存到新状态目录
        project_data['metadata']['status'] = new_status
        project_data['metadata']['updated_at'] = datetime.now().isoformat()
        
        new_path = os.path.join(
            self.root_dir, "projects", new_status, f"{project_id}.json"
        )
        
        with open(new_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 项目状态已更新：{project_id} → {new_status}")
        return True
    
    def list_projects(self, status: str = 'active') -> List[str]:
        """列出项目"""
        path = os.path.join(self.root_dir, "projects", status)
        files = [f.replace('.json', '') for f in os.listdir(path) if f.endswith('.json')]
        return files
    
    # ============================================================
    # 任务管理
    # ============================================================
    
    def create_task(self, task_id: str, task_data: Dict):
        """
        创建任务
        
        Args:
            task_id: 任务 ID
            task_data: 任务数据 {title, description, priority, due_date, project_id, ...}
        """
        task_file = os.path.join(
            self.root_dir, "tasks", "pending", f"{task_id}.json"
        )
        
        # 添加元数据
        task_data['metadata'] = {
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        with open(task_file, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 已创建任务：{task_data.get('title', task_id)}")
        return task_file
    
    def complete_task(self, task_id: str):
        """完成任务"""
        self._move_task(task_id, 'pending', 'completed')
    
    def _move_task(self, task_id: str, from_status: str, to_status: str):
        """移动任务状态"""
        old_path = os.path.join(
            self.root_dir, "tasks", from_status, f"{task_id}.json"
        )
        
        if not os.path.exists(old_path):
            print(f"❌ 任务不存在：{task_id}")
            return False
        
        with open(old_path, 'r', encoding='utf-8') as f:
            task_data = json.load(f)
        
        task_data['metadata']['status'] = to_status
        task_data['metadata']['updated_at'] = datetime.now().isoformat()
        
        new_path = os.path.join(
            self.root_dir, "tasks", to_status, f"{task_id}.json"
        )
        
        with open(new_path, 'w', encoding='utf-8') as f:
            json.dump(task_data, f, indent=2, ensure_ascii=False)
        
        os.remove(old_path)
        print(f"✅ 任务状态已更新：{task_id} → {to_status}")
        return True
    
    def get_pending_tasks(self, project_id: str = None) -> List[Dict]:
        """获取待办任务"""
        path = os.path.join(self.root_dir, "tasks", "pending")
        tasks = []
        
        for file in os.listdir(path):
            if not file.endswith('.json'):
                continue
            
            file_path = os.path.join(path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                task = json.load(f)
            
            # 按项目过滤
            if project_id and task.get('project_id') != project_id:
                continue
            
            tasks.append(task)
        
        # 按优先级排序
        tasks.sort(key=lambda x: x.get('priority', 3))
        
        return tasks
    
    # ============================================================
    # 技能管理
    # ============================================================
    
    def add_skill(self, skill_name: str, skill_data: Dict, category: str = 'technical'):
        """
        添加技能
        
        Args:
            skill_name: 技能名称
            skill_data: 技能数据 {level, learned_at, description, resources, ...}
            category: 技能分类 (technical/soft/certifications)
        """
        skill_file = os.path.join(
            self.root_dir, "skills", category, f"{skill_name}.json"
        )
        
        # 添加元数据
        skill_data['metadata'] = {
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'category': category
        }
        
        with open(skill_file, 'w', encoding='utf-8') as f:
            json.dump(skill_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 已添加技能：{skill_name} ({category})")
        return skill_file
    
    def get_skills(self, category: str = None) -> Dict[str, Dict]:
        """获取技能列表"""
        skills = {}
        
        categories = [category] if category else ['technical', 'soft', 'certifications']
        
        for cat in categories:
            path = os.path.join(self.root_dir, "skills", cat)
            if not os.path.exists(path):
                continue
            
            for file in os.listdir(path):
                if not file.endswith('.json'):
                    continue
                
                skill_name = file.replace('.json', '')
                file_path = os.path.join(path, file)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    skills[skill_name] = json.load(f)
        
        return skills
    
    # ============================================================
    # 知识管理
    # ============================================================
    
    def save_document(self, doc_id: str, content: str, category: str = 'technical', 
                     metadata: Dict = None):
        """
        保存文档
        
        Args:
            doc_id: 文档 ID
            content: 文档内容
            category: 分类 (technical/business/templates)
            metadata: 元数据 {title, tags, author, ...}
        """
        doc_dir = os.path.join(self.root_dir, "knowledge", category)
        os.makedirs(doc_dir, exist_ok=True)
        
        doc_file = os.path.join(doc_dir, f"{doc_id}.md")
        
        with open(doc_file, 'w', encoding='utf-8') as f:
            if metadata:
                f.write("---\n")
                for key, value in metadata.items():
                    f.write(f"{key}: {value}\n")
                f.write("---\n\n")
            
            f.write(content)
        
        print(f"✅ 已保存文档：{doc_id} ({category})")
        return doc_file
    
    def search_documents(self, query: str, category: str = None) -> List[Dict]:
        """搜索文档"""
        results = []
        
        categories = [category] if category else ['technical', 'business', 'templates']
        
        for cat in categories:
            path = os.path.join(self.root_dir, "knowledge", cat)
            if not os.path.exists(path):
                continue
            
            for file in os.listdir(path):
                if not file.endswith('.md'):
                    continue
                
                file_path = os.path.join(path, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if query.lower() in content.lower():
                        results.append({
                            'id': file.replace('.md', ''),
                            'category': cat,
                            'path': file_path,
                            'preview': content[:200] + '...' if len(content) > 200 else content
                        })
                except Exception as e:
                    print(f"⚠️ 读取失败 {file_path}: {e}")
        
        return results
    
    # ============================================================
    # 人际关系管理
    # ============================================================
    
    def add_contact(self, contact_id: str, contact_data: Dict, 
                   category: str = 'colleagues'):
        """
        添加联系人
        
        Args:
            contact_id: 联系人 ID
            contact_data: 联系人数据 {name, role, company, email, phone, ...}
            category: 分类 (colleagues/clients/partners)
        """
        contact_file = os.path.join(
            self.root_dir, "contacts", category, f"{contact_id}.json"
        )
        
        # 添加元数据
        contact_data['metadata'] = {
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'category': category
        }
        
        with open(contact_file, 'w', encoding='utf-8') as f:
            json.dump(contact_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 已添加联系人：{contact_data.get('name', contact_id)}")
        return contact_file
    
    def get_contact(self, contact_id: str) -> Optional[Dict]:
        """获取联系人"""
        for category in ['colleagues', 'clients', 'partners']:
            path = os.path.join(
                self.root_dir, "contacts", category, f"{contact_id}.json"
            )
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        return None
    
    # ============================================================
    # 会议管理
    # ============================================================
    
    def save_meeting_note(self, meeting_id: str, meeting_data: Dict):
        """
        保存会议记录
        
        Args:
            meeting_id: 会议 ID
            meeting_data: 会议数据 {title, date, attendees, notes, action_items, ...}
        """
        note_file = os.path.join(
            self.root_dir, "meetings", "notes", f"{meeting_id}.md"
        )
        
        with open(note_file, 'w', encoding='utf-8') as f:
            f.write(f"# {meeting_data.get('title', '会议记录')}\n\n")
            f.write(f"**日期**: {meeting_data.get('date', 'N/A')}\n")
            f.write(f"**参会者**: {', '.join(meeting_data.get('attendees', []))}\n\n")
            f.write("## 讨论内容\n\n")
            f.write(meeting_data.get('notes', ''))
            
            if 'action_items' in meeting_data:
                f.write("\n## 待办事项\n\n")
                for item in meeting_data['action_items']:
                    f.write(f"- [ ] {item}\n")
        
        # 保存 action_items 到单独目录
        if 'action_items' in meeting_data:
            action_file = os.path.join(
                self.root_dir, "meetings", "action_items", f"{meeting_id}.json"
            )
            with open(action_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'meeting_id': meeting_id,
                    'action_items': meeting_data['action_items'],
                    'created_at': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 已保存会议记录：{meeting_data.get('title', meeting_id)}")
        return note_file
    
    # ============================================================
    # 工作日志
    # ============================================================
    
    def save_daily_log(self, date: str, log_data: Dict):
        """
        保存日报
        
        Args:
            date: 日期 (YYYY-MM-DD)
            log_data: 日志数据 {tasks_completed, issues, notes, ...}
        """
        log_file = os.path.join(
            self.root_dir, "logs", "daily", f"{date}.md"
        )
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"# 工作日报 {date}\n\n")
            
            if 'tasks_completed' in log_data:
                f.write("## 完成的任务\n\n")
                for task in log_data['tasks_completed']:
                    f.write(f"- ✅ {task}\n")
            
            if 'issues' in log_data:
                f.write("\n## 遇到的问题\n\n")
                for issue in log_data['issues']:
                    f.write(f"- ⚠️ {issue}\n")
            
            if 'notes' in log_data:
                f.write("\n## 备注\n\n")
                f.write(log_data['notes'])
        
        print(f"✅ 已保存日报：{date}")
        return log_file
    
    # ============================================================
    # 交叉引用
    # ============================================================
    
    def link_items(self, source_id: str, target_id: str, relation: str):
        """
        创建关联
        
        Args:
            source_id: 源项目 ID
            target_id: 目标项目 ID
            relation: 关系类型 (requires/blocks/related_to/etc)
        """
        links_file = os.path.join(self.root_dir, "relationships", "links.json")
        
        # 读取现有链接
        links = []
        if os.path.exists(links_file):
            with open(links_file, 'r', encoding='utf-8') as f:
                links = json.load(f)
        
        # 添加新链接
        links.append({
            'source': source_id,
            'target': target_id,
            'relation': relation,
            'created_at': datetime.now().isoformat()
        })
        
        # 保存
        with open(links_file, 'w', encoding='utf-8') as f:
            json.dump(links, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 已创建关联：{source_id} → {target_id} ({relation})")
    
    # ============================================================
    # 备份和恢复
    # ============================================================
    
    def backup(self, backup_path: str = None):
        """备份工作记忆"""
        if not backup_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = os.path.join(self.root_dir, "..", "backups")
            os.makedirs(backup_dir, exist_ok=True)
            backup_path = os.path.join(backup_dir, f"work_memory_{timestamp}")
        
        backup_path = os.path.expanduser(backup_path)
        
        # 如果备份已存在，添加时间戳后缀
        if os.path.exists(backup_path):
            backup_path = f"{backup_path}_{datetime.now().strftime('%H%M%S%f')}"
        
        shutil.copytree(self.root_dir, backup_path)
        
        print(f"✅ 已备份工作记忆到：{backup_path}")
        return backup_path
    
    def restore(self, backup_path: str):
        """恢复工作记忆"""
        backup_path = os.path.expanduser(backup_path)
        
        if not os.path.exists(backup_path):
            print(f"❌ 备份不存在：{backup_path}")
            return False
        
        # 如果目标目录不存在，先创建
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir, exist_ok=True)
        
        # 复制备份内容到目标目录
        for item in os.listdir(backup_path):
            src_item = os.path.join(backup_path, item)
            dst_item = os.path.join(self.root_dir, item)
            
            if os.path.isdir(src_item):
                if os.path.exists(dst_item):
                    shutil.rmtree(dst_item)
                shutil.copytree(src_item, dst_item)
            else:
                shutil.copy2(src_item, dst_item)
        
        print(f"✅ 已从备份恢复：{backup_path}")
        return True
    
    # ============================================================
    # 统计和报告
    # ============================================================
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        # 获取技能详情
        skills_data = self.get_skills()
        skills_count = len(skills_data)
        
        stats = {
            'root_dir': self.root_dir,
            'projects': {
                'active': len(self.list_projects('active')),
                'completed': len(self.list_projects('completed')),
                'archived': len(self.list_projects('archived'))
            },
            'tasks': {
                'pending': len(os.listdir(os.path.join(self.root_dir, 'tasks', 'pending'))),
                'in_progress': len(os.listdir(os.path.join(self.root_dir, 'tasks', 'in_progress'))),
                'completed': len(os.listdir(os.path.join(self.root_dir, 'tasks', 'completed')))
            },
            'skills': {
                'count': skills_count,
                'details': skills_data
            },
            'contacts': 0,
            'documents': 0
        }
        
        # 统计联系人
        for category in ['colleagues', 'clients', 'partners']:
            path = os.path.join(self.root_dir, "contacts", category)
            if os.path.exists(path):
                stats['contacts'] += len([f for f in os.listdir(path) if f.endswith('.json')])
        
        # 统计文档
        for category in ['technical', 'business', 'templates']:
            path = os.path.join(self.root_dir, "knowledge", category)
            if os.path.exists(path):
                stats['documents'] += len([f for f in os.listdir(path) if f.endswith('.md')])
        
        # 计算总大小
        total_size = 0
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                total_size += os.path.getsize(os.path.join(root, file))
        
        stats['total_size_kb'] = round(total_size / 1024, 2)
        
        return stats
    
    def print_tree(self, max_depth: int = 2):
        """打印目录树"""
        print(f"\n📂 {self.root_dir}")
        
        def print_dir(path, prefix="", depth=0):
            if depth >= max_depth:
                return
            
            try:
                items = sorted(os.listdir(path))
            except PermissionError:
                return
            
            for i, item in enumerate(items):
                if item.startswith('.'):
                    continue
                
                item_path = os.path.join(path, item)
                is_last = (i == len(items) - 1)
                
                connector = "└── " if is_last else "├── "
                print(f"{prefix}{connector}{item}")
                
                if os.path.isdir(item_path):
                    extension = "    " if is_last else "│   "
                    print_dir(item_path, prefix + extension, depth + 1)
        
        print_dir(self.root_dir)


# ============================================================
# 测试
# ============================================================

def run_tests():
    """运行测试"""
    print("=" * 70)
    print("🧪 工作记忆系统测试")
    print("=" * 70)
    
    # 创建实例
    wm = WorkMemory()
    
    try:
        # 测试 1: 创建项目
        print("\n【1】创建项目...")
        wm.create_project("proj_001", {
            'name': '进化引擎 5.0',
            'description': '下一代进化引擎',
            'start_date': '2026-03-01',
            'priority': 'high'
        })
        
        # 测试 2: 创建任务
        print("\n【2】创建任务...")
        wm.create_task("task_001", {
            'title': '实现图谱关系完善',
            'description': '建立 DERIVED_FROM/DEPENDS_ON 关系',
            'priority': 1,
            'due_date': '2026-03-15',
            'project_id': 'proj_001'
        })
        
        # 测试 3: 添加技能
        print("\n【3】添加技能...")
        wm.add_skill("python_advanced", {
            'level': 'expert',
            'learned_at': '2026-03-01',
            'description': '高级 Python 编程'
        })
        
        # 测试 4: 保存文档
        print("\n【4】保存文档...")
        wm.save_document(
            doc_id="python_tips",
            content="# Python 技巧\n\n1. 使用列表推导式\n2. 使用装饰器...",
            category="technical",
            metadata={'title': 'Python 技巧', 'tags': 'python,tips'}
        )
        
        # 测试 5: 添加联系人
        print("\n【5】添加联系人...")
        wm.add_contact("contact_001", {
            'name': '张三',
            'role': '技术经理',
            'company': '某某公司',
            'email': 'zhangsan@example.com'
        }, category='colleagues')
        
        # 测试 6: 保存会议记录
        print("\n【6】保存会议记录...")
        wm.save_meeting_note("meeting_001", {
            'title': '项目启动会',
            'date': '2026-03-13',
            'attendees': ['张三', '李四'],
            'notes': '讨论了项目范围和时间表',
            'action_items': ['完成需求文档', '制定开发计划']
        })
        
        # 测试 7: 保存日报
        print("\n【7】保存日报...")
        wm.save_daily_log("2026-03-13", {
            'tasks_completed': ['实现工作记忆系统', '编写测试'],
            'issues': ['无'],
            'notes': '进展顺利'
        })
        
        # 测试 8: 搜索文档
        print("\n【8】搜索文档...")
        results = wm.search_documents("Python", category='technical')
        print(f"  找到 {len(results)} 条结果")
        
        # 测试 9: 获取待办任务
        print("\n【9】获取待办任务...")
        tasks = wm.get_pending_tasks(project_id='proj_001')
        print(f"  找到 {len(tasks)} 个待办任务")
        
        # 测试 10: 统计信息
        print("\n【10】统计信息...")
        stats = wm.get_stats()
        print(f"  项目数：{stats['projects']['active']} 个进行中")
        print(f"  任务数：{stats['tasks']['pending']} 个待办")
        print(f"  技能数：{stats['skills']} 个")
        print(f"  文档数：{stats['documents']} 个")
        print(f"  联系人数：{stats['contacts']} 个")
        print(f"  总大小：{stats['total_size_kb']}KB")
        
        # 测试 11: 打印目录树
        print("\n【11】目录结构...")
        wm.print_tree(max_depth=2)
        
        # 测试 12: 备份
        print("\n【12】备份...")
        backup_path = wm.backup()
        print(f"  备份路径：{backup_path}")
        
    finally:
        print("\n" + "=" * 70)
        print("✅ 工作记忆系统测试完成")
        print("=" * 70)


if __name__ == '__main__':
    run_tests()
