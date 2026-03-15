#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
概念提取器 - Concept Extractor

从进化事件、对话、能力描述中自动提取概念
并整合到知识图谱

版本：v3.3.0
创建：2026-03-15
"""

import re
import json
from typing import List, Dict, Optional, Set
from datetime import datetime
from dataclasses import dataclass, field

try:
    from .knowledge_graph import (
        KnowledgeGraph, 
        KnowledgeNode, 
        KnowledgeRelation,
        create_node,
        create_relation
    )
except ImportError:
    from knowledge_graph import (
        KnowledgeGraph, 
        KnowledgeNode, 
        KnowledgeRelation,
        create_node,
        create_relation
    )


# ============================================================
# 配置
# ============================================================

# 常见停用词（中文 + 英文）
STOP_WORDS = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人',
    '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去',
    '你', '会', '着', '没有', '看', '好', '自己', '这', '那',
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'can', 'could', 'may', 'might', 'must', 'shall', 'should'
}

# 类别关键词映射
CATEGORY_KEYWORDS = {
    'skill': ['能力', '技能', '功能', 'capability', 'skill', 'ability', 'function'],
    'concept': ['概念', '原理', '理论', 'concept', 'theory', 'principle'],
    'fact': ['事实', '数据', '信息', 'fact', 'data', 'information'],
    'experience': ['经验', '案例', '实践', 'experience', 'case', 'practice']
}


# ============================================================
# 数据类
# ============================================================

@dataclass
class ExtractedConcept:
    """提取的概念"""
    name: str
    category: str
    source: str
    confidence: float
    definition: str = ""
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'name': self.name,
            'category': self.category,
            'source': self.source,
            'confidence': self.confidence,
            'definition': self.definition,
            'metadata': self.metadata
        }


# ============================================================
# 概念提取器
# ============================================================

class ConceptExtractor:
    """
    概念提取器
    
    功能:
    - 从文本中提取专业术语
    - 从进化事件中提取概念
    - 从能力描述中提取关键词
    - 自动分类和整合到知识图谱
    """
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        """初始化提取器"""
        self.kg = knowledge_graph
        self.term_pattern = re.compile(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b')
        self.cn_pattern = re.compile(r'[\u4e00-\u9fa5]{2,}')
    
    def extract_from_text(self, text: str, source: str = "text") -> List[ExtractedConcept]:
        """
        从文本中提取概念
        
        参数:
            text: 输入文本
            source: 来源标识
        
        返回:
            提取的概念列表
        """
        concepts = []
        
        # 提取英文术语（驼峰命名）
        en_terms = self.term_pattern.findall(text)
        for term in en_terms:
            if len(term) > 3 and term.lower() not in STOP_WORDS:
                concepts.append(ExtractedConcept(
                    name=term,
                    category=self._infer_category(term, text),
                    source=source,
                    confidence=0.6,
                    metadata={'language': 'en'}
                ))
        
        # 提取中文术语（2 字以上）
        cn_terms = self.cn_pattern.findall(text)
        for term in cn_terms:
            if term not in STOP_WORDS and len(term) >= 2:
                concepts.append(ExtractedConcept(
                    name=term,
                    category=self._infer_category(term, text),
                    source=source,
                    confidence=0.5,
                    metadata={'language': 'zh'}
                ))
        
        return concepts
    
    def extract_from_episode(self, episode_data: Dict) -> List[ExtractedConcept]:
        """
        从情景记忆事件中提取概念
        
        参数:
            episode_data: 情景记忆数据
        
        返回:
            提取的概念列表
        """
        concepts = []
        
        # 从事件类型提取
        event_type = episode_data.get('event_type', '')
        if event_type:
            concepts.append(ExtractedConcept(
                name=event_type,
                category='concept',
                source='event_type',
                confidence=0.8,
                definition=f"进化事件类型：{event_type}"
            ))
        
        # 从事件内容提取
        event_data = episode_data.get('data', {})
        for key, value in event_data.items():
            if isinstance(value, str) and len(value) > 3:
                text_concepts = self.extract_from_text(value, f"event_data.{key}")
                concepts.extend(text_concepts)
            
            # 能力名称作为核心概念
            if key in ['capability', 'skill', 'name'] and isinstance(value, str):
                concepts.append(ExtractedConcept(
                    name=value,
                    category='skill',
                    source=f'event_data.{key}',
                    confidence=0.9,
                    definition=f"从事件中提取的技能/能力"
                ))
        
        return concepts
    
    def extract_from_capability(self, capability_data: Dict) -> List[ExtractedConcept]:
        """
        从能力数据中提取概念
        
        参数:
            capability_data: 能力配置数据
        
        返回:
            提取的概念列表
        """
        concepts = []
        
        # 能力名称作为核心概念
        name = capability_data.get('name', '')
        if name:
            concepts.append(ExtractedConcept(
                name=name,
                category='skill',
                source='capability.name',
                confidence=0.95,
                definition=f"核心能力：{name}",
                metadata={
                    'version': capability_data.get('version', '1.0.0'),
                    'status': capability_data.get('status', 'active')
                }
            ))
        
        # 从描述中提取
        description = capability_data.get('description', '')
        if description:
            desc_concepts = self.extract_from_text(description, 'capability.description')
            concepts.extend(desc_concepts)
        
        # 从配置中提取关键词
        config = capability_data.get('config', {})
        for key, value in config.items():
            if isinstance(value, str) and len(value) > 5:
                concepts.append(ExtractedConcept(
                    name=f"{key}配置",
                    category='concept',
                    source=f'capability.config.{key}',
                    confidence=0.6,
                    definition=f"能力配置项：{key} = {value[:50]}"
                ))
        
        return concepts
    
    def extract_from_evolution_event(self, event_data: Dict) -> List[ExtractedConcept]:
        """
        从进化事件中提取概念
        
        参数:
            event_data: 进化事件数据
        
        返回:
            提取的概念列表
        """
        concepts = []
        
        # 事件类型
        event_type = event_data.get('event_type', '')
        if event_type:
            concepts.append(ExtractedConcept(
                name=event_type,
                category='concept',
                source='evolution_event.type',
                confidence=0.85
            ))
        
        # 从事件数据中提取
        data = event_data.get('data', {})
        
        # 能力相关
        if 'capability' in data:
            cap_name = data['capability']
            concepts.append(ExtractedConcept(
                name=cap_name,
                category='skill',
                source='evolution_event.data.capability',
                confidence=0.9,
                definition=f"进化事件中的能力：{cap_name}"
            ))
        
        # 技能相关
        if 'skill' in data:
            skill_name = data['skill']
            concepts.append(ExtractedConcept(
                name=skill_name,
                category='skill',
                source='evolution_event.data.skill',
                confidence=0.9
            ))
        
        # 模式相关
        if 'pattern' in data:
            pattern_name = data['pattern']
            concepts.append(ExtractedConcept(
                name=pattern_name,
                category='concept',
                source='evolution_event.data.pattern',
                confidence=0.8
            ))
        
        return concepts
    
    def _infer_category(self, term: str, context: str = "") -> str:
        """
        推断概念类别
        
        参数:
            term: 术语
            context: 上下文
        
        返回:
            类别标识
        """
        term_lower = term.lower()
        
        # 检查类别关键词
        for category, keywords in CATEGORY_KEYWORDS.items():
            if any(kw in term_lower or kw in context.lower() for kw in keywords):
                return category
        
        # 默认规则
        if term.endswith('ing') or term.endswith('tion') or term.endswith('ity'):
            return 'concept'
        
        if term[0].isupper() and len(term) > 3:
            return 'skill'
        
        return 'concept'  # 默认
    
    # ========== 概念整合 ==========
    
    def integrate_concepts(self, concepts: List[ExtractedConcept], 
                          min_confidence: float = 0.7) -> int:
        """
        整合概念到知识图谱
        
        参数:
            concepts: 提取的概念列表
            min_confidence: 最小置信度阈值
        
        返回:
            整合的概念数量
        """
        integrated = 0
        
        for concept in concepts:
            if concept.confidence < min_confidence:
                continue
            
            # 检查是否已存在
            existing = self._find_similar_concept(concept.name)
            
            if existing:
                # 更新现有节点
                self._update_concept(existing, concept)
            else:
                # 创建新节点
                self._create_concept(concept)
            
            integrated += 1
        
        return integrated
    
    def _find_similar_concept(self, name: str) -> Optional[KnowledgeNode]:
        """查找相似概念"""
        name_lower = name.lower().strip()
        
        # 精确匹配
        for node in self.kg.nodes.values():
            if node.name.lower().strip() == name_lower:
                return node
        
        # 包含匹配
        for node in self.kg.nodes.values():
            node_name_lower = node.name.lower().strip()
            if name_lower in node_name_lower or node_name_lower in name_lower:
                return node
        
        return None
    
    def _update_concept(self, existing: KnowledgeNode, new: ExtractedConcept):
        """更新现有概念"""
        # 更新掌握度（如果有）
        if 'mastery_level' in new.metadata:
            existing.mastery_level = max(existing.mastery_level, new.metadata['mastery_level'])
        
        # 更新元数据
        existing.metadata.update(new.metadata)
        existing.metadata['last_updated'] = datetime.now().isoformat()
        existing.metadata['update_count'] = existing.metadata.get('update_count', 0) + 1
        
        # 保存
        self.kg.update_node(existing.id, 
                           mastery_level=existing.mastery_level,
                           metadata=existing.metadata)
    
    def _create_concept(self, concept: ExtractedConcept):
        """创建新概念"""
        node = create_node(
            name=concept.name,
            category=concept.category,
            definition=concept.definition or f"从{concept.source}提取的概念",
            mastery=concept.metadata.get('mastery_level', 0.0),
            metadata={
                'source': concept.source,
                'confidence': concept.confidence,
                'created_from': 'concept_extractor',
                'created_at': datetime.now().isoformat()
            }
        )
        
        self.kg.add_node(node)
    
    # ========== 关系发现 ==========
    
    def discover_relations(self, source_data: Dict) -> int:
        """
        从数据中发现关系
        
        参数:
            source_data: 源数据（包含多个概念）
        
        返回:
            发现的关系数量
        """
        relations_created = 0
        
        # 从依赖配置中发现
        dependencies = source_data.get('dependencies', {})
        for target, deps in dependencies.items():
            target_node = self._find_similar_concept(target)
            if not target_node:
                continue
            
            for dep in deps:
                source_node = self._find_similar_concept(dep)
                if not source_node:
                    continue
                
                # 创建依赖关系
                relation = create_relation(
                    source_id=source_node.id,
                    target_id=target_node.id,
                    relation_type='depends_on',
                    strength=0.9,
                    evidence=['auto_discovered_from_config']
                )
                self.kg.add_relation(relation)
                relations_created += 1
        
        return relations_created
    
    # ========== 批量处理 ==========
    
    def process_evolution_events(self, events: List[Dict]) -> Dict:
        """
        批量处理进化事件
        
        参数:
            events: 进化事件列表
        
        返回:
            处理统计
        """
        stats = {
            'total_events': len(events),
            'concepts_extracted': 0,
            'concepts_integrated': 0,
            'relations_discovered': 0
        }
        
        all_concepts = []
        
        for event in events:
            # 提取概念
            concepts = self.extract_from_evolution_event(event)
            all_concepts.extend(concepts)
        
        stats['concepts_extracted'] = len(all_concepts)
        
        # 整合概念
        stats['concepts_integrated'] = self.integrate_concepts(all_concepts, min_confidence=0.6)
        
        return stats


# ============================================================
# 测试
# ============================================================

def run_tests():
    """运行测试"""
    print("=" * 60)
    print("🧪 ConceptExtractor 测试")
    print("=" * 60)
    
    # 初始化
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from knowledge_graph import KnowledgeGraph
    
    # 使用测试数据库
    test_db = os.path.expanduser("~/.openclaw/workspace/evolution/data/kg_test.db")
    kg = KnowledgeGraph(test_db)
    extractor = ConceptExtractor(kg)
    
    print("\n✅ 提取器初始化成功")
    
    # 测试 1: 从文本提取
    print("\n【测试 1】从文本提取")
    text = """
    Evolution Engine 是一个强大的进化框架。
    支持 Capability Learning 和 Pattern Mining。
    核心功能包括 Knowledge Graph 构建。
    """
    concepts = extractor.extract_from_text(text, "test_text")
    print(f"  提取到 {len(concepts)} 个概念:")
    for c in concepts[:5]:
        print(f"    • {c.name} ({c.category}, 置信度：{c.confidence})")
    
    # 测试 2: 从进化事件提取
    print("\n【测试 2】从进化事件提取")
    event = {
        'event_type': 'capability_learned',
        'data': {
            'capability': 'web_search',
            'description': '网络搜索能力，支持多引擎',
            'success': True
        }
    }
    concepts = extractor.extract_from_evolution_event(event)
    print(f"  提取到 {len(concepts)} 个概念:")
    for c in concepts:
        print(f"    • {c.name} ({c.category}, 来源：{c.source})")
    
    # 整合到知识图谱
    print("\n【测试 3】整合到知识图谱")
    count = extractor.integrate_concepts(concepts, min_confidence=0.7)
    print(f"  ✅ 整合 {count} 个概念")
    
    # 统计
    print("\n【测试 4】知识图谱统计")
    stats = kg.get_stats()
    print(f"  总节点数：{stats['total_nodes']}")
    print(f"  总关系数：{stats['total_relations']}")
    print(f"  平均掌握度：{stats['avg_mastery']:.2f}")
    
    # 清理测试数据库
    if os.path.exists(test_db):
        os.remove(test_db)
    
    print("\n" + "=" * 60)
    print("✅ ConceptExtractor 测试完成")
    print("=" * 60)


if __name__ == '__main__':
    run_tests()
