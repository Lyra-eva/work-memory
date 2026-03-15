# 进化引擎 v3.5 优化计划

**目标**: 打磨现有功能，提升质量和可用性  
**时间**: 2026-03-15 开始  
**优先级**: 高

---

## 📊 优化方向

### 1. 性能优化 ⚡

#### 1.1 数据库查询优化

**现状**:
- 全表扫描较多
- 缺少复合索引
- 批量查询效率低

**优化项**:
```sql
-- 添加复合索引
CREATE INDEX idx_kg_category_mastery ON knowledge_nodes(category, mastery_level);
CREATE INDEX idx_mc_strength_due ON memory_items(strength, next_review);
CREATE INDEX idx_links_type_strength ON memory_links(link_type, strength);

-- 添加覆盖索引
CREATE INDEX idx_kg_nodes_list ON knowledge_nodes(category, mastery_level, created_at);
```

**预期提升**: 查询速度 50-80%

---

#### 1.2 批量操作优化

**现状**:
- 单条插入，IO 频繁
- 无批量处理接口

**优化项**:
```python
# 新增批量 API
class KnowledgeGraph:
    def add_nodes_batch(self, nodes: List[KnowledgeNode]):
        """批量添加节点"""
        with self.transaction() as conn:
            conn.executemany("INSERT OR REPLACE INTO ...", nodes_data)
    
    def update_nodes_batch(self, updates: List[Tuple[str, Dict]]):
        """批量更新节点"""

class MemoryConsolidator:
    def add_memories_batch(self, memories: List[MemoryItem]):
        """批量添加记忆"""
    
    def review_memories_batch(self, reviews: List[Tuple[str, float]]):
        """批量执行复习"""
```

**预期提升**: 批量操作速度 5-10 倍

---

#### 1.3 缓存层

**现状**:
- 每次查询都访问数据库
- 重复计算频繁

**优化项**:
```python
from functools import lru_cache
from datetime import timedelta

class KnowledgeGraph:
    def __init__(self):
        self._node_cache = {}
        self._cache_ttl = {}
    
    @lru_cache(maxsize=100)
    def get_node_cached(self, node_id: str) -> Optional[KnowledgeNode]:
        """带缓存的节点查询"""
    
    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        # 检查缓存
        if node_id in self._node_cache:
            if not self._is_expired(node_id):
                return self._node_cache[node_id]
        
        # 查询数据库
        node = self._query_from_db(node_id)
        if node:
            self._node_cache[node_id] = node
        return node
    
    def _is_expired(self, node_id: str) -> bool:
        """检查缓存是否过期"""
        if node_id not in self._cache_ttl:
            return True
        return datetime.now() > self._cache_ttl[node_id]
```

**预期提升**: 热点查询速度 90%+

---

### 2. 用户体验改进 🎨

#### 2.1 友好的错误处理

**现状**:
- 直接抛出异常
- 错误信息不清晰

**优化项**:
```python
class EvolutionError(Exception):
    """进化系统基础异常"""
    pass

class NodeNotFoundError(EvolutionError):
    """节点未找到"""
    def __init__(self, node_id: str, suggestions: List[str] = None):
        self.node_id = node_id
        self.suggestions = suggestions or []
    
    def __str__(self):
        msg = f"知识节点未找到：{self.node_id}"
        if self.suggestions:
            msg += f"\n建议：{', '.join(self.suggestions)}"
        return msg

class KnowledgeGraph:
    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        node = self.nodes.get(node_id)
        if not node:
            # 查找相似节点
            suggestions = self._find_similar_nodes(node_id, limit=3)
            raise NodeNotFoundError(node_id, suggestions)
        return node
    
    def _find_similar_nodes(self, node_id: str, limit: int = 3) -> List[str]:
        """查找相似的节点 ID（用于错误提示）"""
        # 实现模糊匹配
```

**效果**: 错误信息更友好，提供解决建议

---

#### 2.2 链式 API

**现状**:
- API 调用繁琐
- 代码冗长

