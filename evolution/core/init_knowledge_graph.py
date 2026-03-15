#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱初始化脚本

从现有进化事件中提取概念
构建初始知识图谱

版本：v3.3.0
创建：2026-03-15
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from datetime import datetime
from knowledge_graph import KnowledgeGraph, create_node, create_relation
from concept_extractor import ConceptExtractor


# ============================================================
# 配置
# ============================================================

WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")
EVOLUTION_DIR = os.path.join(WORKSPACE_DIR, 'evolution')
DATA_DIR = os.path.join(EVOLUTION_DIR, 'data')
EVENTS_FILE = os.path.join(DATA_DIR, 'events.jsonl')
CAPABILITIES_DIR = os.path.join(EVOLUTION_DIR, 'capabilities')
KG_DB_PATH = os.path.join(DATA_DIR, 'knowledge_graph.db')


# ============================================================
# 主流程
# ============================================================

def load_evolution_events():
    """加载进化事件"""
    events = []
    
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        event = json.loads(line)
                        events.append(event)
                    except:
                        continue
    
    print(f"  ✅ 加载 {len(events)} 条进化事件")
    return events


def load_capabilities():
    """加载能力配置"""
    capabilities = []
    
    if os.path.exists(CAPABILITIES_DIR):
        for filename in os.listdir(CAPABILITIES_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(CAPABILITIES_DIR, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    cap = json.load(f)
                    capabilities.append(cap)
    
    print(f"  ✅ 加载 {len(capabilities)} 个能力配置")
    return capabilities


def build_knowledge_graph():
    """构建知识图谱"""
    print("=" * 60)
    print("🔨 开始构建知识图谱")
    print("=" * 60)
    print()
    
    # 1. 初始化
    print("【步骤 1】初始化知识图谱")
    kg = KnowledgeGraph(KG_DB_PATH)
    extractor = ConceptExtractor(kg)
    print(f"  数据库路径：{KG_DB_PATH}")
    print()
    
    # 2. 加载数据
    print("【步骤 2】加载进化数据")
    events = load_evolution_events()
    capabilities = load_capabilities()
    print()
    
    # 3. 从事件提取概念
    print("【步骤 3】从进化事件提取概念")
    all_concepts = []
    
    for event in events:
        concepts = extractor.extract_from_evolution_event(event)
        all_concepts.extend(concepts)
    
    print(f"  提取到 {len(all_concepts)} 个概念")
    
    # 去重
    unique_concepts = {}
    for c in all_concepts:
        key = c.name.lower()
        if key not in unique_concepts:
            unique_concepts[key] = c
    
    print(f"  去重后 {len(unique_concepts)} 个唯一概念")
    print()
    
    # 4. 整合概念
    print("【步骤 4】整合概念到知识图谱")
    integrated = extractor.integrate_concepts(list(unique_concepts.values()), min_confidence=0.6)
    print(f"  ✅ 整合 {integrated} 个概念")
    print()
    
    # 5. 从能力配置提取
    print("【步骤 5】从能力配置提取")
    for cap in capabilities:
        concepts = extractor.extract_from_capability(cap)
        extractor.integrate_concepts(concepts, min_confidence=0.7)
    
    print(f"  ✅ 处理 {len(capabilities)} 个能力")
    print()
    
    # 6. 创建核心关系
    print("【步骤 6】创建核心关系")
    
    # 找出所有 skill 和 concept 节点
    skills = [n for n in kg.nodes.values() if n.category == 'skill']
    concepts = [n for n in kg.nodes.values() if n.category == 'concept']
    
    # 为相关技能创建关系
    relations_created = 0
    for skill in skills:
        # 如果技能名称包含概念名称，创建 used_for 关系
        for concept in concepts:
            if concept.name.lower() in skill.name.lower():
                relation = create_relation(
                    source_id=concept.id,
                    target_id=skill.id,
                    relation_type='used_for',
                    strength=0.8,
                    evidence=['auto_discovered_from_name']
                )
                kg.add_relation(relation)
                relations_created += 1
    
    print(f"  ✅ 创建 {relations_created} 个关系")
    print()
    
    # 7. 统计信息
    print("【步骤 7】生成统计信息")
    stats = kg.get_stats()
    
    print(f"  📊 知识图谱统计:")
    print(f"      总节点数：{stats['total_nodes']}")
    print(f"      总关系数：{stats['total_relations']}")
    print(f"      平均掌握度：{stats['avg_mastery']:.2f}")
    print(f"      类别分布:")
    for cat, count in stats['by_category'].items():
        print(f"          {cat}: {count}")
    print()
    
    # 8. 导出
    print("【步骤 8】导出知识图谱")
    export_path = os.path.join(DATA_DIR, 'knowledge_graph.json')
    nodes, rels = kg.export_to_json(export_path)
    print(f"  ✅ 导出 {nodes} 节点，{rels} 关系 → {export_path}")
    print()
    
    # 9. 示例查询
    print("【步骤 9】示例查询")
    
    # 查找掌握度最低的节点（需要学习）
    nodes_sorted = sorted(kg.nodes.values(), key=lambda n: n.mastery_level)
    if nodes_sorted:
        print(f"  📚 需要加强的知识:")
        for node in nodes_sorted[:3]:
            print(f"      • {node.name} ({node.category}) - 掌握度：{node.mastery_level:.1%}")
    
    # 查找有关系的节点
    print(f"\n  🔗 有关系的节点:")
    for node in list(kg.nodes.values())[:3]:
        relations = kg.get_relations(node.id)
        if relations:
            print(f"      • {node.name}: {len(relations)} 个关系")
    
    print()
    print("=" * 60)
    print("✅ 知识图谱构建完成！")
    print("=" * 60)
    
    return kg


def main():
    """主函数"""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 15 + "知识图谱初始化脚本" + " " * 21 + "║")
    print("║" + " " * 18 + "v3.3.0" + " " * 34 + "║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    start_time = datetime.now()
    
    try:
        kg = build_knowledge_graph()
        
        elapsed = (datetime.now() - start_time).total_seconds()
        print(f"\n⏱️  总耗时：{elapsed:.2f}秒")
        print()
        
        # 保存统计
        stats_path = os.path.join(DATA_DIR, 'kg_init_stats.json')
        stats = {
            'init_time': start_time.isoformat(),
            'completion_time': datetime.now().isoformat(),
            'elapsed_seconds': elapsed,
            'stats': kg.get_stats()
        }
        
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"📄 初始化统计已保存：{stats_path}")
        print()
        
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
