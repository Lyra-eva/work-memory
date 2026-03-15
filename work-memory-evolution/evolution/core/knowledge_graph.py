#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱核心模块 - Knowledge Graph Core

个体认知增强系统的基础模块
支持知识节点管理、关系发现、盲区识别、学习路径建议

版本：v3.3.0
创建：2026-03-15
"""

import json
import os
import sqlite3
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field, asdict
from contextlib import contextmanager
import uuid

try:
    from .exceptions import (
        NodeNotFoundError,
        NodeAlreadyExistsError,
        RelationNotFoundError,
        InvalidNodeError,
        DatabaseError
    )
except ImportError:
    from exceptions import (
        NodeNotFoundError,
        NodeAlreadyExistsError,
        RelationNotFoundError,
        InvalidNodeError,
        DatabaseError
    )


# ============================================================
# 配置
# ============================================================

WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")
EVOLUTION_DIR = os.path.join(WORKSPACE_DIR, 'evolution')
DATA_DIR = os.path.join(EVOLUTION_DIR, 'data')
KG_DB_PATH = os.path.join(DATA_DIR, 'knowledge_graph.db')


# ============================================================
# 数据类定义
# ============================================================

@dataclass
class KnowledgeNode:
    """知识节点"""
    id: str
    name: str
    category: str  # concept, skill, fact, experience
    definition: str
    mastery_level: float = 0.0  # 0-1 掌握程度
    related_nodes: Dict[str, float] = field(default_factory=dict)  # {node_id: strength}
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'KnowledgeNode':
        """从字典创建"""
        return cls(**data)


@dataclass
class KnowledgeRelation:
    """知识关系"""
    source_id: str
    target_id: str
    relation_type: str  # depends_on, similar_to, part_of, causes, used_for
    strength: float = 1.0  # 0-1 关系强度
    evidence: List[str] = field(default_factory=list)  # 支持证据
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'KnowledgeRelation':
        """从字典创建"""
        return cls(**data)


# ============================================================
# 知识图谱核心类
# ============================================================

class KnowledgeGraph:
    """
    知识图谱管理器
    
    功能:
    - 知识节点 CRUD
    - 关系管理
    - 知识盲区发现
    - 学习路径规划
    - 概念相似度计算
    """
    
    def __init__(self, db_path: str = KG_DB_PATH):
        """初始化知识图谱"""
        self.db_path = db_path
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.relations: List[KnowledgeRelation] = []
        self._conn = None
        self._init_db()
        # 内存数据库不需要加载
        if db_path != ":memory:":
            self._load()
    
    @contextmanager
    def transaction(self):
        """事务上下文管理器"""
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
        """初始化数据库架构"""
        with self.transaction() as conn:
            # 知识节点表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_nodes (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    definition TEXT,
                    mastery_level REAL DEFAULT 0.0,
                    related_nodes JSON DEFAULT '{}',
                    metadata JSON DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 知识关系表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS knowledge_relations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    relation_type TEXT NOT NULL,
                    strength REAL DEFAULT 1.0,
                    evidence JSON DEFAULT '[]',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (source_id) REFERENCES knowledge_nodes(id),
                    FOREIGN KEY (target_id) REFERENCES knowledge_nodes(id)
                )
            """)
            
            # 创建索引
            conn.execute("CREATE INDEX IF NOT EXISTS idx_kg_category ON knowledge_nodes(category)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_kg_mastery ON knowledge_nodes(mastery_level)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_kg_relations_source ON knowledge_relations(source_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_kg_relations_target ON knowledge_relations(target_id)")
            
            # 复合索引（优化查询性能）
            conn.execute("CREATE INDEX IF NOT EXISTS idx_kg_category_mastery ON knowledge_nodes(category, mastery_level)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_kg_created ON knowledge_nodes(created_at DESC)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_kg_relations_type ON knowledge_relations(relation_type)")
    
    def _load(self):
        """从数据库加载数据"""
        with self.transaction() as conn:
            # 加载节点
            cursor = conn.execute("SELECT * FROM knowledge_nodes")
            for row in cursor.fetchall():
                node = KnowledgeNode(
                    id=row['id'],
                    name=row['name'],
                    category=row['category'],
                    definition=row['definition'] or '',
                    mastery_level=row['mastery_level'],
                    related_nodes=json.loads(row['related_nodes']) if row['related_nodes'] else {},
                    metadata=json.loads(row['metadata']) if row['metadata'] else {},
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                self.nodes[node.id] = node
            
            # 加载关系
            cursor = conn.execute("SELECT * FROM knowledge_relations")
            for row in cursor.fetchall():
                relation = KnowledgeRelation(
                    source_id=row['source_id'],
                    target_id=row['target_id'],
                    relation_type=row['relation_type'],
                    strength=row['strength'],
                    evidence=json.loads(row['evidence']) if row['evidence'] else [],
                    created_at=row['created_at']
                )
                self.relations.append(relation)
    
    def _save_node(self, node: KnowledgeNode):
        """保存节点到数据库"""
        with self.transaction() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO knowledge_nodes 
                (id, name, category, definition, mastery_level, related_nodes, metadata, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                node.id,
                node.name,
                node.category,
                node.definition,
                node.mastery_level,
                json.dumps(node.related_nodes, ensure_ascii=False),
                json.dumps(node.metadata, ensure_ascii=False),
                node.created_at,
                datetime.now().isoformat()
            ))
    
    def _save_relation(self, relation: KnowledgeRelation):
        """保存关系到数据库"""
        with self.transaction() as conn:
            conn.execute("""
                INSERT INTO knowledge_relations (source_id, target_id, relation_type, strength, evidence)
                VALUES (?, ?, ?, ?, ?)
            """, (
                relation.source_id,
                relation.target_id,
                relation.relation_type,
                relation.strength,
                json.dumps(relation.evidence, ensure_ascii=False)
            ))
    
    # ========== 节点管理 ==========
    
    def add_node(self, node: KnowledgeNode) -> str:
        """添加知识节点"""
        self.nodes[node.id] = node
        self._save_node(node)
        return node.id
    
    def get_node(self, node_id: str, raise_not_found: bool = False) -> Optional[KnowledgeNode]:
        """获取知识节点
        
        参数:
            node_id: 节点 ID
            raise_not_found: 未找到时是否抛出异常
        
        返回:
            KnowledgeNode 对象或 None
        
        异常:
            NodeNotFoundError: 当 raise_not_found=True 且节点不存在时
        """
        node = self.nodes.get(node_id)
        
        if node is None and raise_not_found:
            # 查找相似节点作为建议
            suggestions = self._find_similar_node_ids(node_id, limit=3)
            raise NodeNotFoundError(node_id, suggestions)
        
        return node
    
    def _find_similar_node_ids(self, node_id: str, limit: int = 3) -> List[str]:
        """查找相似的节点 ID（用于错误提示）"""
        node_id_lower = node_id.lower()
        similar = []
        
        for nid in self.nodes.keys():
            # 检查是否包含或相似
            if node_id_lower in nid.lower() or nid.lower() in node_id_lower:
                similar.append(nid)
        
        # 按相似度排序（简单版本）
        similar.sort(key=lambda x: abs(len(x) - len(node_id)))
        return similar[:limit]
    
    def update_node(self, node_id: str, **kwargs) -> bool:
        """更新知识节点
        
        参数:
            node_id: 节点 ID
            **kwargs: 要更新的字段
        
        返回:
            bool: 是否更新成功
        
        异常:
            NodeNotFoundError: 节点不存在
            InvalidNodeError: 参数值无效
        """
        node = self.nodes.get(node_id)
        if not node:
            raise NodeNotFoundError(node_id)
        
        # 验证并更新字段
        for key, value in kwargs.items():
            if not hasattr(node, key):
                continue
            
            # 验证掌握度
            if key == 'mastery_level':
                if not 0.0 <= value <= 1.0:
                    raise InvalidNodeError(f"掌握度必须在 0.0-1.0 之间，当前值：{value}", "mastery_level")
            
            setattr(node, key, value)
        
        node.updated_at = datetime.now().isoformat()
        self._save_node(node)
        return True
    
    def delete_node(self, node_id: str) -> bool:
        """删除知识节点"""
        if node_id not in self.nodes:
            return False
        
        # 删除相关关系
        self.relations = [r for r in self.relations 
                         if r.source_id != node_id and r.target_id != node_id]
        
        del self.nodes[node_id]
        
        with self.transaction() as conn:
            conn.execute("DELETE FROM knowledge_nodes WHERE id = ?", (node_id,))
            conn.execute("DELETE FROM knowledge_relations WHERE source_id = ? OR target_id = ?", 
                        (node_id, node_id))
        
        return True
    
    def list_nodes(self, category: str = None, min_mastery: float = None) -> List[KnowledgeNode]:
        """列出知识节点"""
        nodes = list(self.nodes.values())
        
        if category:
            nodes = [n for n in nodes if n.category == category]
        
        if min_mastery is not None:
            nodes = [n for n in nodes if n.mastery_level >= min_mastery]
        
        return nodes
    
    # ========== 关系管理 ==========
    
    def add_relation(self, relation: KnowledgeRelation) -> int:
        """添加知识关系"""
        self.relations.append(relation)
        self._save_relation(relation)
        
        # 更新源节点的相关性
        source = self.nodes.get(relation.source_id)
        if source:
            source.related_nodes[relation.target_id] = relation.strength
            self._save_node(source)
        
        return len(self.relations)
    
    def get_relations(self, node_id: str, relation_type: str = None) -> List[KnowledgeRelation]:
        """获取节点的关系"""
        relations = [r for r in self.relations if r.source_id == node_id or r.target_id == node_id]
        
        if relation_type:
            relations = [r for r in relations if r.relation_type == relation_type]
        
        return relations
    
    def find_path(self, from_id: str, to_id: str, max_depth: int = 5) -> Optional[List[str]]:
        """查找两个节点之间的路径（BFS）"""
        if from_id == to_id:
            return [from_id]
        
        # 构建邻接表
        adj = {}
        for r in self.relations:
            if r.source_id not in adj:
                adj[r.source_id] = []
            if r.target_id not in adj:
                adj[r.target_id] = []
            adj[r.source_id].append(r.target_id)
            adj[r.target_id].append(r.source_id)  # 无向图
        
        # BFS
        from collections import deque
        queue = deque([(from_id, [from_id])])
        visited = {from_id}
        
        while queue:
            current, path = queue.popleft()
            
            if len(path) > max_depth:
                continue
            
            for neighbor in adj.get(current, []):
                if neighbor == to_id:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None  # 无路径
    
    # ========== 知识盲区发现 ==========
    
    def find_knowledge_gaps(self, target_node_id: str) -> List[str]:
        """
        发现知识盲区
        
        反向遍历依赖关系，找出缺失的前置知识
        """
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
        
        check_dependencies(target_node_id)
        return gaps
    
    def get_prerequisites(self, node_id: str) -> List[str]:
        """获取前置知识节点 ID 列表"""
        prereqs = []
        
        for rel in self.relations:
            if rel.target_id == node_id and rel.relation_type == 'depends_on':
                prereqs.append(rel.source_id)
        
        return prereqs
    
    # ========== 学习路径规划 ==========
    
    def suggest_learning_path(self, goal_node_id: str) -> List[str]:
        """
        建议学习路径
        
        按依赖关系排序，先学前置知识
        """
        gaps = self.find_knowledge_gaps(goal_node_id)
        
        if not gaps:
            return [goal_node_id]  # 无需补充，直接学目标
        
        # 拓扑排序
        path = []
        remaining = set(gaps)
        
        while remaining:
            # 找出没有未学习依赖的节点
            ready = []
            for node_id in remaining:
                deps = self.get_prerequisites(node_id)
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
    
    # ========== 概念相似度 ==========
    
    def calculate_similarity(self, node1_id: str, node2_id: str) -> float:
        """计算两个概念的相似度"""
        node1 = self.nodes.get(node1_id)
        node2 = self.nodes.get(node2_id)
        
        if not node1 or not node2:
            return 0.0
        
        # 1. 类别相同得分
        category_score = 1.0 if node1.category == node2.category else 0.0
        
        # 2. 共享邻居得分
        neighbors1 = set(node1.related_nodes.keys())
        neighbors2 = set(node2.related_nodes.keys())
        shared_neighbors = len(neighbors1 & neighbors2)
        total_neighbors = len(neighbors1 | neighbors2)
        neighbor_score = shared_neighbors / total_neighbors if total_neighbors > 0 else 0.0
        
        # 3. 名称相似度（简单版本）
        name1_lower = node1.name.lower()
        name2_lower = node2.name.lower()
        if name1_lower == name2_lower:
            name_score = 1.0
        elif name1_lower in name2_lower or name2_lower in name1_lower:
            name_score = 0.5
        else:
            name_score = 0.0
        
        # 加权平均
        similarity = (category_score * 0.4 + neighbor_score * 0.4 + name_score * 0.2)
        return similarity
    
    # ========== 统计信息 ==========
    
    def get_stats(self) -> Dict:
        """获取知识图谱统计"""
        stats = {
            'total_nodes': len(self.nodes),
            'total_relations': len(self.relations),
            'by_category': {},
            'avg_mastery': 0.0,
            'avg_relations_per_node': 0.0
        }
        
        # 按类别统计
        for node in self.nodes.values():
            cat = node.category
            stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1
        
        # 平均掌握度
        if self.nodes:
            stats['avg_mastery'] = sum(n.mastery_level for n in self.nodes.values()) / len(self.nodes)
        
        # 平均每节点关系数
        if self.nodes:
            stats['avg_relations_per_node'] = len(self.relations) / len(self.nodes)
        
        return stats
    
    def export_to_json(self, output_path: str):
        """导出为 JSON"""
        data = {
            'schema': 'knowledge_graph.v1',
            'exported_at': datetime.now().isoformat(),
            'nodes': [n.to_dict() for n in self.nodes.values()],
            'relations': [r.to_dict() for r in self.relations]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return len(self.nodes), len(self.relations)
    
    def import_from_json(self, input_path: str):
        """从 JSON 导入"""
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 导入节点
        for node_data in data.get('nodes', []):
            node = KnowledgeNode.from_dict(node_data)
            self.add_node(node)
        
        # 导入关系
        for rel_data in data.get('relations', []):
            relation = KnowledgeRelation.from_dict(rel_data)
            self.add_relation(relation)
        
        return len(data.get('nodes', [])), len(data.get('relations', []))


# ============================================================
# 便捷函数
# ============================================================

def create_node(name: str, category: str, definition: str, 
                mastery: float = 0.0, metadata: Dict = None) -> KnowledgeNode:
    """创建知识节点"""
    return KnowledgeNode(
        id=f"kg_{name.lower().replace(' ', '_')}_{uuid.uuid4().hex[:8]}",
        name=name,
        category=category,
        definition=definition,
        mastery_level=mastery,
        metadata=metadata or {}
    )


def create_relation(source_id: str, target_id: str, relation_type: str,
                   strength: float = 1.0, evidence: List[str] = None) -> KnowledgeRelation:
    """创建知识关系"""
    return KnowledgeRelation(
        source_id=source_id,
        target_id=target_id,
        relation_type=relation_type,
        strength=strength,
        evidence=evidence or []
    )


# ============================================================
# 测试
# ============================================================

def run_tests():
    """运行测试"""
    print("=" * 60)
    print("🧪 KnowledgeGraph 测试")
    print("=" * 60)
    
    # 初始化
    kg = KnowledgeGraph()
    print("\n✅ 知识图谱初始化成功")
    
    # 添加节点
    node1 = create_node("Web Search", "skill", "网络搜索能力", mastery=0.8)
    node2 = create_node("Search Strategy", "concept", "搜索策略概念", mastery=0.6)
    node3 = create_node("Keyword Extraction", "skill", "关键词提取技能", mastery=0.4)
    
    kg.add_node(node1)
    kg.add_node(node2)
    kg.add_node(node3)
    print(f"✅ 添加 3 个节点")
    
    # 添加关系
    rel1 = create_relation(node3.id, node2.id, "depends_on", strength=0.9)
    rel2 = create_relation(node2.id, node1.id, "used_for", strength=0.8)
    
    kg.add_relation(rel1)
    kg.add_relation(rel2)
    print(f"✅ 添加 2 个关系")
    
    # 查询
    print(f"\n📊 统计信息:")
    stats = kg.get_stats()
    print(f"   总节点数：{stats['total_nodes']}")
    print(f"   总关系数：{stats['total_relations']}")
    print(f"   平均掌握度：{stats['avg_mastery']:.2f}")
    
    # 盲区发现
    gaps = kg.find_knowledge_gaps(node1.id)
    print(f"\n🔍 知识盲区：{len(gaps)} 个")
    for gap_id in gaps:
        gap = kg.get_node(gap_id)
        if gap:
            print(f"   • {gap.name} (掌握度：{gap.mastery_level:.1%})")
    
    # 学习路径
    path = kg.suggest_learning_path(node1.id)
    print(f"\n📚 学习路径:")
    for i, node_id in enumerate(path, 1):
        node = kg.get_node(node_id)
        if node:
            print(f"   {i}. {node.name}")
    
    # 导出
    output_path = os.path.join(DATA_DIR, 'kg_export_test.json')
    nodes, rels = kg.export_to_json(output_path)
    print(f"\n💾 导出测试：{nodes} 节点，{rels} 关系 → {output_path}")
    
    print("\n" + "=" * 60)
    print("✅ KnowledgeGraph 测试完成")
    print("=" * 60)


if __name__ == '__main__':
    run_tests()