**优化项**:
```python
class KnowledgeGraph:
    def query(self, category: str = None) -> 'Query':
        """开始链式查询"""
        return Query(self, category)

class Query:
    def __init__(self, kg: KnowledgeGraph, category: str = None):
        self.kg = kg
        self.nodes = kg.list_nodes(category=category)
    
    def with_mastery(self, min_level: float) -> 'Query':
        """过滤掌握度"""
        self.nodes = [n for n in self.nodes if n.mastery_level >= min_level]
        return self
    
    def with_relations(self, relation_type: str = None) -> 'Query':
        """包含关系"""
        # 过滤有关系的节点
        return self
    
    def order_by(self, field: str, reverse: bool = False) -> 'Query':
        """排序"""
        self.nodes.sort(key=lambda n: getattr(n, field, 0), reverse=reverse)
        return self
    
    def limit(self, count: int) -> 'Query':
        """限制数量"""
        self.nodes = self.nodes[:count]
        return self
    
    def first(self) -> Optional[KnowledgeNode]:
        """获取第一个"""
        return self.nodes[0] if self.nodes else None
    
    def all(self) -> List[KnowledgeNode]:
        """获取全部"""
        return self.nodes

# 使用示例
kg = KnowledgeGraph()

# 链式调用
weak_skills = (kg
    .query(category='skill')
    .with_mastery(min_level=0.0)
    .with_mastery(max_level=0.5)
    .order_by('mastery_level')
    .limit(5)
    .all())

# 获取最弱的技能
weakest = (kg
    .query(category='skill')
    .order_by('mastery_level')
    .first())
```

**效果**: 代码更简洁，可读性更强

---

#### 2.3 进度反馈

**现状**:
- 长时间操作无反馈
- 用户不知道进展

**优化项**:
```python
from tqdm import tqdm

class ConceptExtractor:
    def integrate_concepts(self, concepts: List[ExtractedConcept], 
                          min_confidence: float = 0.7,
                          show_progress: bool = False) -> int:
        """整合概念（带进度条）"""
        iterator = concepts
        if show_progress:
            iterator = tqdm(concepts, desc="整合概念", unit="个")
        
        integrated = 0
        for concept in iterator:
            if concept.confidence < min_confidence:
                continue
            
            self._create_concept(concept)
            integrated += 1
            
            if show_progress:
                iterator.set_postfix({'已整合': integrated})
        
        return integrated

class MemoryConsolidator:
    def generate_review_schedule(self, 
                                memories: List[MemoryItem] = None,
                                daily_capacity: int = 10,
                                callback: Callable = None) -> List[ReviewSchedule]:
        """生成复习计划（带回调）"""
        # ...
        for i, memory in enumerate(memories):
            # 处理
            if callback:
                callback(i, len(memories), memory)
```

**效果**: 用户知道操作进展，体验更好

---

### 3. 文档完善 📚

#### 3.1 API 参考文档

**现状**:
- 只有使用指南
- 缺少完整 API 文档

**优化项**:
```markdown
# API 参考文档

## KnowledgeGraph

### `__init__(db_path: str = KG_DB_PATH)`

初始化知识图谱

**参数**:
- `db_path`: 数据库文件路径

**示例**:
```python
kg = KnowledgeGraph()
kg = KnowledgeGraph("/path/to/custom.db")
```

---

### `add_node(node: KnowledgeNode) -> str`

添加知识节点

**参数**:
- `node`: KnowledgeNode 对象

**返回**:
- `str`: 节点 ID

**异常**:
- `ValueError`: 节点 ID 已存在

**示例**:
```python
node = create_node("Python", "skill", "Python 编程", mastery=0.5)
node_id = kg.add_node(node)
```

---

### `find_knowledge_gaps(target_node_id: str) -> List[str]`

发现知识盲区

**参数**:
- `target_node_id`: 目标节点 ID

**返回**:
- `List[str]`: 需要补充的知识节点 ID 列表

**算法**:
1. 反向遍历依赖关系
2. 找出掌握度 < 0.5 的节点
3. 按依赖顺序排序

**示例**:
```python
gaps = kg.find_knowledge_gaps("kg_machine_learning_xxx")
# → ["kg_python_basics", "kg_linear_algebra", ...]
```
```

---

#### 3.2 最佳实践指南

