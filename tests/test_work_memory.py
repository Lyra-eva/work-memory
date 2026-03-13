#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作记忆系统测试
"""

import os
import sys
import tempfile
import shutil
import unittest

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from work_memory import WorkMemory


class TestWorkMemory(unittest.TestCase):
    """工作记忆系统测试"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.wm = WorkMemory(root_dir=self.test_dir)
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_create_project(self):
        """测试创建项目"""
        self.wm.create_project("proj_001", {
            'name': '测试项目',
            'priority': 'high'
        })
        
        project = self.wm.get_project("proj_001")
        self.assertIsNotNone(project)
        self.assertEqual(project['name'], '测试项目')
    
    def test_create_task(self):
        """测试创建任务"""
        self.wm.create_task("task_001", {
            'title': '测试任务',
            'priority': 1
        })
        
        tasks = self.wm.get_pending_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['title'], '测试任务')
    
    def test_complete_task(self):
        """测试完成任务"""
        self.wm.create_task("task_001", {
            'title': '测试任务',
            'priority': 1
        })
        
        self.wm.complete_task("task_001")
        
        tasks = self.wm.get_pending_tasks()
        self.assertEqual(len(tasks), 0)
    
    def test_add_skill(self):
        """测试添加技能"""
        self.wm.add_skill("python", {
            'level': 'expert',
            'description': 'Python 编程'
        }, category='technical')
        
        skills = self.wm.get_skills()
        self.assertIn('python', skills)
    
    def test_save_document(self):
        """测试保存文档"""
        self.wm.save_document(
            doc_id="doc_001",
            content="# 测试文档",
            category="technical"
        )
        
        results = self.wm.search_documents("测试")
        self.assertEqual(len(results), 1)
    
    def test_add_contact(self):
        """测试添加联系人"""
        self.wm.add_contact("contact_001", {
            'name': '张三',
            'email': 'zhangsan@example.com'
        }, category='colleagues')
        
        contact = self.wm.get_contact("contact_001")
        self.assertIsNotNone(contact)
        self.assertEqual(contact['name'], '张三')
    
    def test_save_meeting_note(self):
        """测试保存会议记录"""
        self.wm.save_meeting_note("meeting_001", {
            'title': '测试会议',
            'date': '2026-03-13',
            'attendees': ['张三'],
            'notes': '会议内容',
            'action_items': ['待办 1']
        })
        
        # 检查文件是否存在
        note_file = os.path.join(
            self.test_dir, "meetings", "notes", "meeting_001.md"
        )
        self.assertTrue(os.path.exists(note_file))
    
    def test_save_daily_log(self):
        """测试保存日报"""
        self.wm.save_daily_log("2026-03-13", {
            'tasks_completed': ['任务 1'],
            'notes': '测试日报'
        })
        
        log_file = os.path.join(
            self.test_dir, "logs", "daily", "2026-03-13.md"
        )
        self.assertTrue(os.path.exists(log_file))
    
    def test_get_stats(self):
        """测试统计信息"""
        self.wm.create_project("proj_001", {'name': '测试'})
        self.wm.create_task("task_001", {'title': '测试'})
        
        stats = self.wm.get_stats()
        
        self.assertIn('projects', stats)
        self.assertIn('tasks', stats)
        self.assertEqual(stats['projects']['active'], 1)
    
    def test_backup_restore(self):
        """测试备份恢复"""
        # 创建数据
        self.wm.create_project("proj_001", {'name': '测试'})
        
        # 备份
        backup_path = self.wm.backup()
        self.assertTrue(os.path.exists(backup_path))
        
        # 删除原数据
        shutil.rmtree(self.test_dir)
        
        # 恢复
        self.wm = WorkMemory(root_dir=self.test_dir)
        self.wm.restore(backup_path)
        
        # 验证
        project = self.wm.get_project("proj_001")
        self.assertIsNotNone(project)


def run_tests():
    """运行测试"""
    unittest.main()


if __name__ == '__main__':
    run_tests()
