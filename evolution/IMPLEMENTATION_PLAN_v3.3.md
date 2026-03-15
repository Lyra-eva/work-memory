# 方向 1+3 联合实现方案

**个体认知增强 × 记忆系统增强**

**版本**: v3.3-v3.5  
**优先级**: ⭐⭐⭐⭐⭐  
**实施时间**: 2026-03-16 开始

---

## 🎯 核心目标

将**认知增强**与**记忆系统**深度融合，打造：
- 有"自我意识"的进化系统
- 能够反思、关联、巩固的智能记忆
- 持续成长的个体认知能力

---

## 📦 功能模块分解

### 模块 A: 知识图谱构建 (方向 1.3)

#### A.1 核心数据结构

```python
# ~/.openclaw/workspace/evolution/core/knowledge_graph.py

from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional
from datetime import datetime
import json

@dataclass
class KnowledgeNode:
    """知识节点"""
    id: str
    name: str
    category: str  # concept, skill, fact, experience
    definition: str
    related_nodes: Dict[str, float] = field(default_factory=dict)  # {node_id: strength}
    mastery_level: float = 0.0  # 0-1 掌握程度
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'definition': self.definition,
            'related_nodes': self.related_nodes,
            'mastery_level': self.mastery_level,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'metadata': self.metadata
        }

@dataclass
class KnowledgeRelation:
    """知识关系"""
    source_id: str
    target_id: str
    relation_type: str  # depends_on, similar_to, part_of, causes, used_for
    strength: float  # 0-1 关系强度
    evidence: List[str] = field(default_factory=list)  # 支持证据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

class KnowledgeGraph:
    """知识图谱"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.relations: List[KnowledgeRelation] = []
        self._load()
    
    def _load(self):
        """从数据库加载"""
        # 从 SQLite 或 JSON 加载
        pass
    
    def add_node(self, node: KnowledgeNode):
        """添加知识节点"""
        self.nodes[node.id] = node
        self._save()
    
    def add_relation(self, relation: KnowledgeRelation):
        """添加知识关系"""
        self.relations.append(relation)
        # 更新节点的相关性
        source = self.nodes.get(relation.source_id)
        if source:
            source.related_nodes[relation.target_id] = relation.strength
            source.updated_at = datetime.now().isoformat()
        self._save()
    
    def find_knowledge_gaps(self, target_skill: str) -> List[str]:
        """发现知识盲区"""
        # 反向遍历依赖关系，找出缺失的前置知识
        gaps = []
        visited = set()
        
        def check_dependencies(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            
            node = self.nodes.get(node_id)
            if not node:
                gaps.append(node_id)
                return
            
            if node.mastery_level < 0.5:  # 掌握度低于 50%
                gaps.append(node_id)
            
            # 检查前置依赖
            for rel in self.relations:
                if rel.target_id == node_id and rel.relation_type == 'depends_on':
                    check_dependencies(rel.source_id)
        
        check_dependencies(target_skill)
        return gaps
    
    def suggest_learning_path(self, goal: str) -> List[str]:
        """建议学习路径"""
        gaps = self.find_knowledge_gaps(goal)
        # 按依赖关系排序，先学前置知识
        path = []
        remaining = set(gaps)
        
        while remaining:
            # 找出没有未学习依赖的节点
            ready = []
            for node_id in remaining:
                deps = [r.source_id for r in self.relations 
                       if r.target_id == node_id and r.relation_type == 'depends_on']
                if not any(d in remaining for d in deps):
                    ready.append(node_id)
            
            if not ready:
                # 有循环依赖，打破
                ready = [list(remaining)[0]]
            
            # 添加到路径
            for node_id in ready:
                path.append(node_id)
                remaining.remove(node_id)
        
        return path
    
    def _save(self):
        """保存到数据库"""
        pass
```

#### A.2 自动概念提取

