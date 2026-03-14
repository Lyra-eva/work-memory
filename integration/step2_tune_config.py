#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
步骤 2: 调整参数 - 优化进化引擎配置
"""

import json
import os

print("=" * 70)
print("⚙️ 步骤 2: 调整参数")
print("=" * 70)

# 配置路径
CONFIG_DIR = '/home/admin/.openclaw/workspace/integration'
CONFIG_FILE = os.path.join(CONFIG_DIR, 'evolution_config.json')

# 默认配置
default_config = {
    "agent": {
        "default_agent_id": "lily",
        "enable_evolution": True,
        "auto_cleanup": True
    },
    "ooda": {
        "emotional_analysis": {
            "enabled": True,
            "sensitivity": 0.7,
            "positive_keywords": ["成功", "棒", "好", "太棒了", "excellent", "great"],
            "negative_keywords": ["失败", "错", "失望", "糟糕", "fail", "error"]
        },
        "intent_classification": {
            "enabled": True,
            "auto_detect": True
        },
        "decision": {
            "bandit_algorithm": "ucb1",
            "exploration_weight": 0.2,
            "risk_thresholds": {
                "low": 0.7,
                "medium": 0.4,
                "high": 0.0
            }
        }
    },
    "graph": {
        "storage_backend": "sqlite",
        "db_path": "/home/admin/.openclaw/workspace/memory/cognition/graph.db",
        "auto_create_relations": True,
        "relation_thresholds": {
            "similarity_min": 0.5,
            "dependency_auto_detect": False
        }
    },
    "logging": {
        "level": "INFO",
        "enable_detailed_output": True,
        "log_to_file": False,
        "log_path": "/home/admin/.openclaw/workspace/logs/evolution.log"
    },
    "performance": {
        "cache_enabled": True,
        "cache_ttl_seconds": 300,
        "batch_processing": False,
        "async_execution": False
    }
}

print("\n【2.1】创建配置文件...")

# 如果配置文件不存在，创建默认配置
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=2, ensure_ascii=False)
    print(f"  ✓ 创建配置文件：{CONFIG_FILE}")
else:
    print(f"  ✓ 配置文件已存在")

# 读取配置
with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    config = json.load(f)

print("\n【2.2】当前配置概览...")
print(f"  智能体 ID: {config['agent']['default_agent_id']}")
print(f"  进化启用：{config['agent']['enable_evolution']}")
print(f"  情绪分析：{config['ooda']['emotional_analysis']['enabled']}")
print(f"  意图分类：{config['ooda']['intent_classification']['enabled']}")
print(f"  Bandit 算法：{config['ooda']['decision']['bandit_algorithm']}")
print(f"  存储后端：{config['graph']['storage_backend']}")
print(f"  日志级别：{config['logging']['level']}")

print("\n【2.3】调整参数...")

# 优化建议
optimizations = {
    "ooda.emotional_analysis.sensitivity": {
        "old": 0.7,
        "new": 0.8,
        "reason": "提高情绪识别敏感度"
    },
    "ooda.decision.exploration_weight": {
        "old": 0.2,
        "new": 0.3,
        "reason": "增加探索权重，发现更多进化策略"
    },
    "graph.relation_thresholds.similarity_min": {
        "old": 0.5,
        "new": 0.6,
        "reason": "提高相似度阈值，减少噪声关联"
    },
    "performance.cache_ttl_seconds": {
        "old": 300,
        "new": 600,
        "reason": "延长缓存时间，提高性能"
    }
}

# 应用优化
for key, opt in optimizations.items():
    keys = key.split('.')
    obj = config
    for k in keys[:-1]:
        obj = obj[k]
    
    old_val = obj[keys[-1]]
    obj[keys[-1]] = opt['new']
    
    print(f"  ✓ {key}")
    print(f"    {old_val} → {opt['new']} ({opt['reason']})")

# 保存优化后的配置
with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"\n  ✓ 配置已保存到：{CONFIG_FILE}")

print("\n【2.4】验证配置...")

# 验证配置有效性
def validate_config(cfg):
    errors = []
    
    # 检查必需字段
    if 'agent' not in cfg:
        errors.append("缺少 agent 配置")
    if 'ooda' not in cfg:
        errors.append("缺少 ooda 配置")
    if 'graph' not in cfg:
        errors.append("缺少 graph 配置")
    
    # 检查值范围
    sensitivity = cfg.get('ooda', {}).get('emotional_analysis', {}).get('sensitivity', 0)
    if not 0 <= sensitivity <= 1:
        errors.append(f"情绪敏感度超出范围：{sensitivity}")
    
    exploration = cfg.get('ooda', {}).get('decision', {}).get('exploration_weight', 0)
    if not 0 <= exploration <= 1:
        errors.append(f"探索权重超出范围：{exploration}")
    
    return errors

errors = validate_config(config)
if errors:
    print("  ⚠️ 配置验证失败:")
    for err in errors:
        print(f"    - {err}")
else:
    print("  ✓ 配置验证通过")

print("\n" + "=" * 70)
print("✅ 步骤 2 完成：参数调整完成")
print("=" * 70)

# 显示配置摘要
print("\n📋 配置摘要:")
print("-" * 70)
print(json.dumps(config, indent=2))
