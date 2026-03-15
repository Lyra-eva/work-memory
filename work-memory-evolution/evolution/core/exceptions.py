#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进化系统异常模块

提供友好的错误处理和错误提示

版本：v3.5.1
创建：2026-03-15
"""


# ============================================================
# 基础异常类
# ============================================================

class EvolutionError(Exception):
    """进化系统基础异常"""
    pass


# ============================================================
# 知识图谱异常
# ============================================================

class KnowledgeGraphError(EvolutionError):
    """知识图谱异常"""
    pass


class NodeNotFoundError(KnowledgeGraphError):
    """知识节点未找到"""
    
    def __init__(self, node_id: str, suggestions: list = None):
        self.node_id = node_id
        self.suggestions = suggestions or []
    
    def __str__(self):
        msg = f"❌ 知识节点未找到：{self.node_id}"
        if self.suggestions:
            msg += f"\n\n💡 建议检查以下相似节点:"
            for sug in self.suggestions[:3]:
                msg += f"\n   • {sug}"
        return msg


class NodeAlreadyExistsError(KnowledgeGraphError):
    """知识节点已存在"""
    
    def __init__(self, node_id: str):
        self.node_id = node_id
    
    def __str__(self):
        return f"❌ 知识节点已存在：{self.node_id}"


class RelationNotFoundError(KnowledgeGraphError):
    """知识关系未找到"""
    
    def __init__(self, source_id: str, target_id: str, relation_type: str = None):
        self.source_id = source_id
        self.target_id = target_id
        self.relation_type = relation_type
    
    def __str__(self):
        msg = f"❌ 知识关系未找到"
        msg += f"\n   源节点：{self.source_id}"
        msg += f"\n   目标节点：{self.target_id}"
        if self.relation_type:
            msg += f"\n   关系类型：{self.relation_type}"
        return msg


class InvalidNodeError(KnowledgeGraphError):
    """无效的知识节点"""
    
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
    
    def __str__(self):
        msg = f"❌ 无效的知识节点"
        if self.field:
            msg += f"\n   字段：{self.field}"
        msg += f"\n   原因：{self.message}"
        return msg


# ============================================================
# 记忆巩固异常
# ============================================================

class MemoryConsolidationError(EvolutionError):
    """记忆巩固异常"""
    pass


class MemoryNotFoundError(MemoryConsolidationError):
    """记忆项目未找到"""
    
    def __init__(self, memory_id: str):
        self.memory_id = memory_id
    
    def __str__(self):
        return f"❌ 记忆项目未找到：{self.memory_id}"


class InvalidRecallQualityError(MemoryConsolidationError):
    """无效的回忆质量值"""
    
    def __init__(self, quality: float):
        self.quality = quality
    
    def __str__(self):
        return f"❌ 无效的回忆质量：{self.quality:.2f}\n   有效范围：0.0 - 1.0"


class ReviewScheduleError(MemoryConsolidationError):
    """复习调度错误"""
    
    def __init__(self, message: str):
        self.message = message
    
    def __str__(self):
        return f"❌ 复习调度错误：{self.message}"


# ============================================================
# 记忆关联异常
# ============================================================

class MemoryLinkingError(EvolutionError):
    """记忆关联异常"""
    pass


class LinkNotFoundError(MemoryLinkingError):
    """记忆关联未找到"""
    
    def __init__(self, source_id: str, target_id: str):
        self.source_id = source_id
        self.target_id = target_id
    
    def __str__(self):
        return f"❌ 记忆关联未找到\n   源：{self.source_id} → 目标：{self.target_id}"


class InvalidSimilarityError(MemoryLinkingError):
    """无效的相似度计算"""
    
    def __init__(self, message: str):
        self.message = message
    
    def __str__(self):
        return f"❌ 相似度计算失败：{self.message}"


# ============================================================
# 概念提取异常
# ============================================================

class ConceptExtractionError(EvolutionError):
    """概念提取异常"""
    
    def __init__(self, message: str, source: str = None):
        self.message = message
        self.source = source
    
    def __str__(self):
        msg = f"❌ 概念提取失败：{self.message}"
        if self.source:
            msg += f"\n   来源：{self.source}"
        return msg


# ============================================================
# 数据库异常
# ============================================================

class DatabaseError(EvolutionError):
    """数据库操作异常"""
    
    def __init__(self, message: str, operation: str = None):
        self.message = message
        self.operation = operation
    
    def __str__(self):
        msg = f"❌ 数据库错误：{self.message}"
        if self.operation:
            msg += f"\n   操作：{self.operation}"
        return msg


class ConnectionError(DatabaseError):
    """数据库连接错误"""
    
    def __str__(self):
        return f"❌ 数据库连接失败：{self.message}"


# ============================================================
# 工具函数
# ============================================================

def validate_quality(quality: float) -> None:
    """验证回忆质量值"""
    if not 0.0 <= quality <= 1.0:
        raise InvalidRecallQualityError(quality)


def validate_mastery(mastery: float) -> None:
    """验证掌握度值"""
    if not 0.0 <= mastery <= 1.0:
        raise InvalidNodeError(f"掌握度必须在 0.0-1.0 之间", "mastery_level")


def validate_strength(strength: float) -> None:
    """验证关系强度值"""
    if not 0.0 <= strength <= 1.0:
        raise InvalidNodeError(f"关系强度必须在 0.0-1.0 之间", "strength")


def safe_get(dictionary: dict, key: str, default=None, required: bool = False) -> any:
    """安全获取字典值"""
    if key not in dictionary:
        if required:
            raise InvalidNodeError(f"缺少必需字段", key)
        return default
    return dictionary[key]
