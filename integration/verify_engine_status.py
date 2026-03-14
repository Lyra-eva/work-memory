#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进化引擎状态验证

验证内容:
1. 进化引擎是否正常工作
2. 进化前后能力对比
3. 使用情况统计
"""

import sqlite3
import json
import os
from datetime import datetime

print("=" * 70)
print("🔍 进化引擎状态验证")
print("=" * 70)

GRAPH_DB = '/home/admin/.openclaw/workspace/memory/cognition/graph.db'
CONFIG_FILE = '/home/admin/.openclaw/workspace/integration/evolution_config.json'

# ============================================================
# 1. 基础状态检查
# ============================================================
print("\n【1】基础状态检查")
print("-" * 70)

checks = []

# 检查 1: 图谱数据库
if os.path.exists(GRAPH_DB):
    checks.append(("图谱数据库", True, "存在"))
else:
    checks.append(("图谱数据库", False, "不存在"))

# 检查 2: 配置文件
if os.path.exists(CONFIG_FILE):
    checks.append(("配置文件", True, "存在"))
else:
    checks.append(("配置文件", False, "不存在"))

# 检查 3: 集成模块
if os.path.exists('/home/admin/.openclaw/workspace/integration/evolving_agent.py'):
    checks.append(("集成模块", True, "存在"))
else:
    checks.append(("集成模块", False, "不存在"))

# 检查 4: OODA 触发器
if os.path.exists('/home/admin/.openclaw/workspace/evolution-engine/examples/ooda_demo.py'):
    checks.append(("OODA 触发器", True, "存在"))
else:
    checks.append(("OODA 触发器", False, "不存在"))

# 显示检查结果
for name, passed, detail in checks:
    status = "✅" if passed else "❌"
    print(f"  {status} {name}: {detail}")

all_passed = all(passed for _, passed, _ in checks)
print(f"\n  基础状态：{'✅ 正常' if all_passed else '❌ 异常'}")

# ============================================================
# 2. 图谱数据统计
# ============================================================
print("\n【2】图谱数据统计")
print("-" * 70)

conn = sqlite3.connect(GRAPH_DB)
cursor = conn.cursor()

# 节点统计
cursor.execute("SELECT COUNT(*) FROM nodes")
total_nodes = cursor.fetchone()[0]
print(f"  总节点数：{total_nodes}")

# 关系统计
cursor.execute("SELECT COUNT(*) FROM edges")
total_edges = cursor.fetchone()[0]
print(f"  总关系数：{total_edges}")
print(f"  图谱密度：{total_edges / max(total_nodes, 1):.2f}")

# 节点类型分布
print(f"\n  节点类型分布:")
cursor.execute("""
    SELECT node_type, COUNT(*) as count 
    FROM nodes 
    GROUP BY node_type 
    ORDER BY count DESC
""")
for node_type, count in cursor.fetchall():
    percentage = count / total_nodes * 100
    bar = '█' * int(percentage / 5)
    print(f"    {node_type:15} {count:3} ({percentage:5.1f}%) {bar}")

# ============================================================
# 3. 进化能力对比
# ============================================================
print("\n【3】进化前后能力对比")
print("-" * 70)

# 获取能力节点
cursor.execute("""
    SELECT node_id, properties 
    FROM nodes 
    WHERE node_type = 'Capability'
""")
capabilities = cursor.fetchall()

print(f"  已掌握能力：{len(capabilities)} 个")
for node_id, props in capabilities:
    props = json.loads(props)
    name = props.get('name', 'unknown')
    version = props.get('version', '1.0.0')
    success_rate = props.get('success_rate', 'N/A')
    print(f"    - {name} v{version} (成功率：{success_rate})")

# 获取进化事件
cursor.execute("""
    SELECT json_extract(properties, '$.event_type') as type, COUNT(*) as count
    FROM nodes
    WHERE node_type = 'Event'
    GROUP BY type
    ORDER BY count DESC
""")
events = cursor.fetchall()

print(f"\n  进化事件统计:")
total_events = sum(count for _, count in events)
for event_type, count in events:
    percentage = count / total_events * 100 if total_events > 0 else 0
    bar = '█' * int(percentage / 5)
    print(f"    {event_type:25} {count:2} ({percentage:5.1f}%) {bar}")

# ============================================================
# 4. 决策质量分析
# ============================================================
print("\n【4】决策质量分析")
print("-" * 70)

# 获取决策节点
cursor.execute("""
    SELECT json_extract(properties, '$.decision_type') as type, COUNT(*) as count
    FROM nodes
    WHERE node_type = 'Decision'
    GROUP BY type
    ORDER BY count DESC