```python
# ~/.openclaw/workspace/evolution/core/concept_extractor.py

import re
from typing import List, Dict
from core.knowledge_graph import KnowledgeNode, KnowledgeRelation

class ConceptExtractor:
    """从对话和事件中提取概念"""
    
    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph
        self.term_pattern = re.compile(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b')
    
    def extract_from_episode(self, episode_content: str) -> List[Dict]:
        """从情景记忆提取概念"""
        concepts = []
        
        # 提取专业术语
        terms = self.term_pattern.findall(episode_content)
        for term in terms:
            if len(term) > 3:  # 过滤短词
                concepts.append({
                    'name': term,
                    'source': 'episode',
                    'confidence': 0.6
                })
        
        return concepts
    
    def extract_from_capability(self, capability_data: Dict) -> List[Dict]:
        """从能力数据提取概念"""
        concepts = []
        
        # 能力名称作为核心概念
        concepts.append({
            'name': capability_data.get('name', ''),
            'source': 'capability',
            'confidence': 0.9,
            'category': 'skill'
        })
        
        # 能力描述中的关键词
        description = capability_data.get('description', '')
        keywords = self._extract_keywords(description)
        for kw in keywords:
            concepts.append({
                'name': kw,
                'source': 'capability_description',
                'confidence': 0.7,
                'category': 'concept'
            })
        
        return concepts
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单的名词短语提取
        # TODO: 使用更好的 NLP 模型
        words = text.split()
        return [w for w in words if len(w) > 4 and w[0].isupper()]
    
    def integrate_concepts(self, concepts: List[Dict]):
        """整合概念到知识图谱"""
        for concept in concepts:
            if concept['confidence'] < 0.7:
                continue
            
            # 检查是否已存在
            existing = self._find_similar_concept(concept['name'])
            if existing:
                # 更新现有节点
                pass
            else:
                # 创建新节点
                node = KnowledgeNode(
                    id=f"concept_{concept['name'].lower().replace(' ', '_')}",
                    name=concept['name'],
                    category=concept.get('category', 'concept'),
                    definition=f"从{concept['source']}中提取的概念",
                    metadata={'source': concept['source']}
                )
                self.kg.add_node(node)
    
    def _find_similar_concept(self, name: str) -> Optional[KnowledgeNode]:
        """查找相似概念"""
        name_lower = name.lower()
        for node in self.kg.nodes.values():
            if node.name.lower() == name_lower:
                return node
        return None
```

---

### 模块 B: 长期记忆巩固 (方向 3.1)

#### B.1 间隔重复算法

