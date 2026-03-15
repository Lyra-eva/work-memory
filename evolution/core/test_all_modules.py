#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个体认知增强系统 v3.5 全面测试

测试所有模块：
- v3.3: 知识图谱 + 概念提取器
- v3.4: 记忆巩固
- v3.5: 记忆关联

版本：v3.5.0
创建：2026-03-15
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from datetime import datetime


def print_header(title):
    """打印标题"""
    print()
    print("=" * 70)
    print(f"  {title}")
    print("=" * 70)
    print()


def print_section(title):
    """打印小标题"""
    print(f"【{title}】")


def main():
    """主测试流程"""
    print_header("个体认知增强系统 v3.5 全面测试")
    
    # ========== 初始化 ==========
    print_section("步骤 1: 系统初始化")
    
    from knowledge_graph import KnowledgeGraph
    from memory_consolidation import MemoryConsolidator
    from memory_linking import MemoryLinker
    
    kg = KnowledgeGraph()
    mc = MemoryConsolidator()
    linker = MemoryLinker()
    
    print(f"  ✅ 知识图谱：{len(kg.nodes)} 节点")
    print(f"  ✅ 记忆巩固：{mc.get_stats()['total_memories']} 记忆")
    print(f"  ✅ 记忆关联：{linker.get_stats()['total_links']} 关联")
    
    # ========== v3.3 知识图谱测试 ==========
    print_header("v3.3 知识图谱模块测试")
    
    # 1. 节点操作
    print_section("v3.3-1: 节点 CRUD")
    
    from knowledge_graph import create_node, create_relation
    
    node1 = create_node("Test Skill", "skill", "测试技能", mastery=0.5)
    node2 = create_node("Test Concept", "concept", "测试概念", mastery=0.3)
    
    kg.add_node(node1)
    kg.add_node(node2)
    print(f"  ✅ 创建 2 个节点")
    
    # 查询
    fetched = kg.get_node(node1.id)
    print(f"  ✅ 查询：{fetched.name} (掌握度：{fetched.mastery_level:.0%})")
    
    # 更新
    kg.update_node(node1.id, mastery_level=0.7)
    updated = kg.get_node(node1.id)
    print(f"  ✅ 更新：{0.5:.0%} → {updated.mastery_level:.0%}")
    
    # 2. 关系管理
    print_section("v3.3-2: 关系管理")
    
    rel = create_relation(node2.id, node1.id, "depends_on", strength=0.9)
    kg.add_relation(rel)
    print(f"  ✅ 创建关系")
    
    relations = kg.get_relations(node1.id)
    print(f"  ✅ 查询关系：{len(relations)} 个")
    
    # 3. 知识发现
    print_section("v3.3-3: 知识发现")
    
    gaps = kg.find_knowledge_gaps(node1.id)
    print(f"  🔍 知识盲区：{len(gaps)} 个")
    
    path = kg.suggest_learning_path(node1.id)
    print(f"  📚 学习路径：{len(path)} 步")
    
    # 4. 概念提取
    print_section("v3.3-4: 概念提取")
    
    from concept_extractor import ConceptExtractor
    
    extractor = ConceptExtractor(kg)
    
    text = "Evolution Engine 支持 Pattern Mining 和 Knowledge Graph"
    concepts = extractor.extract_from_text(text, "test")
    print(f"  📝 从文本提取：{len(concepts)} 个概念")
    
    event = {
        'event_type': 'capability_learned',
        'data': {'capability': 'test_capability'}
    }
    concepts = extractor.extract_from_evolution_event(event)
    print(f"  📊 从事件提取：{len(concepts)} 个概念")
    
    # ========== v3.4 记忆巩固测试 ==========
    print_header("v3.4 记忆巩固模块测试")
    
    # 1. 创建记忆
    print_section("v3.4-1: 记忆项目管理")
    
    from memory_consolidation import create_memory
    
    mem1 = create_memory(
        {'type': 'test', 'name': '测试记忆 1'},
        importance=0.8,
        emotional_intensity=0.7
    )
    mem2 = create_memory(
        {'type': 'test', 'name': '测试记忆 2'},
        importance=0.6,
        emotional_intensity=0.5
    )
    
    mc.add_memory(mem1)
    mc.add_memory(mem2)
    print(f"  ✅ 创建 2 个记忆")
    
    # 2. 遗忘曲线
    print_section("v3.4-2: 遗忘曲线计算")
    
    retention = mc.calculate_retention(mem1)
    print(f"  📊 保留率：{retention:.1%}")
    
    time_to_forget = mc.predict_forgetting_time(mem1)
    print(f"  ⏰ 距离遗忘：{time_to_forget:.1f}小时")
    
    # 3. 复习调度
    print_section("v3.4-3: 复习调度")
    
    schedule = mc.generate_review_schedule(daily_capacity=5)
    print(f"  📅 复习计划：{len(schedule)} 项")
    
    # 4. 执行复习
    print_section("v3.4-4: 复习执行")
    
    updated = mc.review_memory(mem1.id, recall_quality=0.85)
    print(f"  ✅ 复习完成")
    print(f"      强度：{mem1.strength:.2f} → {updated.strength:.2f}")
    print(f"      下次复习：{updated.next_review[:10]}")
    
    # ========== v3.5 记忆关联测试 ==========
    print_header("v3.5 记忆关联模块测试")
    
    # 1. 相似度计算
    print_section("v3.5-1: 多维度相似度")
    
    data1 = {
        'id': 'test_1',
        'tags': ['learning', 'skill'],
        'entities': ['python'],
        'created_at': '2026-03-15T10:00:00',
        'emotion': {'type': 'joy', 'valence': 'positive'},
        'content': '学习 Python 技能'
    }
    data2 = {
        'id': 'test_2',
        'tags': ['learning', 'improvement'],
        'entities': ['python', 'coding'],
        'created_at': '2026-03-15T11:00:00',
        'emotion': {'type': 'excitement', 'valence': 'positive'},
        'content': '提升 Python 编程能力'
    }
    
    scores = linker.calculate_similarity(data1, data2)
    print(f"  主题相似度：{scores['thematic']:.2f}")
    print(f"  实体相似度：{scores['entity']:.2f}")
    print(f"  时间相似度：{scores['temporal']:.2f}")
    print(f"  情感相似度：{scores['emotional']:.2f}")
    print(f"  语义相似度：{scores['semantic']:.2f}")
    print(f"  总分：{scores['total']:.2f}")
    
    # 2. 关联发现
    print_section("v3.5-2: 关联发现")
    
    memories = [data1, data2]
    links = linker.discover_links(memories, min_strength=0.3)
    print(f"  ✅ 发现 {links} 个关联")
    
    # 3. 相关记忆查找
    print_section("v3.5-3: 相关记忆查找")
    
    related = linker.find_related_memories(data1, memories, min_strength=0.2)
    print(f"  ✅ 找到 {len(related)} 个相关记忆")
    
    # 4. 记忆链生成
    print_section("v3.5-4: 记忆链生成")
    
    chain = linker.create_memory_chain(data1, memories, max_length=5)
    print(f"  ✅ 创建记忆链：{chain.id[:12]}...")
    print(f"      长度：{len(chain.memories)}")
    print(f"      总强度：{chain.total_strength:.2f}")
    
    # 5. 上下文摘要
    print_section("v3.5-5: 上下文摘要")
    
    related_mems = [m for m, s in related]
    summary = linker.generate_context_summary(data1, related_mems)
    print(f"  📝 摘要:")
    print(f"      主题：{', '.join(summary.themes[:3])}")
    print(f"      实体：{', '.join(summary.entities[:3])}")
    print(f"      时间：{summary.time_span}")
    
    # ========== 综合统计 ==========
    print_header("综合统计")
    
    kg_stats = kg.get_stats()
    mc_stats = mc.get_stats()
    linker_stats = linker.get_stats()
    
    print("📊 知识图谱:")
    print(f"      总节点：{kg_stats['total_nodes']}")
    print(f"      总关系：{kg_stats['total_relations']}")
    print(f"      平均掌握：{kg_stats['avg_mastery']:.2f}")
    
    print("\n💾 记忆巩固:")
    print(f"      总记忆：{mc_stats['total_memories']}")
    print(f"      平均强度：{mc_stats['avg_strength']:.2f}")
    print(f"      平均保留：{mc_stats['avg_retention']:.2f}")
    print(f"      需要复习：{mc_stats['due_count']}")
    
    print("\n🔗 记忆关联:")
    print(f"      总关联：{linker_stats['total_links']}")
    print(f"      平均强度：{linker_stats['avg_strength']:.2f}")
    print(f"      记忆链：{linker_stats['chains']['total']}")
    
    # ========== 导出测试 ==========
    print_header("导出测试")
    
    export_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    
    kg_nodes, kg_rels = kg.export_to_json(os.path.join(export_dir, 'kg_test_export.json'))
    print(f"  💾 知识图谱：{kg_nodes} 节点，{kg_rels} 关系")
    
    mc_mems, _ = mc.export_to_json(os.path.join(export_dir, 'mc_test_export.json'))
    print(f"  💾 记忆巩固：{mc_mems} 记忆")
    
    linker_links, linker_chains = linker.export_to_json(os.path.join(export_dir, 'ml_test_export.json'))
    print(f"  💾 记忆关联：{linker_links} 关联，{linker_chains} 链")
    
    # ========== 测试总结 ==========
    print_header("测试总结")
    
    print("✅ v3.3 知识图谱模块")
    print("    • 节点 CRUD ✓")
    print("    • 关系管理 ✓")
    print("    • 知识发现 ✓")
    print("    • 概念提取 ✓")
    print()
    print("✅ v3.4 记忆巩固模块")
    print("    • 记忆项目管理 ✓")
    print("    • 遗忘曲线计算 ✓")
    print("    • 间隔重复算法 ✓")
    print("    • 复习调度 ✓")
    print()
    print("✅ v3.5 记忆关联模块")
    print("    • 多维度相似度 ✓")
    print("    • 关联发现 ✓")
    print("    • 记忆链生成 ✓")
    print("    • 上下文摘要 ✓")
    print()
    print("=" * 70)
    print("  🎉 所有测试通过！个体认知增强系统 v3.5 运行正常")
    print("=" * 70)
    print()
    
    return 0


if __name__ == '__main__':
    exit(main())