""")
decisions = cursor.fetchall()

total_decisions = sum(count for _, count in decisions)
print(f"  总决策数：{total_decisions}")

if total_decisions > 0:
    print(f"\n  决策类型分布:")
    for dec_type, count in decisions:
        percentage = count / total_decisions * 100
        bar = '█' * int(percentage / 5)
        print(f"    {dec_type:15} {count:3} ({percentage:5.1f}%) {bar}")
    
    # 决策质量评估
    evolve_count = sum(count for dec_type, count in decisions if dec_type == 'evolve')
    optimize_count = sum(count for dec_type, count in decisions if dec_type == 'optimize')
    maintain_count = sum(count for dec_type, count in decisions if dec_type == 'maintain')
    
    # 健康决策分布：evolve 40-60%, optimize 10-30%, maintain 20-40%
    evolve_ratio = evolve_count / total_decisions
    optimize_ratio = optimize_count / total_decisions
    maintain_ratio = maintain_count / total_decisions
    
    print(f"\n  决策质量评估:")
    
    if 0.4 <= evolve_ratio <= 0.7:
        print(f"    ✅ 进化决策比例合理 ({evolve_ratio:.0%})")
    elif evolve_ratio > 0.7:
        print(f"    ⚠️ 进化决策过多 ({evolve_ratio:.0%}),可能过于激进")
    else:
        print(f"    ⚠️ 进化决策过少 ({evolve_ratio:.0%}),可能过于保守")
    
    if optimize_ratio >= 0.1:
        print(f"    ✅ 优化决策正常 ({optimize_ratio:.0%})")
    else:
        print(f"    ⚠️ 优化决策偏少 ({optimize_ratio:.0%})")

# ============================================================
# 5. 情绪和意图分析
# ============================================================
print("\n【5】情绪和意图分析")
print("-" * 70)

# 情绪统计
cursor.execute("""
    SELECT 
        AVG(json_extract(properties, '$.emotional_tone')) as avg_tone,
        MIN(json_extract(properties, '$.emotional_tone')) as min_tone,
        MAX(json_extract(properties, '$.emotional_tone')) as max_tone,
        COUNT(*) as count
    FROM nodes
    WHERE node_type = 'Event'
    AND json_extract(properties, '$.emotional_tone') IS NOT NULL
""")
emotion_stats = cursor.fetchone()

if emotion_stats[0] is not None:
    avg_tone, min_tone, max_tone, count = emotion_stats
    print(f"  情绪数据统计:")
    print(f"    平均极性：{avg_tone:.2f}")
    print(f"    最小极性：{min_tone:.2f}")
    print(f"    最大极性：{max_tone:.2f}")
    print(f"    覆盖数量：{count}")
    
    if avg_tone > 0.5:
        print(f"    ✅ 整体情绪正面 (进化引擎工作正常)")
    elif avg_tone > 0:
        print(f"    ✅ 整体情绪中性偏正面")
    else:
        print(f"    ⚠️ 整体情绪偏负面 (可能需要关注)")
else:
    print(f"  ⚠️ 无情绪数据")

# 意图统计
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
    print(f"\n  意图分布:")
    total_intents = sum(count for _, count in intents)
    for intent, count in intents:
        percentage = count / total_intents * 100
        bar = '█' * int(percentage / 10)
        print(f"    {intent:15} {count:3} ({percentage:5.1f}%) {bar}")
    
    # 意图多样性评估
    if len(intents) >= 3:
        print(f"    ✅ 意图类型丰富 ({len(intents)} 种)")
    else:
        print(f"    ⚠️ 意图类型单一 ({len(intents)} 种)")
else:
    print(f"  ⚠️ 无意图数据")

# ============================================================
# 6. 使用情况统计
# ============================================================
print("\n【6】使用情况统计")
print("-" * 70)

# 时间线分析
cursor.execute("""
    SELECT 
        DATE(created_at) as date,
        COUNT(*) as count
    FROM nodes
    WHERE node_type = 'Decision'
    GROUP BY DATE(created_at)
    ORDER BY date DESC
    LIMIT 7
""")
daily_decisions = cursor.fetchall()

if daily_decisions:
    print(f"  近 7 天决策趋势:")
    for date, count in daily_decisions:
        bar = '█' * min(count, 20)
        print(f"    {date}: {count:2} {bar}")
else:
    print(f"  ⚠️ 无决策时间数据")

# 使用频率
cursor.execute("""
    SELECT MIN(created_at), MAX(created_at)
    FROM nodes
    WHERE node_type = 'Decision'