```python
# ~/.openclaw/workspace/evolution/core/memory_consolidation.py

import math
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class MemoryItem:
    """记忆项目"""
    id: str
    content: Dict
    strength: float = 0.0  # 记忆强度 0-1
    decay_rate: float = 0.1  # 衰减速率
    last_reviewed: Optional[str] = None
    review_count: int = 0
    next_review: Optional[str] = None
    importance: float = 0.5  # 重要性 0-1
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'strength': self.strength,
            'decay_rate': self.decay_rate,
            'last_reviewed': self.last_reviewed,
            'review_count': self.review_count,
            'next_review': self.next_review,
            'importance': self.importance
        }

class MemoryConsolidator:
    """记忆巩固器 - 基于艾宾浩斯遗忘曲线"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.memories: Dict[str, MemoryItem] = {}
        self._load()
    
    def add_memory(self, memory: MemoryItem):
        """添加记忆"""
        # 计算初始复习时间
        memory.next_review = self._calculate_next_review(
            memory.strength,
            memory.importance,
            memory.review_count
        )
        self.memories[memory.id] = memory
        self._save()
    
    def review_memory(self, memory_id: str, recall_quality: float):
        """复习记忆"""
        memory = self.memories.get(memory_id)
        if not memory:
            return
        
        # 根据回忆质量更新强度
        if recall_quality > 0.8:  # 回忆良好
            memory.strength = min(1.0, memory.strength + 0.2)
            memory.decay_rate *= 0.9  # 减缓衰减
        elif recall_quality < 0.5:  # 回忆困难
            memory.strength *= 0.7  # 强度下降
            memory.decay_rate *= 1.2  # 加快衰减（需要更频繁复习）
        
        memory.review_count += 1
        memory.last_reviewed = datetime.now().isoformat()
        memory.next_review = self._calculate_next_review(
            memory.strength,
            memory.importance,
            memory.review_count
        )
        
        self._save()
    
    def _calculate_next_review(self, strength: float, importance: float, 
                               review_count: int) -> str:
        """计算下次复习时间"""
        # 基础间隔（小时）
        base_interval = 24  # 1 天
        
        # 强度因子：强度越高，间隔越长
        strength_factor = 1 + strength * 2
        
        # 重要性因子：越重要，间隔越短（需要更牢固）
        importance_factor = 1 + (1 - importance) * 0.5
        
        # 重复次数因子：复习次数越多，间隔呈指数增长
        repetition_factor = math.pow(2, review_count) if review_count > 0 else 1
        
        # 最终间隔（小时）
        interval_hours = base_interval * strength_factor * importance_factor * repetition_factor
        
        # 限制最大间隔为 30 天
        interval_hours = min(interval_hours, 24 * 30)
        
        next_review = datetime.now() + timedelta(hours=interval_hours)
        return next_review.isoformat()
    
    def get_due_memories(self) -> List[MemoryItem]:
        """获取需要复习的记忆"""
        now = datetime.now()
        due = []
        
        for memory in self.memories.values():
            if memory.next_review:
                next_review = datetime.fromisoformat(memory.next_review)
                if next_review <= now:
                    due.append(memory)
        
        # 按重要性排序
        due.sort(key=lambda m: m.importance, reverse=True)
        return due
    
    def calculate_retention(self, memory: MemoryItem) -> float:
        """计算记忆保留率（艾宾浩斯曲线）"""
        if not memory.last_reviewed:
            return memory.strength
        
        last_review = datetime.fromisoformat(memory.last_reviewed)
        time_elapsed = (datetime.now() - last_review).total_seconds() / 3600  # 小时
        
        # 艾宾浩斯遗忘曲线：R = e^(-t/S)
        # S 是记忆强度相关的常数
        S = 24 * (1 + memory.strength)  # 半衰期（小时）
        retention = math.exp(-time_elapsed / S)
        
        # 考虑重要性加成
        retention *= (0.5 + memory.importance * 0.5)
        
        return min(1.0, retention)
    
    def _load(self):
        """从数据库加载"""
        pass
    
    def _save(self):
        """保存到数据库"""
        pass
```

#### B.2 记忆强度衰减模型

