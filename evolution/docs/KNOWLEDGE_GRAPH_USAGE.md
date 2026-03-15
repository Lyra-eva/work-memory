# 知识图谱使用指南

**版本**: v3.3.0  
**创建**: 2026-03-15  
**状态**: ✅ 生产就绪

---

## 📚 目录

1. [快速开始](#快速开始)
2. [核心 API](#核心-api)
3. [使用示例](#使用示例)
4. [最佳实践](#最佳实践)
5. [故障排查](#故障排查)

---

## 快速开始

### 1. 初始化

```python
from evolution.core.knowledge_graph import KnowledgeGraph

# 初始化知识图谱
kg = KnowledgeGraph()
```

### 2. 添加概念

```python
from evolution.core.knowledge_graph import create_node

# 创建知识节点
node = create_node(
    name="Web Search",
    category="skill",
    definition="网络搜索能力",
    mastery=0.5
)

kg.add_node(node)
```

### 3. 创建关系

```python
from evolution.core.knowledge_graph import create_relation

# 创建依赖关系
rel = create_relation(
    source_id=node1.id,
    target_id=node2.id,
    relation_type="depends_on",
    strength=0.9
)

kg.add_relation(rel)
```

### 4. 查询统计

```python
stats = kg.get_stats()
print(f"总节点数：{stats['total_nodes']}")
print(f"总关系数：{stats['total_relations']}")
```

---

## 核心 API

### KnowledgeGraph 类

#### 节点管理

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `add_node(node)` | KnowledgeNode | str | 添加节点，返回 ID |
| `get_node(node_id)` | str | Optional[KnowledgeNode] | 获取节点 |
| `update_node(node_id, **kwargs)` | str, dict | bool | 更新节点属性 |
| `delete_node(node_id)` | str | bool | 删除节点 |
| `list_nodes(category, min_mastery)` | str, float | List[KnowledgeNode] | 列出节点 |

#### 关系管理

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `add_relation(relation)` | KnowledgeRelation | int | 添加关系 |
| `get_relations(node_id, type)` | str, str | List[KnowledgeRelation] | 获取关系 |
| `find_path(from, to, depth)` | str, str, int | Optional[List[str]] | 查找路径 |

#### 知识发现

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `find_knowledge_gaps(target)` | str | List[str] | 发现知识盲区 |
| `get_prerequisites(node_id)` | str | List[str] | 获取前置知识 |
| `suggest_learning_path(goal)` | str | List[str] | 建议学习路径 |
| `calculate_similarity(n1, n2)` | str, str | float | 计算相似度 |

---

### ConceptExtractor 类

#### 概念提取

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `extract_from_text(text, source)` | str, str | List[ExtractedConcept] | 从文本提取 |
| `extract_from_episode(data)` | dict | List[ExtractedConcept] | 从事件提取 |
| `extract_from_capability(data)` | dict | List[ExtractedConcept] | 从能力提取 |
| `extract_from_evolution_event(data)` | dict | List[ExtractedConcept] | 从进化事件提取 |

#### 概念整合

| 方法 | 参数 | 返回 | 说明 |
|------|------|------|------|
| `integrate_concepts(concepts, min_conf)` | List, float | int | 整合到图谱 |
| `discover_relations(data)` | dict | int | 发现关系 |

---

## 使用示例

### 示例 1: 构建个人知识图谱

```python
from evolution.core.knowledge_graph import KnowledgeGraph, create_node, create_relation

kg = KnowledgeGraph()

# 添加技能节点
python_skill = create_node("Python Programming", "skill", "Python 编程能力", mastery=0.7)
web_skill = create_node("Web Development", "skill", "Web 开发能力", mastery=0.5)
js_skill = create_node("JavaScript", "skill", "JavaScript 编程", mastery=0.6)

kg.add_node(python_skill)
kg.add_node(web_skill)
kg.add_node(js_skill)

# 创建依赖关系
# Web 开发需要 JavaScript
kg.add_relation(create_relation(js_skill.id, web_skill.id, "depends_on", 0.9))

# 查询 Web 开发的前置知识
prereqs = kg.get_prerequisites(web_skill.id)
print(f"学习 Web 开发前需要：{prereqs}")

# 发现知识盲区
gaps = kg.find_knowledge_gaps(web_skill.id)
print(f"知识盲区：{gaps}")

# 获取学习路径
path = kg.suggest_learning_path(web_skill.id)
print(f"建议学习路径：{path}")
```

---

### 示例 2: 从进化事件自动构建

```python
from evolution.core.knowledge_graph import KnowledgeGraph
from evolution.core.concept_extractor import ConceptExtractor

kg = KnowledgeGraph()
extractor = ConceptExtractor(kg)

# 模拟进化事件
events = [
    {
        'event_type': 'capability_learned',
        'data': {
            'capability': 'image_analysis',
            'description': '图像分析能力',
            'success': True
        }
    },
    {
        'event_type': 'skill_improved',
        'data': {
            'skill': 'web_search',
            'version': '2.0.0'
        }
    }
]

# 提取并整合概念
for event in events:
    concepts = extractor.extract_from_evolution_event(event)
    extractor.integrate_concepts(concepts)

# 查看统计
stats = kg.get_stats()
print(f"构建完成：{stats['total_nodes']} 个节点")
```

---

### 示例 3: 学习路径规划

```python
# 假设已有知识图谱
kg = KnowledgeGraph()

# 目标：掌握"Machine Learning"
goal = "kg_machine_learning_xxx"

# 1. 发现知识盲区
gaps = kg.find_knowledge_gaps(goal)
print(f"需要补充的知识：{gaps}")

# 2. 获取学习路径
path = kg.suggest_learning_path(goal)
print("\n建议学习顺序:")
for i, node_id in enumerate(path, 1):
    node = kg.get_node(node_id)
    print(f"{i}. {node.name} (掌握度：{node.mastery_level:.0%})")

# 3. 查找相关资源
for node_id in path:
    node = kg.get_node(node_id)
    relations = kg.get_relations(node_id)
    
    if relations:
        print(f"\n{node.name} 相关知识:")
        for rel in relations:
            related = kg.get_node(rel.target_id if rel.source_id == node_id else rel.source_id)
            print(f"  - {related.name} ({rel.relation_type})")
```

---

### 示例 4: 概念相似度计算

```python
kg = KnowledgeGraph()

# 添加相关概念
node1 = create_node("Deep Learning", "concept", "深度学习")
node2 = create_node("Machine Learning", "concept", "机器学习")
node3 = create_node("Web Development", "skill", "Web 开发")

kg.add_node(node1)
kg.add_node(node2)
kg.add_node(node3)

# 计算相似度
sim1 = kg.calculate_similarity(node1.id, node2.id)
sim2 = kg.calculate_similarity(node1.id, node3.id)

print(f"Deep Learning vs Machine Learning: {sim1:.2f}")
print(f"Deep Learning vs Web Development: {sim2:.2f}")
```

---

## 最佳实践

### 1. 节点命名规范

```python
# ✅ 好的命名
create_node("Web Search", "skill", ...)  # 驼峰命名，清晰
create_node("machine_learning", "concept", ...)  # 下划线分隔

# ❌ 避免
create_node("ws", "skill", ...)  # 缩写不清晰
create_node("WebSearchCapabilityFunction", "skill", ...)  # 过长
```

### 2. 关系强度设置

```python
# 强依赖 (0.8-1.0)
create_relation(src, tgt, "depends_on", strength=0.9)

# 中等关联 (0.5-0.8)
create_relation(src, tgt, "similar_to", strength=0.6)

# 弱关联 (0.3-0.5)
create_relation(src, tgt, "related_to", strength=0.4)
```

### 3. 掌握度更新

```python
# 学习后更新
kg.update_node(node_id, mastery_level=0.7)

# 批量更新
for node_id in learned_nodes:
    node = kg.get_node(node_id)
    kg.update_node(node_id, mastery_level=min(1.0, node.mastery_level + 0.1))
```

### 4. 定期导出备份

```python
# 每周导出一次
import datetime

if datetime.datetime.now().weekday() == 0:  # 周一
    backup_path = f"kg_backup_{datetime.date.today()}.json"
    kg.export_to_json(backup_path)
```

---

## 故障排查

### 问题 1: 节点无法添加

**症状**: `add_node()` 返回但节点不存在

**原因**: 数据库锁定或路径错误

**解决**:
```python
# 检查数据库路径
print(kg.db_path)

# 确保目录存在
import os
os.makedirs(os.path.dirname(kg.db_path), exist_ok=True)
```

---

### 问题 2: 关系创建失败

**症状**: 关系未出现在查询结果中

**原因**: 源或目标节点不存在

**解决**:
```python
# 验证节点存在
if kg.get_node(source_id) and kg.get_node(target_id):
    kg.add_relation(relation)
else:
    print("节点不存在")
```

---

### 问题 3: 学习路径为空

**症状**: `suggest_learning_path()` 返回空列表

**原因**: 目标节点掌握度已足够或无依赖关系

**解决**:
```python
# 检查目标节点
node = kg.get_node(goal_id)
print(f"当前掌握度：{node.mastery_level}")

# 检查是否有依赖关系
relations = kg.get_relations(goal_id, "depends_on")
print(f"依赖关系数：{len(relations)}")
```

---

### 问题 4: 概念提取不准确

**症状**: 提取到无关概念

**解决**:
```python
# 提高置信度阈值
extractor.integrate_concepts(concepts, min_confidence=0.8)

# 手动过滤
filtered = [c for c in concepts if len(c.name) > 3 and c.confidence > 0.7]
```

---

## 性能优化

### 1. 批量操作

```python
# ✅ 批量添加
nodes = [create_node(...) for _ in range(100)]
for node in nodes:
    kg.add_node(node)

# ❌ 避免频繁 IO
for i in range(100):
    node = create_node(...)
    kg.add_node(node)  # 每次都写磁盘
```

### 2. 缓存常用查询

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_node_cached(node_id):
    return kg.get_node(node_id)
```

### 3. 索引优化

```sql
-- 为常用查询字段创建索引
CREATE INDEX IF NOT EXISTS idx_category ON knowledge_nodes(category);
CREATE INDEX IF NOT EXISTS idx_mastery ON knowledge_nodes(mastery_level);
```

---

## 数据格式

### KnowledgeNode

```json
{
  "id": "kg_web_search_123",
  "name": "Web Search",
  "category": "skill",
  "definition": "网络搜索能力",
  "mastery_level": 0.75,
  "related_nodes": {
    "kg_keyword_extraction_456": 0.9
  },
  "metadata": {
    "source": "evolution_event",
    "version": "1.0.0"
  },
  "created_at": "2026-03-15T11:00:00",
  "updated_at": "2026-03-15T12:00:00"
}
```

### KnowledgeRelation

```json
{
  "source_id": "kg_keyword_extraction_456",
  "target_id": "kg_web_search_123",
  "relation_type": "used_for",
  "strength": 0.9,
  "evidence": ["auto_discovered", "manual_verified"],
  "created_at": "2026-03-15T11:00:00"
}
```

---

## 相关文件

- **核心模块**: `~/.openclaw/workspace/evolution/core/knowledge_graph.py`
- **概念提取**: `~/.openclaw/workspace/evolution/core/concept_extractor.py`
- **初始化脚本**: `~/.openclaw/workspace/evolution/core/init_knowledge_graph.py`
- **数据库**: `~/.openclaw/workspace/evolution/data/knowledge_graph.db`
- **导出文件**: `~/.openclaw/workspace/evolution/data/knowledge_graph.json`

---

## 下一步

- [ ] 实现记忆巩固模块
- [ ] 实现跨会话记忆关联
- [ ] 添加可视化界面
- [ ] 集成到进化流水线

---

**有问题？** 查看 `IMPLEMENTATION_PLAN_v3.3.md` 获取更多细节！