**新增文档**:
```markdown
# 进化引擎最佳实践

## 知识图谱

### ✅ 推荐做法

1. **命名规范**
```python
# 好的命名
create_node("Web Search", "skill", ...)  # 清晰
create_node("machine_learning", "concept", ...)  # 下划线分隔

# 避免
create_node("ws", "skill", ...)  # 缩写不清晰
```

2. **关系强度设置**
```python
# 强依赖 (0.8-1.0)
create_relation(src, tgt, "depends_on", strength=0.9)

# 中等关联 (0.5-0.8)
create_relation(src, tgt, "similar_to", strength=0.6)
```

3. **批量操作**
```python
# 批量添加（高效）
nodes = [create_node(...) for _ in range(100)]
kg.add_nodes_batch(nodes)

# 单条添加（低效）
for i in range(100):
    kg.add_node(create_node(...))
```

## 记忆巩固

### 最佳复习时机

- **保留率 60-70%**: 最佳复习时机
- **保留率 < 40%**: 需要救援复习
- **保留率 > 80%**: 可以延后复习

### 回忆质量评估

| 质量 | 分数 | 效果 |
|------|------|------|
| 完美 | 0.95-1.0 | 强度 +20% |
| 良好 | 0.8-0.95 | 强度 +15% |
| 一般 | 0.6-0.8 | 强度 +8% |
| 困难 | 0.4-0.6 | 强度 -5% |
| 失败 | < 0.4 | 强度 -20% |
```

---

#### 3.3 示例代码库

**新增目录**:
```
~/.openclaw/workspace/evolution/examples/
├── 01_knowledge_graph_basics.py      # 知识图谱基础
├── 02_concept_extraction.py          # 概念提取示例
├── 03_memory_consolidation.py        # 记忆巩固示例
├── 04_memory_linking.py              # 记忆关联示例
├── 05_integrated_workflow.py         # 完整工作流
└── README.md                         # 示例说明
```

**示例内容**:
```python
# examples/01_knowledge_graph_basics.py
"""知识图谱基础示例"""

from evolution.core.knowledge_graph import KnowledgeGraph, create_node

# 初始化
kg = KnowledgeGraph()

# 创建技能节点
python = create_node("Python", "skill", "Python 编程能力", mastery=0.5)
web = create_node("Web Development", "skill", "Web 开发能力", mastery=0.3)

kg.add_node(python)
kg.add_node(web)

# 查询
print(f"Python 掌握度：{kg.get_node(python.id).mastery_level:.0%}")

# 学习路径
path = kg.suggest_learning_path(web.id)
print(f"学习路径：{path}")
```

---

### 4. 测试增强 🧪

#### 4.1 单元测试覆盖

**现状**:
- 只有集成测试
- 缺少单元测试

**优化项**:
```python
# tests/test_knowledge_graph.py
import unittest
from evolution.core.knowledge_graph import KnowledgeGraph, create_node

class TestKnowledgeGraph(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.kg = KnowledgeGraph(":memory:")  # 内存数据库
    
    def test_add_node(self):
        """测试添加节点"""
        node = create_node("Test", "skill", "测试技能")
        node_id = self.kg.add_node(node)
        
        self.assertIsNotNone(node_id)
        self.assertIn(node_id, self.kg.nodes)
    
    def test_get_node_not_found(self):
        """测试查询不存在的节点"""
        result = self.kg.get_node("nonexistent")
        self.assertIsNone(result)
    
    def test_update_node(self):
        """测试更新节点"""
        node = create_node("Test", "skill", "测试技能", mastery=0.5)
        self.kg.add_node(node)
        
        self.kg.update_node(node.id, mastery_level=0.8)
        updated = self.kg.get_node(node.id)
        
        self.assertEqual(updated.mastery_level, 0.8)
    
    def test_find_knowledge_gaps(self):
        """测试知识盲区发现"""
        # 创建依赖链
        basic = create_node("Basic", "skill", "基础", mastery=0.3)
        advanced = create_node("Advanced", "skill", "进阶", mastery=0.8)
        
        self.kg.add_node(basic)
        self.kg.add_node(advanced)
        
        # 创建依赖关系
        from evolution.core.knowledge_graph import create_relation
        rel = create_relation(basic.id, advanced.id, "depends_on")
        self.kg.add_relation(rel)
        
        # 查找盲区
        gaps = self.kg.find_knowledge_gaps(advanced.id)
        self.assertIn(basic.id, gaps)

if __name__ == '__main__':
    unittest.main()
```

