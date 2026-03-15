#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆关联模块 - Memory Linking

跨会话记忆关联系统
支持主题关联、实体关联、时间关联、情感关联
生成记忆链和上下文摘要

版本：v3.5.0
创建：2026-03-15
"""

import json
import os
import sqlite3
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field, asdict
from contextlib import contextmanager
from collections import Counter
import uuid


# ============================================================
# 配置
# ============================================================

WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")
EVOLUTION_DIR = os.path.join(WORKSPACE_DIR, 'evolution')
DATA_DIR = os.path.join(EVOLUTION_DIR, 'data')
LINK_DB_PATH = os.path.join(DATA_DIR, 'memory_links.db')


# ============================================================
# 数据类
# ============================================================

@dataclass
class MemoryLink:
    """记忆关联"""
    id: int
    source_id: str
    target_id: str
    link_type: str  # thematic, entity, temporal, emotional, semantic
    strength: float  # 0-1 关联强度
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class MemoryChain:
    """记忆链"""
    id: str
    memories: List[str]  # 记忆 ID 列表
    chain_type: str
    total_strength: float
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ContextSummary:
    """上下文摘要"""
    current_memory: str
    related_memories: List[str]
    summary_text: str
    themes: List[str]
    entities: List[str]
    time_span: str
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ============================================================
# 记忆关联器
# ============================================================

class MemoryLinker:
    """
    记忆关联器
    
    功能:
    - 多维度相似度计算
    - 跨会话记忆关联
    - 记忆链生成
    - 上下文摘要生成
    """
    
    def __init__(self, db_path: str = LINK_DB_PATH):
        """初始化记忆关联器"""
        self.db_path = db_path
        self.links: List[MemoryLink] = []
        self.chains: Dict[str, MemoryChain] = {}
        self._init_db()
        # 内存数据库不需要加载
        if db_path != ":memory:":
            self._load()
    
    @contextmanager
    def transaction(self):
        """事务上下文"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _init_db(self):
        """初始化数据库"""
        with self.transaction() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    link_type TEXT NOT NULL,
                    strength REAL DEFAULT 1.0,
                    metadata JSON DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_chains (
                    id TEXT PRIMARY KEY,
                    memories JSON NOT NULL,
                    chain_type TEXT NOT NULL,
                    total_strength REAL DEFAULT 1.0,
                    metadata JSON DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 索引
            conn.execute("CREATE INDEX IF NOT EXISTS idx_links_source ON memory_links(source_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_links_target ON memory_links(target_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_links_type ON memory_links(link_type)")
            
            # 复合索引（优化查询性能）
            conn.execute("CREATE INDEX IF NOT EXISTS idx_links_type_strength ON memory_links(link_type, strength DESC)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_links_created ON memory_links(created_at DESC)")
    
    def _load(self):
        """从数据库加载"""
        with self.transaction() as conn:
            # 加载关联
            cursor = conn.execute("SELECT * FROM memory_links")
            for row in cursor.fetchall():
                link = MemoryLink(
                    id=row['id'],
                    source_id=row['source_id'],
                    target_id=row['target_id'],
                    link_type=row['link_type'],
                    strength=row['strength'],
                    metadata=json.loads(row['metadata']) if row['metadata'] else {},
                    created_at=row['created_at']
                )
                self.links.append(link)
            
            # 加载记忆链
            cursor = conn.execute("SELECT * FROM memory_chains")
            for row in cursor.fetchall():
                chain = MemoryChain(
                    id=row['id'],
                    memories=json.loads(row['memories']),
                    chain_type=row['chain_type'],
                    total_strength=row['total_strength'],
                    metadata=json.loads(row['metadata']) if row['metadata'] else {},
                    created_at=row['created_at']
                )
                self.chains[chain.id] = chain
    
    def _save_link(self, link: MemoryLink):
        """保存关联"""
        with self.transaction() as conn:
            conn.execute("""
                INSERT INTO memory_links (source_id, target_id, link_type, strength, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                link.source_id,
                link.target_id,
                link.link_type,
                link.strength,
                json.dumps(link.metadata, ensure_ascii=False)
            ))
    
    def _save_chain(self, chain: MemoryChain):
        """保存记忆链"""
        with self.transaction() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO memory_chains 
                (id, memories, chain_type, total_strength, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                chain.id,
                json.dumps(chain.memories, ensure_ascii=False),
                chain.chain_type,
                chain.total_strength,
                json.dumps(chain.metadata, ensure_ascii=False)
            ))
    
    # ========== 多维度相似度计算 ==========
    
    def calculate_similarity(self, mem1: Dict, mem2: Dict) -> Dict[str, float]:
        """
        计算多维度相似度
        
        参数:
            mem1: 记忆 1 数据
            mem2: 记忆 2 数据
        
        返回:
            各维度相似度字典
        """
        scores = {}
        
        # 1. 主题相似度（基于标签/类别）
        scores['thematic'] = self._thematic_similarity(mem1, mem2)
        
        # 2. 实体相似度（共享概念/关键词）
        scores['entity'] = self._entity_similarity(mem1, mem2)
        
        # 3. 时间接近度
        scores['temporal'] = self._temporal_similarity(mem1, mem2)
        
        # 4. 情感相似度
        scores['emotional'] = self._emotional_similarity(mem1, mem2)
        
        # 5. 语义相似度（基于内容文本）
        scores['semantic'] = self._semantic_similarity(mem1, mem2)
        
        # 计算加权总分
        weights = {
            'thematic': 0.25,
            'entity': 0.25,
            'temporal': 0.15,
            'emotional': 0.15,
            'semantic': 0.20
        }
        
        scores['total'] = sum(scores[k] * weights[k] for k in weights)
        
        return scores
    
    def _thematic_similarity(self, mem1: Dict, mem2: Dict) -> float:
        """主题相似度（基于标签）"""
        tags1 = set(mem1.get('tags', []))
        tags2 = set(mem2.get('tags', []))
        
        if not tags1 or not tags2:
            # 使用事件类型作为备选
            type1 = mem1.get('event_type', '')
            type2 = mem2.get('event_type', '')
            return 1.0 if type1 == type2 else 0.0
        
        # Jaccard 相似度
        intersection = len(tags1 & tags2)
        union = len(tags1 | tags2)
        return intersection / union if union > 0 else 0.0
    
    def _entity_similarity(self, mem1: Dict, mem2: Dict) -> float:
        """实体相似度（共享概念）"""
        entities1 = set(mem1.get('entities', []))
        entities2 = set(mem2.get('entities', []))
        
        if not entities1 or not entities2:
            # 从内容中提取关键词作为备选
            content1 = str(mem1.get('content', {}))
            content2 = str(mem2.get('content', {}))
            # 简单关键词提取（实际应该用 NLP）
            words1 = set(w.lower() for w in content1.split() if len(w) > 4)
            words2 = set(w.lower() for w in content2.split() if len(w) > 4)
            if not words1 or not words2:
                return 0.0
            intersection = len(words1 & words2)
            total = len(words1 | words2)
            return intersection / total if total > 0 else 0.0
        
        # 计算共享实体比例
        intersection = len(entities1 & entities2)
        return min(1.0, intersection / max(len(entities1), len(entities2)))
    
    def _temporal_similarity(self, mem1: Dict, mem2: Dict) -> float:
        """时间接近度"""
        time1_str = mem1.get('created_at') or mem1.get('timestamp')
        time2_str = mem2.get('created_at') or mem2.get('timestamp')
        
        if not time1_str or not time2_str:
            return 0.0
        
        try:
            time1 = datetime.fromisoformat(time1_str[:19])
            time2 = datetime.fromisoformat(time2_str[:19])
        except:
            return 0.0
        
        diff_hours = abs((time1 - time2).total_seconds()) / 3600
        
        # 24 小时内为 1.0，7 天内线性衰减到 0
        if diff_hours < 24:
            return 1.0
        elif diff_hours < 168:  # 7 天
            return max(0.0, 1.0 - (diff_hours - 24) / 144)
        else:
            return 0.0
    
    def _emotional_similarity(self, mem1: Dict, mem2: Dict) -> float:
        """情感相似度"""
        emotion1 = mem1.get('emotion', {})
        emotion2 = mem2.get('emotion', {})
        
        if not emotion1 or not emotion2:
            return 0.5  # 中性
        
        # 情感类型相同得 1 分
        type1 = emotion1.get('type', 'neutral')
        type2 = emotion2.get('type', 'neutral')
        
        if type1 == type2:
            return 1.0
        
        # 情感相似组
        similar_groups = [
            {'joy', 'excitement', 'pride', 'happiness'},
            {'sadness', 'disappointment', 'grief', 'sorrow'},
            {'anger', 'frustration', 'annoyance', 'rage'},
            {'fear', 'anxiety', 'worry', 'nervousness'},
            {'surprise', 'amazement', 'shock'},
        ]
        
        for group in similar_groups:
            if type1 in group and type2 in group:
                return 0.7
        
        # 效价（正面/负面）相同
        valence1 = emotion1.get('valence', 'neutral')
        valence2 = emotion2.get('valence', 'neutral')
        if valence1 == valence2 and valence1 != 'neutral':
            return 0.5
        
        return 0.0
    
    def _semantic_similarity(self, mem1: Dict, mem2: Dict) -> float:
        """语义相似度（基于内容）"""
        content1 = str(mem1.get('content', {}))
        content2 = str(mem2.get('content', {}))
        
        # 简单实现：词重叠度
        # 实际应该用词向量或嵌入
        words1 = set(content1.lower().split())
        words2 = set(content2.lower().split())
        
        # 过滤停用词
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                     '的', '了', '在', '是', '我', '有', '和'}
        words1 = words1 - stop_words
        words2 = words2 - stop_words
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union if union > 0 else 0.0
    
    # ========== 关联发现 ==========
    
    def find_related_memories(self, 
                             current_memory: Dict,
                             all_memories: List[Dict],
                             min_strength: float = 0.5,
                             limit: int = 10) -> List[Tuple[Dict, float]]:
        """
        查找相关记忆
        
        参数:
            current_memory: 当前记忆
            all_memories: 所有记忆列表
            min_strength: 最小关联强度
            limit: 返回数量限制
        
        返回:
            [(记忆，关联强度), ...]
        """
        results = []
        
        for memory in all_memories:
            if memory.get('id') == current_memory.get('id'):
                continue
            
            # 计算相似度
            scores = self.calculate_similarity(current_memory, memory)
            total_score = scores['total']
            
            if total_score >= min_strength:
                results.append((memory, total_score))
        
        # 按强度排序
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:limit]
    
    def discover_links(self,
                      memories: List[Dict],
                      min_strength: float = 0.6) -> int:
        """
        批量发现记忆关联
        
        参数:
            memories: 记忆列表
            min_strength: 最小关联强度
        
        返回:
            发现的关联数量
        """
        links_created = 0
        
        for i, mem1 in enumerate(memories):
            for mem2 in memories[i+1:]:
                scores = self.calculate_similarity(mem1, mem2)
                
                if scores['total'] >= min_strength:
                    # 找出最强的维度
                    best_type = max(scores, key=lambda k: scores[k] if k != 'total' else 0)
                    
                    # 创建关联
                    link = MemoryLink(
                        id=0,  # 自动增长
                        source_id=mem1.get('id', str(uuid.uuid4())),
                        target_id=mem2.get('id', str(uuid.uuid4())),
                        link_type=best_type,
                        strength=scores['total'],
                        metadata={
                            'scores': scores,
                            'auto_discovered': True
                        }
                    )
                    
                    self.links.append(link)
                    self._save_link(link)
                    links_created += 1
        
        return links_created
    
    # ========== 记忆链生成 ==========
    
    def create_memory_chain(self,
                           seed_memory: Dict,
                           all_memories: List[Dict],
                           max_length: int = 10,
                           min_strength: float = 0.5) -> MemoryChain:
        """
        创建记忆链（关联序列）
        
        参数:
            seed_memory: 种子记忆
            all_memories: 所有记忆
            max_length: 最大长度
            min_strength: 最小关联强度
        
        返回:
            MemoryChain 对象
        """
        chain_memories = [seed_memory.get('id', 'seed')]
        visited = {seed_memory.get('id', 'seed')}
        
        current = seed_memory
        total_strength = 1.0
        
        for _ in range(max_length - 1):
            # 查找相关的未访问记忆
            related = self.find_related_memories(
                current, 
                all_memories,
                min_strength=min_strength,
                limit=10
            )
            
            next_memory = None
            link_strength = 0.0
            
            for mem, strength in related:
                mem_id = mem.get('id', '')
                if mem_id not in visited:
                    next_memory = mem
                    link_strength = strength
                    break
            
            if not next_memory:
                break
            
            # 添加到链
            next_id = next_memory.get('id', str(uuid.uuid4()))
            chain_memories.append(next_id)
            visited.add(next_id)
            total_strength *= link_strength
            
            current = next_memory
        
        # 创建记忆链
        chain = MemoryChain(
            id=f"chain_{uuid.uuid4().hex[:12]}",
            memories=chain_memories,
            chain_type='associative',
            total_strength=total_strength,
            metadata={
                'seed_id': seed_memory.get('id', 'seed'),
                'discovery_method': 'greedy'
            }
        )
        
        self.chains[chain.id] = chain
        self._save_chain(chain)
        
        return chain
    
    def get_chain(self, chain_id: str) -> Optional[MemoryChain]:
        """获取记忆链"""
        return self.chains.get(chain_id)
    
    def list_chains(self, chain_type: str = None) -> List[MemoryChain]:
        """列出记忆链"""
        chains = list(self.chains.values())
        
        if chain_type:
            chains = [c for c in chains if c.chain_type == chain_type]
        
        return chains
    
    # ========== 上下文摘要 ==========
    
    def generate_context_summary(self,
                                current_memory: Dict,
                                related_memories: List[Dict]) -> ContextSummary:
        """
        生成上下文摘要
        
        参数:
            current_memory: 当前记忆
            related_memories: 相关记忆列表
        
        返回:
            ContextSummary 对象
        """
        # 收集主题
        all_tags = []
        for mem in [current_memory] + related_memories:
            all_tags.extend(mem.get('tags', []))
        
        themes = [tag for tag, count in Counter(all_tags).most_common(5)]
        
        # 收集实体
        all_entities = []
        for mem in [current_memory] + related_memories:
            all_entities.extend(mem.get('entities', []))
        
        entities = list(set(all_entities))[:10]
        
        # 计算时间跨度
        times = []
        for mem in [current_memory] + related_memories:
            time_str = mem.get('created_at') or mem.get('timestamp')
            if time_str:
                try:
                    times.append(datetime.fromisoformat(time_str[:19]))
                except:
                    pass
        
        if times:
            time_span = f"{min(times).date()} ~ {max(times).date()}"
        else:
            time_span = "unknown"
        
        # 生成摘要文本
        summary_parts = []
        
        # 当前记忆
        current_title = current_memory.get('title') or current_memory.get('event_type', 'Memory')
        summary_parts.append(f"当前：{current_title}")
        
        # 相关记忆
        if related_memories:
            summary_parts.append(f"\n相关记忆 ({len(related_memories)} 个):")
            for i, mem in enumerate(related_memories[:5], 1):
                title = mem.get('title') or mem.get('event_type', 'Memory')
                time_str = mem.get('created_at', '')[:10]
                summary_parts.append(f"  {i}. {title} ({time_str})")
        
        # 主题
        if themes:
            summary_parts.append(f"\n主题：{', '.join(themes)}")
        
        summary_text = '\n'.join(summary_parts)
        
        # 创建摘要对象
        summary = ContextSummary(
            current_memory=current_memory.get('id', 'current'),
            related_memories=[m.get('id', '') for m in related_memories],
            summary_text=summary_text,
            themes=themes,
            entities=entities,
            time_span=time_span,
            metadata={
                'total_related': len(related_memories),
                'generated_at': datetime.now().isoformat()
            }
        )
        
        return summary
    
    # ========== 统计信息 ==========
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        # 按类型统计关联
        by_type = {}
        for link in self.links:
            link_type = link.link_type
            by_type[link_type] = by_type.get(link_type, 0) + 1
        
        # 平均关联强度
        avg_strength = sum(l.strength for l in self.links) / len(self.links) if self.links else 0
        
        # 记忆链统计
        chain_stats = {
            'total': len(self.chains),
            'avg_length': sum(len(c.memories) for c in self.chains.values()) / len(self.chains) if self.chains else 0,
            'by_type': {}
        }
        
        for chain in self.chains.values():
            t = chain.chain_type
            chain_stats['by_type'][t] = chain_stats['by_type'].get(t, 0) + 1
        
        return {
            'total_links': len(self.links),
            'by_type': by_type,
            'avg_strength': avg_strength,
            'chains': chain_stats
        }
    
    def export_to_json(self, output_path: str) -> Tuple[int, int]:
        """导出为 JSON"""
        data = {
            'schema': 'memory_links.v1',
            'exported_at': datetime.now().isoformat(),
            'links': [l.to_dict() for l in self.links],
            'chains': [c.to_dict() for c in self.chains.values()]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return len(self.links), len(self.chains)


# ============================================================
# 测试
# ============================================================

def run_tests():
    """运行测试"""
    print("=" * 60)
    print("🧪 MemoryLinker 测试")
    print("=" * 60)
    
    import os
    test_db = os.path.expanduser("~/.openclaw/workspace/evolution/data/ml_test.db")
    linker = MemoryLinker(test_db)
    
    print("\n✅ 记忆关联器初始化成功")
    
    # 创建测试记忆
    print("\n【测试 1】创建测试记忆")
    memories = [
        {
            'id': 'mem_1',
            'event_type': 'capability_learned',
            'tags': ['learning', 'skill'],
            'entities': ['web_search', 'python'],
            'created_at': '2026-03-15T10:00:00',
            'emotion': {'type': 'joy', 'valence': 'positive'},
            'content': '学会了 web_search 能力'
        },
        {
            'id': 'mem_2',
            'event_type': 'skill_improved',
            'tags': ['learning', 'improvement'],
            'entities': ['python', 'coding'],
            'created_at': '2026-03-15T11:00:00',
            'emotion': {'type': 'excitement', 'valence': 'positive'},
            'content': '提升了 python 编程技能'
        },
        {
            'id': 'mem_3',
            'event_type': 'pattern_discovered',
            'tags': ['pattern', 'analysis'],
            'entities': ['data_analysis'],
            'created_at': '2026-03-14T10:00:00',
            'emotion': {'type': 'surprise', 'valence': 'positive'},
            'content': '发现了数据分析模式'
        }
    ]
    print(f"  ✅ 创建 3 个测试记忆")
    
    # 计算相似度
    print("\n【测试 2】相似度计算")
    scores = linker.calculate_similarity(memories[0], memories[1])
    print(f"  记忆 1 vs 记忆 2:")
    print(f"      主题：{scores['thematic']:.2f}")
    print(f"      实体：{scores['entity']:.2f}")
    print(f"      时间：{scores['temporal']:.2f}")
    print(f"      情感：{scores['emotional']:.2f}")
    print(f"      语义：{scores['semantic']:.2f}")
    print(f"      总分：{scores['total']:.2f}")
    
    # 发现关联
    print("\n【测试 3】发现关联")
    links = linker.discover_links(memories, min_strength=0.3)
    print(f"  ✅ 发现 {links} 个关联")
    
    # 查找相关记忆
    print("\n【测试 4】查找相关记忆")
    related = linker.find_related_memories(memories[0], memories, min_strength=0.3)
    print(f"  ✅ 找到 {len(related)} 个相关记忆")
    for mem, strength in related:
        print(f"      • {mem['id']}: {strength:.2f}")
    
    # 创建记忆链
    print("\n【测试 5】创建记忆链")
    chain = linker.create_memory_chain(memories[0], memories, max_length=5)
    print(f"  ✅ 创建记忆链：{chain.id}")
    print(f"      长度：{len(chain.memories)}")
    print(f"      总强度：{chain.total_strength:.2f}")
    
    # 生成上下文摘要
    print("\n【测试 6】生成上下文摘要")
    related_mems = [m for m, s in related]
    summary = linker.generate_context_summary(memories[0], related_mems)
    print(f"  📝 摘要:")
    print(f"      主题：{', '.join(summary.themes)}")
    print(f"      实体：{', '.join(summary.entities[:3])}")
    print(f"      时间：{summary.time_span}")
    
    # 统计信息
    print("\n【测试 7】统计信息")
    stats = linker.get_stats()
    print(f"  总关联数：{stats['total_links']}")
    print(f"  平均强度：{stats['avg_strength']:.2f}")
    print(f"  记忆链数：{stats['chains']['total']}")
    
    # 清理
    if os.path.exists(test_db):
        os.remove(test_db)
    
    print("\n" + "=" * 60)
    print("✅ MemoryLinker 测试完成")
    print("=" * 60)


if __name__ == '__main__':
    run_tests()