```python
# ~/.openclaw/workspace/evolution/core/memory_decay.py

from datetime import datetime, timedelta
from typing import List, Dict
import math

class MemoryDecayModel:
    """记忆衰减模型"""
    
    def __init__(self):
        # 艾宾浩斯遗忘曲线参数
        self.base_decay_rate = 0.1  # 基础衰减速率/小时
        self.half_life_hours = 24  # 半衰期（小时）
    
    def calculate_decay(self, 
                       initial_strength: float,
                       time_elapsed_hours: float,
                       repetitions: int = 0,
                       importance: float = 0.5,
                       emotional_intensity: float = 0.5) -> float:
        """
        计算记忆衰减
        
        参数:
            initial_strength: 初始强度
            time_elapsed_hours: 经过时间（小时）
            repetitions: 复习次数
            importance: 重要性 (0-1)
            emotional_intensity: 情感强度 (0-1)
        
        返回:
            当前记忆强度 (0-1)
        """
        # 基础衰减（指数衰减）
        decay_constant = self.base_decay_rate
        
        # 复习次数减少衰减速率
        if repetitions > 0:
            decay_constant /= math.log2(repetitions + 2)
        
        # 重要性降低衰减速率
        decay_constant *= (1 - importance * 0.5)
        
        # 情感强度降低衰减速率（情感强烈的记忆更持久）
        decay_constant *= (1 - emotional_intensity * 0.3)
        
        # 计算衰减
        current_strength = initial_strength * math.exp(-decay_constant * time_elapsed_hours)
        
        return max(0.0, min(1.0, current_strength))
    
    def predict_forgetting_time(self,
                               current_strength: float,
                               threshold: float = 0.3,
                               repetitions: int = 0,
                               importance: float = 0.5) -> float:
        """
        预测遗忘时间
        
        参数:
            current_strength: 当前强度
            threshold: 遗忘阈值（低于此值认为已遗忘）
            repetitions: 复习次数
            importance: 重要性
        
        返回:
            距离遗忘的小时数
        """
        decay_constant = self.base_decay_rate
        if repetitions > 0:
            decay_constant /= math.log2(repetitions + 2)
        decay_constant *= (1 - importance * 0.5)
        
        if decay_constant <= 0:
            return float('inf')
        
        # 解方程：threshold = current_strength * e^(-decay * t)
        # t = -ln(threshold / current_strength) / decay
        if current_strength <= threshold:
            return 0
        
        time_to_forget = -math.log(threshold / current_strength) / decay_constant
        return time_to_forget
    
    def suggest_review_schedule(self,
                               memories: List[Dict],
                               review_capacity: int = 10) -> List[Dict]:
        """
        建议复习计划
        
        参数:
            memories: 记忆列表
            review_capacity: 每次最多复习数量
        
        返回:
            复习计划
        """
        schedule = []
        
        for memory in memories:
            # 计算遗忘风险
            time_to_forget = self.predict_forgetting_time(
                memory['strength'],
                repetitions=memory.get('repetitions', 0),
                importance=memory.get('importance', 0.5)
            )
            
            # 计算优先级（越容易遗忘的优先级越高）
            urgency = 1.0 / (time_to_forget + 1)  # 加 1 避免除零
            importance = memory.get('importance', 0.5)
            priority = urgency * (0.5 + importance * 0.5)
            
            schedule.append({
                'memory_id': memory['id'],
                'priority': priority,
                'optimal_review_time': self._calculate_optimal_time(memory),
                'estimated_duration': self._estimate_review_duration(memory)
            })
        
        # 按优先级排序
        schedule.sort(key=lambda s: s['priority'], reverse=True)
        
        # 限制数量
        return schedule[:review_capacity]
    
    def _calculate_optimal_time(self, memory: Dict) -> str:
        """计算最佳复习时间"""
        # 在记忆强度降到 0.6 时复习
        target_strength = 0.6
        current = memory['strength']
        
        if current <= target_strength:
            return datetime.now().isoformat()
        
        decay = self.base_decay_rate / math.log2(memory.get('repetitions', 0) + 2)
        hours = -math.log(target_strength / current) / decay
        
        optimal_time = datetime.now() + timedelta(hours=hours)
        return optimal_time.isoformat()
    
    def _estimate_review_duration(self, memory: Dict) -> int:
        """估计复习所需时间（分钟）"""
        # 基础时间 5 分钟
        base = 5
        
        # 根据复杂度和熟悉度调整
        complexity = memory.get('complexity', 1.0)
        familiarity = memory.get('strength', 0.5)
        
        duration = base * complexity * (2 - familiarity)
        return int(duration)
```

---

### 模块 C: 跨会话记忆关联 (方向 3.2)

#### C.1 主题关联发现

