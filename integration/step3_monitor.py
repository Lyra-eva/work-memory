#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤 3: 监控效果 - 查看进化决策质量
"""

import sqlite3
import json
import os

print("=" * 70)
print("📊 步骤 3: 监控效果")
print("=" * 70)

GRAPH_DB = '/home/admin/.openclaw/workspace/memory/cognition/graph.db'

print("\n【3.1】连接图谱数据库...")
conn = sqlite3.connect(GRAPH_DB)
cursor = conn.cursor()
print(f"  ✓ 数据库：{GRAPH_DB}")

print("\n【3.2】图谱整体统计...")
cursor.execute("SELECT COUNT(*) FROM nodes")
total_nodes = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM edges")
total_edges = cursor.fetchone()[0]

print(f"  总节点数：{total_nodes}")
print(f"  总关系数：{total_edges}")
print(f"  图谱密度：{total_edges / max(total_nodes, 1):.2f}")

print("\n【3.3】节点类型分布...")
cursor.execute("""
    SELECT node_type, COUNT(*) as count 
    FROM nodes 
    GROUP BY node_type 
    ORDER BY count DESC
""")
nodes_by_type = cursor.fetchall()

for node_type, count in nodes_by_type:
    percentage = count / total_nodes * 100
    bar = '█' * int(percentage / 5)
    print(f"  {node_type:15} {count:3} ({percentage:5.1f}%) {bar}")

print("\n【3.4】关系类型分布...")
cursor.execute("""
    SELECT relation_type, COUNT(*) as count 
    FROM edges 
    GROUP BY relation_type 
    ORDER BY count DESC
""")
edges_by_type = cursor.fetchall()

if edges_by_type:
    for rel_type, count in edges_by_type:
        percentage = count / total_edges * 100
        bar = '█' * int(percentage / 5)
        print(f"  {rel_type:15} {count:3} ({percentage:5.1f}%) {bar}")
else:
    print("  ⚠️ 暂无关系数据")

print("\n【3.5】决策节点分析...")
cursor.execute("""
    SELECT COUNT(*) FROM nodes WHERE node_type = 'Decision'
""")
decision_count = cursor.fetchone()[0]

if decision_count > 0:
    cursor.execute("""
        SELECT json_extract(properties, '$.decision_type') as type, COUNT(*) as count
        FROM nodes
        WHERE node_type = 'Decision'
        GROUP BY type
        ORDER BY count DESC
    """)
    decisions_by_type = cursor.fetchall()
    
    print(f"  决策总数：{decision_count}")
    print(f"  决策类型分布:")
    for dec_type, count in decisions_by_type:
        percentage = count / decision_count * 100
        bar = '█' * int(percentage / 5)
        print(f"    {dec_type:15} {count:3} ({percentage:5.1f}%) {bar}")
else:
    print(f"  决策总数：0 (需要更多进化事件)")

print("\n【3.6】进化事件趋势...")
cursor.execute("""
    SELECT json_extract(properties, '$.event_type') as type, COUNT(*) as count
    FROM nodes
    WHERE node_type = 'Event'
    GROUP BY type
    ORDER BY count DESC
""")
events_by_type = cursor.fetchall()

print(f"  事件总数：{sum(count for _, count in events_by_type)}")
print(f"  事件类型分布:")
for event_type, count in events_by_type:
    percentage = count / sum(c for _, c in events_by_type) * 100
    bar = '█' * int(percentage / 5)
    print(f"    {event_type:25} {count:3} ({percentage:5.1f}%) {bar}")

print("\n【3.7】情绪分析效果...")
cursor.execute("""
    SELECT 
        AVG(json_extract(properties, '$.emotional_tone')) as avg_tone,
        MIN(json_extract(properties, '$.emotional_tone')) as min_tone,
        MAX(json_extract(properties, '$.emotional_tone')) as max_tone
    FROM nodes
    WHERE node_type = 'Event'
    AND json_extract(properties, '$.emotional_tone') IS NOT NULL
""")
emotion_stats = cursor.fetchone()

if emotion_stats[0] is not None:
    avg_tone, min_tone, max_tone = emotion_stats
    print(f"  平均情绪极性：{avg_tone:.2f}")
    print(f"  最小情绪极性：{min_tone:.2f}")
    print(f"  最大情绪极性：{max_tone:.2f}")
    
    if avg_tone > 0.3:
        print(f"  ✓ 情绪偏正面 (进化引擎工作正常)")
    elif avg_tone < -0.3:
        print(f"  ⚠️ 情绪偏负面 (可能需要优化)")
    else:
        print(f"  ✓ 情绪中性 (正常)")
else:
    print(f"  ⚠️ 暂无情绪数据")

print("\n【3.8】意图分类效果...")
cursor.execute("""
    SELECT 
        json_extract(properties, '$.user_intent') as intent,
        COUNT(*) as count
    FROM nodes
    WHERE node_type = 'Event'
    AND json_extract(properties, '$.user_intent') IS NOT NULL
    GROUP BY intent
    ORDER BY count DESC
