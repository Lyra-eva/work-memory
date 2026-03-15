#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试套件 - 进化引擎 v3.5.1

测试覆盖:
- 知识图谱模块
- 记忆巩固模块
- 记忆关联模块
- 异常处理

版本：v3.5.1
创建：2026-03-15
"""

import sys
import os
import unittest

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.knowledge_graph import KnowledgeGraph, create_node, create_relation
from core.memory_consolidation import MemoryConsolidator, create_memory
from core.memory_linking import MemoryLinker
from core.exceptions import (
    NodeNotFoundError,
    MemoryNotFoundError,
    InvalidRecallQualityError,
    InvalidNodeError
)


# ============================================================
# 知识图谱测试
# ============================================================

class TestKnowledgeGraph(unittest.TestCase):
    """知识图谱单元测试"""
    
    def setUp(self):
        """测试前准备"""
        import tempfile
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.kg = KnowledgeGraph(self.temp_db.name)
    
    def tearDown(self):
        """测试后清理"""
        del self.kg
        import os
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)
    
    # ========== 节点管理测试 ==========
    
    def test_add_node(self):
        """测试添加节点"""
        node = create_node("Test Skill", "skill", "测试技能", mastery=0.5)
        node_id = self.kg.add_node(node)
        
        self.assertIsNotNone(node_id)
        self.assertIn(node_id, self.kg.nodes)
        self.assertEqual(self.kg.nodes[node_id].name, "Test Skill")
    
    def test_get_node(self):
        """测试查询节点"""
        node = create_node("Test", "skill", "测试")
        self.kg.add_node(node)
        
        fetched = self.kg.get_node(node.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "Test")
    
    def test_get_node_not_found(self):
        """测试查询不存在的节点"""
        result = self.kg.get_node("nonexistent")
        self.assertIsNone(result)
    
    def test_get_node_not_found_with_exception(self):
        """测试查询不存在的节点（抛出异常）"""
        with self.assertRaises(NodeNotFoundError):
            self.kg.get_node("nonexistent", raise_not_found=True)
    
    def test_update_node(self):
        """测试更新节点"""
        node = create_node("Test", "skill", "测试技能", mastery=0.5)
        self.kg.add_node(node)
        
        self.kg.update_node(node.id, mastery_level=0.8)
        updated = self.kg.get_node(node.id)
        
        self.assertEqual(updated.mastery_level, 0.8)
    
    def test_update_node_invalid_mastery(self):
        """测试更新节点（无效掌握度）"""
        node = create_node("Test", "skill", "测试技能", mastery=0.5)
        self.kg.add_node(node)
        
        with self.assertRaises(InvalidNodeError):
            self.kg.update_node(node.id, mastery_level=1.5)
    
    def test_delete_node(self):
        """测试删除节点"""
        node = create_node("Test", "skill", "测试技能")
        self.kg.add_node(node)
        
        result = self.kg.delete_node(node.id)
        self.assertTrue(result)
        self.assertNotIn(node.id, self.kg.nodes)
    
    def test_list_nodes(self):
        """测试列出节点"""
        for i in range(5):
            node = create_node(f"Node{i}", "skill", f"测试节点{i}", mastery=i*0.2)
            self.kg.add_node(node)
        
        all_nodes = self.kg.list_nodes()
        self.assertEqual(len(all_nodes), 5)
        
        # 按类别过滤
        skills = self.kg.list_nodes(category="skill")
        self.assertEqual(len(skills), 5)
        
        # 按掌握度过滤
        high_mastery = self.kg.list_nodes(min_mastery=0.6)
        self.assertEqual(len(high_mastery), 2)
    
    # ========== 关系管理测试 ==========
    
    def test_add_relation(self):
        """测试添加关系"""
        node1 = create_node("Node1", "skill", "技能 1")
        node2 = create_node("Node2", "skill", "技能 2")
        self.kg.add_node(node1)
        self.kg.add_node(node2)
        
        rel = create_relation(node1.id, node2.id, "depends_on", strength=0.9)
        rel_id = self.kg.add_relation(rel)
        
        self.assertIsNotNone(rel_id)
        self.assertEqual(len(self.kg.relations), 1)
    
    def test_get_relations(self):
        """测试查询关系"""
        node1 = create_node("Node1", "skill", "技能 1")
        node2 = create_node("Node2", "skill", "技能 2")
        self.kg.add_node(node1)
        self.kg.add_node(node2)
        
        rel = create_relation(node1.id, node2.id, "depends_on")
        self.kg.add_relation(rel)
        
        relations = self.kg.get_relations(node1.id)
        self.assertEqual(len(relations), 1)
    
    # ========== 知识发现测试 ==========
    
    def test_find_knowledge_gaps(self):
        """测试知识盲区发现"""
        basic = create_node("Basic", "skill", "基础", mastery=0.3)
        advanced = create_node("Advanced", "skill", "进阶", mastery=0.8)
        self.kg.add_node(basic)
        self.kg.add_node(advanced)
        
        rel = create_relation(basic.id, advanced.id, "depends_on")
        self.kg.add_relation(rel)
        
        gaps = self.kg.find_knowledge_gaps(advanced.id)
        self.assertIn(basic.id, gaps)
    
    def test_suggest_learning_path(self):
        """测试学习路径规划"""
        basic = create_node("Basic", "skill", "基础", mastery=0.3)
        advanced = create_node("Advanced", "skill", "进阶", mastery=0.8)
        self.kg.add_node(basic)
        self.kg.add_node(advanced)
        
        rel = create_relation(basic.id, advanced.id, "depends_on")
        self.kg.add_relation(rel)
        
        path = self.kg.suggest_learning_path(advanced.id)
        self.assertIn(basic.id, path)
    
    def test_calculate_similarity(self):
        """测试相似度计算"""
        node1 = create_node("Python Programming", "skill", "Python 编程")
        node2 = create_node("Python Development", "skill", "Python 开发")
        self.kg.add_node(node1)
        self.kg.add_node(node2)
        
        sim = self.kg.calculate_similarity(node1.id, node2.id)
        self.assertGreater(sim, 0.0)  # 应该有一定相似度


# ============================================================
# 记忆巩固测试
# ============================================================

class TestMemoryConsolidation(unittest.TestCase):
    """记忆巩固单元测试"""
    
    def setUp(self):
        """测试前准备"""
        import tempfile
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.mc = MemoryConsolidator(self.temp_db.name)
    
    def tearDown(self):
        """测试后清理"""
        del self.mc
        import os
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)
    
    # ========== 记忆项目管理测试 ==========
    
    def test_add_memory(self):
        """测试添加记忆"""
        memory = create_memory({'type': 'test', 'name': '测试记忆'}, importance=0.8)
        memory_id = self.mc.add_memory(memory)
        
        self.assertIsNotNone(memory_id)
        self.assertIn(memory_id, self.mc.memories)
    
    def test_get_memory(self):
        """测试查询记忆"""
        memory = create_memory({'type': 'test', 'name': '测试记忆'})
        self.mc.add_memory(memory)
        
        fetched = self.mc.get_memory(memory.id)
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.content['name'], '测试记忆')
    
    def test_get_memory_not_found(self):
        """测试查询不存在的记忆"""
        result = self.mc.get_memory("nonexistent")
        self.assertIsNone(result)
    
    def test_delete_memory(self):
        """测试删除记忆"""
        memory = create_memory({'type': 'test', 'name': '测试记忆'})
        self.mc.add_memory(memory)
        
        result = self.mc.delete_memory(memory.id)
        self.assertTrue(result)
        self.assertNotIn(memory.id, self.mc.memories)
    
    # ========== 遗忘曲线测试 ==========
    
    def test_calculate_retention(self):
        """测试保留率计算"""
        memory = create_memory({'type': 'test'}, importance=0.8)
        self.mc.add_memory(memory)
        
        retention = self.mc.calculate_retention(memory)
        self.assertGreaterEqual(retention, 0.0)
        self.assertLessEqual(retention, 1.0)
    
    def test_predict_forgetting_time(self):
        """测试遗忘时间预测"""
        memory = create_memory({'type': 'test'}, importance=0.8)
        self.mc.add_memory(memory)
        
        time = self.mc.predict_forgetting_time(memory)
        self.assertGreaterEqual(time, 0.0)
    
    # ========== 复习调度测试 ==========
    
    def test_review_memory(self):
        """测试复习记忆"""
        memory = create_memory({'type': 'test'}, importance=0.8)
        self.mc.add_memory(memory)
        
        strength_before = memory.strength
        updated = self.mc.review_memory(memory.id, recall_quality=0.85)
        
        self.assertGreater(updated.strength, strength_before)
        self.assertEqual(memory.review_count, 1)
        self.assertIsNotNone(memory.next_review)
    
    def test_review_memory_not_found(self):
        """测试复习不存在的记忆"""
        with self.assertRaises(MemoryNotFoundError):
            self.mc.review_memory("nonexistent", 0.8)
    
    def test_review_memory_invalid_quality(self):
        """测试复习（无效回忆质量）"""
        memory = create_memory({'type': 'test'})
        self.mc.add_memory(memory)
        
        with self.assertRaises(InvalidRecallQualityError):
            self.mc.review_memory(memory.id, recall_quality=1.5)
    
    def test_get_due_memories(self):
        """测试获取到期记忆"""
        memory = create_memory({'type': 'test'})
        self.mc.add_memory(memory)
        
        due = self.mc.get_due_memories()
        self.assertIsInstance(due, list)
    
    def test_generate_review_schedule(self):
        """测试生成复习计划"""
        for i in range(5):
            memory = create_memory({'type': 'test', 'id': i}, importance=0.5 + i*0.1)
            self.mc.add_memory(memory)
        
        schedule = self.mc.generate_review_schedule(daily_capacity=3)
        self.assertLessEqual(len(schedule), 3)


# ============================================================
# 记忆关联测试
# ============================================================

class TestMemoryLinking(unittest.TestCase):
    """记忆关联单元测试"""
    
    def setUp(self):
        """测试前准备"""
        import tempfile
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.linker = MemoryLinker(self.temp_db.name)
    
    def tearDown(self):
        """测试后清理"""
        del self.linker
        import os
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)
    
    # ========== 相似度计算测试 ==========
    
    def test_calculate_similarity(self):
        """测试相似度计算"""
        mem1 = {
            'id': 'mem1',
            'tags': ['learning', 'skill'],
            'entities': ['python'],
            'created_at': '2026-03-15T10:00:00',
            'emotion': {'type': 'joy', 'valence': 'positive'},
            'content': '学习 Python 技能'
        }
        mem2 = {
            'id': 'mem2',
            'tags': ['learning', 'improvement'],
            'entities': ['python', 'coding'],
            'created_at': '2026-03-15T11:00:00',
            'emotion': {'type': 'excitement', 'valence': 'positive'},
            'content': '提升 Python 编程能力'
        }
        
        scores = self.linker.calculate_similarity(mem1, mem2)
        
        self.assertIn('thematic', scores)
        self.assertIn('entity', scores)
        self.assertIn('temporal', scores)
        self.assertIn('emotional', scores)
        self.assertIn('semantic', scores)
        self.assertIn('total', scores)
        self.assertGreaterEqual(scores['total'], 0.0)
        self.assertLessEqual(scores['total'], 1.0)
    
    # ========== 关联发现测试 ==========
    
    def test_find_related_memories(self):
        """测试查找相关记忆"""
        mem1 = {
            'id': 'mem1',
            'tags': ['learning'],
            'entities': ['python'],
            'created_at': '2026-03-15T10:00:00',
            'content': '学习'
        }
        mem2 = {
            'id': 'mem2',
            'tags': ['learning'],
            'entities': ['python'],
            'created_at': '2026-03-15T11:00:00',
            'content': '学习'
        }
        
        related = self.linker.find_related_memories(mem1, [mem1, mem2])
        self.assertIsInstance(related, list)
    
    def test_discover_links(self):
        """测试发现关联"""
        memories = [
            {'id': 'mem1', 'tags': ['learning'], 'content': '学习'},
            {'id': 'mem2', 'tags': ['learning'], 'content': '学习'},
        ]
        
        links = self.linker.discover_links(memories, min_strength=0.3)
        self.assertGreaterEqual(links, 0)
    
    # ========== 记忆链测试 ==========
    
    def test_create_memory_chain(self):
        """测试创建记忆链"""
        memories = [
            {'id': 'mem1', 'tags': ['a'], 'content': '内容 1'},
            {'id': 'mem2', 'tags': ['a'], 'content': '内容 2'},
        ]
        
        chain = self.linker.create_memory_chain(memories[0], memories)
        
        self.assertIsNotNone(chain.id)
        self.assertGreaterEqual(len(chain.memories), 1)
    
    # ========== 上下文摘要测试 ==========
    
    def test_generate_context_summary(self):
        """测试生成上下文摘要"""
        current = {
            'id': 'current',
            'title': '当前记忆',
            'tags': ['learning'],
            'entities': ['python']
        }
        related = [
            {
                'id': 'related1',
                'title': '相关记忆 1',
                'tags': ['learning'],
                'created_at': '2026-03-15T10:00:00'
            }
        ]
        
        summary = self.linker.generate_context_summary(current, related)
        
        self.assertEqual(summary.current_memory, 'current')
        self.assertIn('related1', summary.related_memories)
        self.assertIsInstance(summary.summary_text, str)


# ============================================================
# 异常处理测试
# ============================================================

class TestExceptions(unittest.TestCase):
    """异常处理测试"""
    
    def test_node_not_found_error(self):
        """测试 NodeNotFoundError"""
        try:
            raise NodeNotFoundError("test_id", ["suggestion1", "suggestion2"])
        except NodeNotFoundError as e:
            self.assertIn("test_id", str(e))
            self.assertIn("suggestion1", str(e))
    
    def test_memory_not_found_error(self):
        """测试 MemoryNotFoundError"""
        try:
            raise MemoryNotFoundError("test_memory")
        except MemoryNotFoundError as e:
            self.assertIn("test_memory", str(e))
    
    def test_invalid_recall_quality_error(self):
        """测试 InvalidRecallQualityError"""
        try:
            raise InvalidRecallQualityError(1.5)
        except InvalidRecallQualityError as e:
            self.assertIn("1.5", str(e))
            self.assertIn("0.0 - 1.0", str(e))


# ============================================================
# 性能测试
# ============================================================

class TestPerformance(unittest.TestCase):
    """性能测试"""
    
    def test_batch_insert_performance(self):
        """批量插入性能测试"""
        kg = KnowledgeGraph(":memory:")
        
        import time
        start = time.time()
        
        for i in range(100):
            node = create_node(f"Node{i}", "concept", f"测试节点{i}")
            kg.add_node(node)
        
        elapsed = time.time() - start
        
        # 要求：< 1 秒
        self.assertLess(elapsed, 1.0, f"批量插入超时：{elapsed:.2f}秒")
    
    def test_query_performance(self):
        """查询性能测试"""
        kg = KnowledgeGraph(":memory:")
        
        # 准备数据
        for i in range(100):
            node = create_node(f"Node{i}", "concept", f"测试节点{i}")
            kg.add_node(node)
        
        # 查询 100 次
        import time
        start = time.time()
        
        for i in range(100):
            kg.get_node(f"kg_node{i}_xxx")
        
        elapsed = (time.time() - start) / 100
        
        # 要求：平均 < 5ms
        self.assertLess(elapsed, 0.005, f"查询超时：{elapsed*1000:.2f}ms")


# ============================================================
# 测试运行
# ============================================================

if __name__ == '__main__':
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeGraph))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryConsolidation))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryLinking))
    suite.addTests(loader.loadTestsFromTestCase(TestExceptions))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果
    print()
    print("=" * 60)
    print(f"  测试完成：{result.testsRun} 个测试")
    print(f"  成功：{result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  失败：{len(result.failures)}")
    print(f"  错误：{len(result.errors)}")
    print("=" * 60)
    
    # 退出码
    sys.exit(0 if result.wasSuccessful() else 1)