```python
# ~/.openclaw/workspace/evolution/core/memory_linking.py

from typing import List, Dict, Set, Tuple
from datetime import datetime
import hashlib

class MemoryLinker:
    """记忆关联器"""
    
    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph
        self.link_threshold = 0.6  # 关联阈值
    
    def find_related_episodes(self, 
                             current_episode: Dict,
                             all_episodes: List[Dict],
                             limit: int = 5) -> List[Dict]:
        """查找相关情景记忆"""
        scores = []
        
        for episode in all_episodes:
            if episode['id'] == current_episode['id']:
                continue
            
            # 计算多维度相似度
            score = self._calculate_similarity(current_episode, episode)
            
            if score > self.link_threshold:
                scores.append((score, episode))
        
        # 按相似度排序
        scores.sort(reverse=True)
        return [ep for score, ep in scores[:limit]]
    
    def _calculate_similarity(self, ep1: Dict, ep2: Dict) -> float:
        """计算两个记忆的相似度"""
        scores = []
        weights = []
        
        # 1. 主题相似度
        theme_sim = self._theme_similarity(ep1, ep2)
        scores.append(theme_sim)
        weights.append(0.4)
        
        # 2. 实体相似度（共享概念）
        entity_sim = self._entity_similarity(ep1, ep2)
        scores.append(entity_sim)
        weights.append(0.3)
        
        # 3. 时间接近度
        time_sim = self._time_similarity(ep1, ep2)
        scores.append(time_sim)
        weights.append(0.15)
        
        # 4. 情感相似度
        emotion_sim = self._emotion_similarity(ep1, ep2)
        scores.append(emotion_sim)
        weights.append(0.15)
        
        # 加权平均
        total = sum(s * w for s, w in zip(scores, weights))
        return total
    
    def _theme_similarity(self, ep1: Dict, ep2: Dict) -> float:
        """主题相似度"""
        tags1 = set(ep1.get('tags', []))
        tags2 = set(ep2.get('tags', []))
        
        if not tags1 or not tags2:
            return 0.0
        
        intersection = len(tags1 & tags2)
        union = len(tags1 | tags2)
        return intersection / union if union > 0 else 0.0
    
    def _entity_similarity(self, ep1: Dict, ep2: Dict) -> float:
        """实体相似度（共享概念）"""
        entities1 = set(ep1.get('entities', []))
        entities2 = set(ep2.get('entities', []))
        
        if not entities1 or not entities2:
            return 0.0
        
        intersection = len(entities1 & entities2)
        return min(1.0, intersection / max(len(entities1), len(entities2)))
    
    def _time_similarity(self, ep1: Dict, ep2: Dict) -> float:
        """时间接近度"""
        time1 = datetime.fromisoformat(ep1.get('created_at', datetime.now().isoformat()))
        time2 = datetime.fromisoformat(ep2.get('created_at', datetime.now().isoformat()))
        
        diff_hours = abs((time1 - time2).total_seconds()) / 3600
        
        # 24 小时内为 1.0，7 天内线性衰减到 0
        if diff_hours < 24:
            return 1.0
        elif diff_hours < 168:  # 7 天
            return 1.0 - (diff_hours - 24) / 144
        else:
            return 0.0
    
    def _emotion_similarity(self, ep1: Dict, ep2: Dict) -> float:
        """情感相似度"""
        emotion1 = ep1.get('emotion', {})
        emotion2 = ep2.get('emotion', {})
        
        if not emotion1 or not emotion2:
            return 0.5  # 中性
        
        # 情感类型相同得 1 分，相似得 0.5 分
        type1 = emotion1.get('type', 'neutral')
        type2 = emotion2.get('type', 'neutral')
        
        if type1 == type2:
            return 1.0
        elif self._similar_emotions(type1, type2):
            return 0.5
        else:
            return 0.0
    
    def _similar_emotions(self, e1: str, e2: str) -> bool:
        """判断情感是否相似"""
        similar_groups = [
            {'joy', 'excitement', 'pride'},
            {'sadness', 'disappointment', 'grief'},
            {'anger', 'frustration', 'annoyance'},
            {'fear', 'anxiety', 'worry'},
        ]
        
        for group in similar_groups:
            if e1 in group and e2 in group:
                return True
        return False
    
    def create_memory_chain(self, 
                           seed_episode: Dict,
                           all_episodes: List[Dict],
                           max_length: int = 10) -> List[Dict]:
        """创建记忆链（关联序列）"""
        chain = [seed_episode]
        visited = {seed_episode['id']}
        
        current = seed_episode
        for _ in range(max_length - 1):
            # 找最相关的未访问记忆
            related = self.find_related_episodes(current, all_episodes, limit=10)
            
            next_episode = None
            for ep in related:
                if ep['id'] not in visited:
                    next_episode = ep
                    break
            
            if not next_episode:
                break
            
            chain.append(next_episode)
            visited.add(next_episode['id'])
            current = next_episode
        
        return chain
    
    def generate_context_summary(self, 
                                episode: Dict,
                                related_episodes: List[Dict]) -> str:
        """生成上下文摘要"""
        summary_parts = []
        
        # 当前记忆
        summary_parts.append(f"当前：{episode.get('title', '无标题')}")
        
        # 相关记忆
        if related_episodes:
            summary_parts.append("\n相关记忆:")
            for i, ep in enumerate(related_episodes[:3], 1):
                summary_parts.append(f"  {i}. {ep.get('title', '无标题')} "
                                   f"({ep.get('created_at', '')[:10]})")
        
        return '\n'.join(summary_parts)
```