""")
intents = cursor.fetchall()

if intents:
    print(f"  意图分类统计:")
    for intent, count in intents:
        percentage = count / sum(c for _, c in intents) * 100
        bar = '█' * int(percentage / 10)
        print(f"    {intent:15} {count:3} ({percentage:5.1f}%) {bar}")
else:
    print(f"  ⚠️ 暂无意图数据")

print("\n【3.9】执行性能统计...")
cursor.execute("""
    SELECT 
        AVG(json_extract(properties, '$.execution_time')) as avg_time,
        MIN(json_extract(properties, '$.execution_time')) as min_time,
        MAX(json_extract(properties, '$.execution_time')) as max_time
    FROM nodes
    WHERE node_type = 'Decision'
    AND json_extract(properties, '$.execution_time') IS NOT NULL
""")
perf_stats = cursor.fetchone()

avg_time = None
if perf_stats[0] is not None:
    avg_time, min_time, max_time = perf_stats
    print(f"  平均执行时间：{avg_time*1000:.2f}ms")
    print(f"  最小执行时间：{min_time*1000:.2f}ms")
    print(f"  最大执行时间：{max_time*1000:.2f}ms")
    
    if avg_time < 0.1:  # 100ms
        print(f"  ✓ 性能优秀 (<100ms)")
    elif avg_time < 0.5:
        print(f"  ✓ 性能良好 (<500ms)")
    else:
        print(f"  ⚠️ 性能待优化 (>500ms)")
else:
    print(f"  ⚠️ 暂无性能数据")

print("\n【3.10】质量评估...")

# 计算质量分数
quality_score = 0
max_score = 100

# 图谱密度 (20 分)
density = total_edges / max(total_nodes, 1)
if density >= 0.5:
    quality_score += 20
elif density >= 0.3:
    quality_score += 15
elif density >= 0.1:
    quality_score += 10

# 决策多样性 (20 分)
if decision_count >= 5:
    quality_score += 20
elif decision_count >= 2:
    quality_score += 15

# 情绪分析覆盖 (20 分)
cursor.execute("SELECT COUNT(*) FROM nodes WHERE node_type = 'Event' AND json_extract(properties, '$.emotional_tone') IS NOT NULL")
emotion_coverage = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM nodes WHERE node_type = 'Event'")
total_events = cursor.fetchone()[0]
if total_events > 0:
    coverage_rate = emotion_coverage / total_events
    if coverage_rate >= 0.8:
        quality_score += 20
    elif coverage_rate >= 0.5:
        quality_score += 15
    elif coverage_rate >= 0.3:
        quality_score += 10

# 意图分类覆盖 (20 分)
cursor.execute("SELECT COUNT(*) FROM nodes WHERE node_type = 'Event' AND json_extract(properties, '$.user_intent') IS NOT NULL")
intent_coverage = cursor.fetchone()[0]
if total_events > 0:
    intent_rate = intent_coverage / total_events
    if intent_rate >= 0.8:
        quality_score += 20
    elif intent_rate >= 0.5:
        quality_score += 15
    elif intent_rate >= 0.3:
        quality_score += 10

# 执行性能 (20 分)
if perf_stats[0] is not None:
    if avg_time < 0.1:
        quality_score += 20
    elif avg_time < 0.5:
        quality_score += 15
    elif avg_time < 1.0:
        quality_score += 10

# 显示质量分数
print(f"  图谱密度：     {'✅' if density >= 0.3 else '⚠️'}  ({density:.2f})")
print(f"  决策多样性：   {'✅' if decision_count >= 3 else '⚠️'}  ({decision_count} 种)")
print(f"  情绪分析覆盖： {'✅' if total_events > 0 and emotion_coverage/total_events >= 0.5 else '⚠️'}  ({emotion_coverage}/{total_events})")
print(f"  意图分类覆盖： {'✅' if total_events > 0 and intent_coverage/total_events >= 0.5 else '⚠️'}  ({intent_coverage}/{total_events})")
if avg_time is not None:
    print(f"  执行性能：     {'✅' if avg_time < 0.5 else '⚠️'}  ({avg_time*1000:.2f}ms)")
else:
    print(f"  执行性能：     ⚠️  (暂无数据)")

print(f"\n  {'=' * 40}")
print(f"  质量总分：{quality_score}/{max_score}")

if quality_score >= 80:
    print(f"  评级：⭐⭐⭐⭐⭐ 优秀")
elif quality_score >= 60:
    print(f"  评级：⭐⭐⭐⭐ 良好")
elif quality_score >= 40:
    print(f"  评级：⭐⭐⭐ 中等")
else:
    print(f"  评级：⭐⭐ 待改进")

conn.close()

print("\n" + "=" * 70)
print("✅ 步骤 3 完成：效果监控完成")
print("=" * 70)

print("\n📋 改进建议:")
print("-" * 70)
if density < 0.3:
    print("  1. 建立更多图谱关系 (运行 build_relations.py)")
if decision_count < 3:
    print("  2. 增加进化事件触发频率")
if total_events > 0 and emotion_coverage/total_events < 0.5:
    print("  3. 确保事件包含 message 字段用于情绪分析")
if total_events > 0 and intent_coverage/total_events < 0.5:
    print("  4. 确保事件类型正确用于意图分类")
if avg_time is not None and avg_time >= 0.5:
    print("  5. 优化图谱查询性能")

if density >= 0.3 and decision_count >= 3 and (avg_time is None or avg_time < 0.5):
    print("  ✅ 所有指标正常，无需改进")
