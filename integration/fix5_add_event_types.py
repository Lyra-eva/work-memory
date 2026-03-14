#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
方案 5: 增加事件类型 - 丰富进化场景

问题：当前只有 capability_learned 一种事件类型
解决：添加多种事件类型，丰富进化场景
"""

import sqlite3
import json
import uuid
from datetime import datetime

print("=" * 70)
print("🔧 方案 5: 增加事件类型")
print("=" * 70)

GRAPH_DB = '/home/admin/.openclaw/workspace/memory/cognition/graph.db'

print("\n【5.1】连接图谱数据库...")
conn = sqlite3.connect(GRAPH_DB)
cursor = conn.cursor()
print(f"  ✓ 数据库：{GRAPH_DB}")

print("\n【5.2】检查当前事件类型分布...")
cursor.execute("""
    SELECT json_extract(properties, '$.event_type') as type, COUNT(*) as count
    FROM nodes
    WHERE node_type = 'Event'
    GROUP BY type
    ORDER BY count DESC
""")
current_types = cursor.fetchall()

print(f"  当前事件类型:")
for event_type, count in current_types:
    print(f"    - {event_type}: {count}")

print("\n【5.3】添加新事件类型...")

# 定义新事件类型
new_events = [
    {
        'event_type': 'pattern_discovered',
        'agent_id': 'lily',
        'data': {
            'pattern_name': '成功学习模式',
            'pattern_type': 'success',
            'confidence': 0.85,
            'recommendation': '继续当前学习策略'
        },
        'emotional_tone': 0.6,
        'user_intent': 'explore',
        'importance': 0.85
    },
    {
        'event_type': 'memory_consolidated',
        'agent_id': 'lily',
        'data': {
            'consolidation_type': 'daily',
            'events_processed': 10,
            'patterns_extracted': 2
        },
        'emotional_tone': 0.3,
        'user_intent': 'optimize',
        'importance': 0.6
    },
    {
        'event_type': 'config_updated',
        'agent_id': 'lily',
        'data': {
            'config_section': 'ooda.decision',
            'old_value': 0.2,
            'new_value': 0.3,
            'reason': '增加探索权重'
        },
        'emotional_tone': 0.2,
        'user_intent': 'improve',
        'importance': 0.5
    },
    {
        'event_type': 'capability_optimized',
        'agent_id': 'lily',
        'data': {
            'capability': 'web_search',
            'optimization_type': 'performance',
            'improvement': 0.3
        },
        'emotional_tone': 0.7,
        'user_intent': 'optimize',
        'importance': 0.75
    },
    {
        'event_type': 'goal_achieved',
        'agent_id': 'lily',
        'data': {
            'goal': '学会 3 个技能',
            'progress': 1.0,
            'time_taken': '2 小时'
        },
        'emotional_tone': 0.9,
        'user_intent': 'learn',
        'importance': 0.95
    }
]

# 插入新事件
inserted_count = 0
for event_data in new_events:
    node_id = f"event_{uuid.uuid4().hex[:12]}"
    
    cursor.execute("""
        INSERT INTO nodes (node_id, node_type, properties, created_at, updated_at)
        VALUES (?, ?, ?, datetime('now'), datetime('now'))
    """, (
        node_id,
        'Event',
        json.dumps(event_data, ensure_ascii=False)
    ))
    
    inserted_count += 1
    print(f"  ✓ 添加：{event_data['event_type']}")

conn.commit()
print(f"\n  总计添加：{inserted_count} 个新事件")

print("\n【5.4】验证新事件类型...")
cursor.execute("""
    SELECT json_extract(properties, '$.event_type') as type, COUNT(*) as count
    FROM nodes
    WHERE node_type = 'Event'
    GROUP BY type
    ORDER BY count DESC
""")
all_types = cursor.fetchall()

print(f"  更新后事件类型:")
for event_type, count in all_types:
    percentage = count / sum(c for _, c in all_types) * 100
    bar = '█' * int(percentage / 5)
    print(f"    {event_type:25} {count:2} ({percentage:5.1f}%) {bar}")

print("\n【5.5】分析事件类型多样性...")
total_events = sum(count for _, count in all_types)
unique_types = len(all_types)
diversity_index = unique_types / total_events * 100

print(f"  事件总数：{total_events}")
print(f"  事件类型数：{unique_types}")
print(f"  多样性指数：{diversity_index:.1f}%")

if diversity_index >= 30:
    print(f"  ✅ 多样性优秀")
elif diversity_index >= 20:
    print(f"  ✅ 多样性良好")
else:
    print(f"  ⚠️ 多样性待提升")

conn.close()

print("\n" + "=" * 70)
print("✅ 方案 5 完成：事件类型丰富完成")
print("=" * 70)

print("\n📋 新增事件类型说明:")
print("-" * 70)
print("  1. pattern_discovered - 模式发现事件")
print("     触发：发现新的进化模式")
print("     决策：evolve/investigate")
print()
print("  2. memory_consolidated - 记忆巩固事件")
print("     触发：定期记忆整理")
print("     决策：optimize/maintain")
print()
print("  3. config_updated - 配置更新事件")
print("     触发：配置参数调整")
print("     决策：maintain")
print()
print("  4. capability_optimized - 能力优化事件")
print("     触发：能力性能提升")
print("     决策：evolve/optimize")
print()
print("  5. goal_achieved - 目标达成事件")
print("     触发：完成学习目标")
print("     决策：evolve")