---

## 📊 数据库设计

### 新增表结构

```sql
-- 知识节点表
CREATE TABLE knowledge_nodes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    definition TEXT,
    mastery_level REAL DEFAULT 0.0,
    metadata JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 知识关系表
CREATE TABLE knowledge_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    strength REAL DEFAULT 1.0,
    evidence JSON DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES knowledge_nodes(id),
    FOREIGN KEY (target_id) REFERENCES knowledge_nodes(id)
);

-- 记忆巩固表
CREATE TABLE memory_consolidation (
    id TEXT PRIMARY KEY,
    content JSON NOT NULL,
    strength REAL DEFAULT 0.0,
    decay_rate REAL DEFAULT 0.1,
    last_reviewed TIMESTAMP,
    review_count INTEGER DEFAULT 0,
    next_review TIMESTAMP,
    importance REAL DEFAULT 0.5,
    emotional_intensity REAL DEFAULT 0.5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 记忆关联表
CREATE TABLE memory_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    link_type TEXT NOT NULL,
    strength REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES episodic_memory(id),
    FOREIGN KEY (target_id) REFERENCES episodic_memory(id)
);

-- 索引
CREATE INDEX idx_knowledge_category ON knowledge_nodes(category);
CREATE INDEX idx_knowledge_mastery ON knowledge_nodes(mastery_level);
CREATE INDEX idx_relations_source ON knowledge_relations(source_id);
CREATE INDEX idx_relations_target ON knowledge_relations(target_id);
CREATE INDEX idx_memory_next_review ON memory_consolidation(next_review);
CREATE INDEX idx_memory_links_source ON memory_links(source_id);
```

---

## 🔄 集成流程

### 整体工作流

```
1. 新事件发生
   ↓
2. 概念提取 → 知识图谱
   ↓
3. 存储为情景记忆
   ↓
4. 记忆关联发现
   ↓
5. 记忆巩固调度
   ↓
6. 定期复习强化
```

---

## 📈 成功指标

| 指标 | 基线 | 目标 |
|------|------|------|
| 知识节点数 | 0 | 100+ |
| 知识关系数 | 0 | 300+ |
| 记忆保留率 | 50% | 80% |
| 关联发现准确率 | - | 75%+ |
| 复习完成率 | - | 70%+ |

---

## 🚀 实施步骤

### Week 1: 知识图谱基础
- [ ] 实现 KnowledgeGraph 核心类
- [ ] 创建数据库表
- [ ] 实现概念提取器
- [ ] 单元测试

### Week 2: 记忆巩固
- [ ] 实现间隔重复算法
- [ ] 创建记忆巩固表
- [ ] 实现复习调度
- [ ] 集成到进化事件流

### Week 3: 记忆关联
- [ ] 实现相似度计算
- [ ] 创建记忆关联表
- [ ] 实现记忆链生成
- [ ] 上下文摘要功能

### Week 4: 集成测试
- [ ] 端到端测试
- [ ] 性能优化
- [ ] 文档完善
- [ ] v3.3 发布

---

**下一步**: 从哪个模块开始实现？我建议从**知识图谱基础**开始！🎯