""")
time_range = cursor.fetchone()

if time_range[0] and time_range[1]:
    first_use = time_range[0]
    last_use = time_range[1]
    print(f"\n  使用时间:")
    print(f"    首次使用：{first_use}")
    print(f"    最后使用：{last_use}")
    print(f"    ✅ 进化引擎已投入使用")

# ============================================================
# 7. 综合健康评分
# ============================================================
print("\n【7】综合健康评分")
print("-" * 70)

score = 0
max_score = 100

# 基础检查 (20 分)
if all_passed:
    score += 20
    print(f"  基础检查：     ✅ +20 分")
else:
    print(f"  基础检查：     ⚠️ +0 分")

# 图谱密度 (15 分)
density = total_edges / max(total_nodes, 1)
if density >= 0.3:
    score += 15
    print(f"  图谱密度：     ✅ +15 分 ({density:.2f})")
elif density >= 0.15:
    score += 10
    print(f"  图谱密度：     ⚠️ +10 分 ({density:.2f})")
else:
    print(f"  图谱密度：     ⚠️ +5 分 ({density:.2f})")

# 数据完整性 (20 分)
cursor.execute("SELECT COUNT(*) FROM nodes WHERE node_type = 'Event' AND json_extract(properties, '$.emotional_tone') IS NOT NULL")
emotion_count = cursor.fetchone()[0]
cursor.execute("SELECT COUNT(*) FROM nodes WHERE node_type = 'Event'")
event_count = cursor.fetchone()[0]
emotion_coverage = emotion_count / event_count if event_count > 0 else 0

if emotion_coverage >= 0.9:
    score += 20
    print(f"  数据完整性：   ✅ +20 分 ({emotion_coverage:.0%})")
elif emotion_coverage >= 0.5:
    score += 15
    print(f"  数据完整性：   ⚠️ +15 分 ({emotion_coverage:.0%})")
else:
    print(f"  数据完整性：   ⚠️ +5 分 ({emotion_coverage:.0%})")

# 决策多样性 (15 分)
if len(decisions) >= 3:
    score += 15
    print(f"  决策多样性：   ✅ +15 分 ({len(decisions)} 种)")
elif len(decisions) >= 2:
    score += 10
    print(f"  决策多样性：   ⚠️ +10 分 ({len(decisions)} 种)")
else:
    print(f"  决策多样性：   ⚠️ +5 分 ({len(decisions)} 种)")

# 情绪健康 (15 分)
if emotion_stats[0] is not None and avg_tone > 0.5:
    score += 15
    print(f"  情绪健康：     ✅ +15 分 ({avg_tone:.2f})")
elif emotion_stats[0] is not None and avg_tone > 0:
    score += 10
    print(f"  情绪健康：     ⚠️ +10 分 ({avg_tone:.2f})")
else:
    print(f"  情绪健康：     ⚠️ +5 分")

# 使用活跃度 (15 分)
if total_decisions >= 10:
    score += 15
    print(f"  使用活跃度：   ✅ +15 分 ({total_decisions} 次决策)")
elif total_decisions >= 5:
    score += 10
    print(f"  使用活跃度：   ⚠️ +10 分 ({total_decisions} 次决策)")
else:
    print(f"  使用活跃度：   ⚠️ +5 分 ({total_decisions} 次决策)")

print(f"\n  {'=' * 40}")
print(f"  综合评分：{score}/{max_score}")

if score >= 80:
    print(f"  评级：⭐⭐⭐⭐⭐ 优秀")
elif score >= 60:
    print(f"  评级：⭐⭐⭐⭐ 良好")
elif score >= 40:
    print(f"  评级：⭐⭐⭐ 中等")
else:
    print(f"  评级：⭐⭐ 待改进")

conn.close()

print("\n" + "=" * 70)
print("✅ 验证完成")
print("=" * 70)

# 总结
print("\n📋 验证总结:")
print("-" * 70)
if score >= 60:
    print("  ✅ 进化引擎状态正常")
    print(f"  ✅ 已掌握 {len(capabilities)} 个能力")
    print(f"  ✅ 已执行 {total_decisions} 次进化决策")
    print(f"  ✅ 数据完整性 {emotion_coverage:.0%}")
    print(f"  ✅ 综合评分 {score}/{max_score}")
else:
    print("  ⚠️ 进化引擎需要优化")
    print(f"  当前评分：{score}/{max_score}")
