#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆巩固演示脚本

展示完整的记忆管理工作流程：
1. 从进化事件创建记忆
2. 计算遗忘曲线
3. 生成复习计划
4. 执行复习
5. 查看效果

版本：v3.4.0
创建：2026-03-15
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from datetime import datetime
from knowledge_graph import KnowledgeGraph
from memory_consolidation import MemoryConsolidator, create_memory


def main():
    """演示主流程"""
    print()
    print("╔" + "═" * 60 + "╗")
    print("║" + " " * 18 + "记忆巩固系统演示" + " " * 24 + "║")
    print("║" + " " * 22 + "v3.4.0" + " " * 32 + "║")
    print("╚" + "═" * 60 + "╝")
    print()
    
    # 初始化
    print("【步骤 1】初始化系统")
    kg = KnowledgeGraph()
    mc = MemoryConsolidator()
    print(f"  ✅ 知识图谱：{len(kg.nodes)} 节点")
    print(f"  ✅ 记忆系统：{mc.get_stats()['total_memories']} 记忆")
    print()
    
    # 从进化事件创建记忆
    print("【步骤 2】从进化事件创建记忆")
    
    events = [
        {
            'event_type': 'capability_learned',
            'data': {
                'capability': 'web_search',
                'description': '网络搜索能力',
                'success': True
            }
        },
        {
            'event_type': 'skill_improved',
            'data': {
                'skill': 'image_analysis',
                'version': '2.0.0',
                'accuracy': 0.92
            }
        },
        {
            'event_type': 'pattern_discovered',
            'data': {
                'pattern': 'error_recovery',
                'confidence': 0.85
            }
        }
    ]
    
    for event in events:
        # 创建记忆
        memory = create_memory(
            content={
                'type': 'evolution_event',
                'event_type': event['event_type'],
                'data': event['data']
            },
            importance=0.8 if event['event_type'] == 'capability_learned' else 0.6,
            emotional_intensity=0.7
        )
        mc.add_memory(memory)
        print(f"  ✅ 创建记忆：{event['event_type']}")
    
    print()
    
    # 查看记忆状态
    print("【步骤 3】查看记忆状态")
    stats = mc.get_stats()
    print(f"  📊 统计信息:")
    print(f"      总记忆数：{stats['total_memories']}")
    print(f"      平均强度：{stats['avg_strength']:.2f}")
    print(f"      平均保留：{stats['avg_retention']:.2f}")
    print(f"      高重要性：{stats['by_importance']['high']}")
    print()
    
    # 生成复习计划
    print("【步骤 4】生成复习计划")
    schedule = mc.generate_review_schedule(daily_capacity=5)
    print(f"  📅 今日复习计划 ({len(schedule)} 项):")
    
    for i, item in enumerate(schedule, 1):
        mem = mc.get_memory(item.memory_id)
        event_type = mem.content.get('event_type', 'unknown')
        print(f"      {i}. [{item.review_type}] {event_type}")
        print(f"         优先级：{item.priority:.2f}, 预计：{item.estimated_duration}分钟")
    
    print()
    
    # 模拟复习
    print("【步骤 5】模拟复习过程")
    
    memories = mc.list_memories()[:3]
    for mem in memories:
        event_type = mem.content.get('event_type', 'unknown')
        
        # 复习前
        retention_before = mc.calculate_retention(mem)
        
        # 模拟回忆质量
        import random
        quality = random.uniform(0.6, 0.95)
        
        # 执行复习
        updated = mc.review_memory(mem.id, quality)
        
        # 复习后
        retention_after = mc.calculate_retention(updated)
        
        print(f"  📝 {event_type}:")
        print(f"      回忆质量：{quality:.0%}")
        print(f"      保留率：{retention_before:.0%} → {retention_after:.0%}")
        print(f"      强度：{mem.strength:.2f} → {updated.strength:.2f}")
        print(f"      下次复习：{updated.next_review[:10]}")
        print()
    
    # 最终统计
    print("【步骤 6】最终统计")
    final_stats = mc.get_stats()
    print(f"  📈 效果对比:")
    print(f"      平均强度：{stats['avg_strength']:.2f} → {final_stats['avg_strength']:.2f}")
    print(f"      平均保留：{stats['avg_retention']:.2f} → {final_stats['avg_retention']:.2f}")
    print(f"      总复习次数：{final_stats['total_reviews']}")
    print()
    
    # 导出
    print("【步骤 7】导出数据")
    export_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              'data', 'memory_demo.json')
    memories, _ = mc.export_to_json(export_path)
    print(f"  💾 导出 {memories} 个记忆 → {export_path}")
    print()
    
    print("=" * 60)
    print("✅ 演示完成！")
    print("=" * 60)
    print()
    
    return 0


if __name__ == '__main__':
    exit(main())