**目标**: 覆盖率 > 80%

---

#### 4.2 性能测试

**新增性能测试**:
```python
# tests/test_performance.py
import time
import unittest
from evolution.core.knowledge_graph import KnowledgeGraph, create_node

class TestPerformance(unittest.TestCase):
    def test_batch_insert_performance(self):
        """批量插入性能测试"""
        kg = KnowledgeGraph(":memory:")
        
        # 插入 1000 个节点
        start = time.time()
        for i in range(1000):
            node = create_node(f"Node{i}", "concept", f"测试节点{i}")
            kg.add_node(node)
        elapsed = time.time() - start
        
        # 要求：< 1 秒
        self.assertLess(elapsed, 1.0, f"批量插入超时：{elapsed:.2f}秒")
    
    def test_query_performance(self):
        """查询性能测试"""
        kg = KnowledgeGraph(":memory:")
        
        # 准备数据
        for i in range(1000):
            node = create_node(f"Node{i}", "concept", f"测试节点{i}")
            kg.add_node(node)
        
        # 查询 100 次
        start = time.time()
        for i in range(100):
            kg.get_node(f"kg_node{i}_xxx")
        elapsed = (time.time() - start) / 100
        
        # 要求：平均 < 5ms
        self.assertLess(elapsed, 0.005, f"查询超时：{elapsed*1000:.2f}ms")
```

---

#### 4.3 回归测试

**新增回归测试集**:
```python
# tests/test_regression.py
"""回归测试集 - 确保旧功能不被破坏"""

import unittest

class TestRegression(unittest.TestCase):
    """回归测试"""
    
    def test_v3.3_features(self):
        """v3.3 功能回归"""
        # 测试知识图谱所有功能
        
    def test_v3.4_features(self):
        """v3.4 功能回归"""
        # 测试记忆巩固所有功能
        
    def test_v3.5_features(self):
        """v3.5 功能回归"""
        # 测试记忆关联所有功能
```

---

## 📅 实施计划

### Week 1: 性能优化
- [ ] 数据库索引优化
- [ ] 批量操作 API
- [ ] 缓存层实现
- [ ] 性能基准测试

### Week 2: 用户体验
- [ ] 错误处理优化
- [ ] 链式 API 实现
- [ ] 进度反馈机制
- [ ] 日志系统完善

### Week 3: 文档完善
- [ ] API 参考文档
- [ ] 最佳实践指南
- [ ] 示例代码库
- [ ] 视频教程脚本

### Week 4: 测试增强
- [ ] 单元测试 (>80% 覆盖)
- [ ] 性能测试
- [ ] 回归测试
- [ ] CI/CD 配置

---

## 📊 成功指标

### 性能指标
- [ ] 查询响应 < 5ms (当前 < 10ms)
- [ ] 批量操作速度提升 5 倍
- [ ] 缓存命中率 > 70%

### 质量指标
- [ ] 单元测试覆盖率 > 80%
- [ ] 文档完整度 > 95%
- [ ] 示例代码 > 10 个

### 用户体验
- [ ] 错误信息清晰度评分 > 4/5
- [ ] API 易用性评分 > 4/5
- [ ] 文档满意度 > 4/5

---

## 🎯 优先级排序

### P0 (必须做)
1. 数据库索引优化
2. 错误处理优化
3. 单元测试覆盖

### P1 (应该做)
1. 批量操作 API
2. API 参考文档
3. 性能测试

### P2 (可以做)
1. 缓存层
2. 链式 API
3. 示例代码库

### P3 (可选)
1. 进度反馈
2. 视频教程
3. CI/CD

---

**优化计划制定完成!** 🎉

接下来从哪个开始？我建议从 **P0 优先级** 开始：
1. 数据库索引优化 (快速见效)
2. 错误处理优化 (提升体验)
3. 单元测试 (保证质量)

你觉得呢？
