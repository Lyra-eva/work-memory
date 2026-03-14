#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进化事件总线 - 记忆系统集成版

将进化事件存储到记忆系统，实现统一管理

版本：3.1.0 (记忆集成版)
创建：2026-03-12
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field, asdict
from enum import Enum


# ============================================================
# 配置
# ============================================================

WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE_DIR, 'memory')
EVOLUTION_DIR = os.path.join(MEMORY_DIR, 'evolution')
EVENTS_FILE = os.path.join(EVOLUTION_DIR, 'events.jsonl')
INDEX_FILE = os.path.join(EVOLUTION_DIR, 'index.json')
STATS_FILE = os.path.join(EVOLUTION_DIR, 'stats.json')


# ============================================================
# 枚举定义
# ============================================================

class EvolutionEventType(Enum):
    """进化事件类型"""
    CAPABILITY_LEARNED = "capability_learned"
    CAPABILITY_UPDATED = "capability_updated"
    CAPABILITY_DEPRECATED = "capability_deprecated"
    MEMORY_CONSOLIDATED = "memory_consolidated"
    PATTERN_DISCOVERED = "pattern_discovered"
    SKILL_IMPROVED = "skill_improved"
    CONFIG_UPDATED = "config_updated"


class ValidationStatus(Enum):
    """验证状态"""
    PENDING = "pending"
    VALIDATED = "validated"
    FAILED = "failed"
    WARNING = "warning"


class ValidationLevel(Enum):
    """验证级别"""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"


@dataclass
class ValidationTaskResult:
    """验证任务结果"""
    item_id: str
    item_type: str
    status: ValidationStatus
    level: ValidationLevel
    passed_checks: List[str] = field(default_factory=list)
    failed_checks: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    score: float = 0.0
    message: str = ""
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ============================================================
# 数据类定义
# ============================================================

@dataclass
class EvolutionEvent:
    """进化事件"""
    event_type: str
    agent_id: str
    timestamp: str
    data: Dict
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EvolutionEvent':
        return cls(**data)


# ============================================================
# 进化事件总线（记忆集成版）
# ============================================================

class EvolutionEventBus:
    """
    进化事件总线 - 记忆系统集成版
    
    功能:
    - 发布进化事件到记忆系统
    - 从记忆系统查询事件历史
    - 统计个人进化数据
    - 支持事件订阅与通知
    """
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self._init_storage()
        self._load_index()
    
    def _init_storage(self):
        """初始化存储"""
        os.makedirs(EVOLUTION_DIR, exist_ok=True)
        
        # 如果文件不存在，创建空文件
        if not os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
                pass
        
        if not os.path.exists(INDEX_FILE):
            self._rebuild_index()
    
    def _load_index(self):
        """加载索引"""
        if os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
        else:
            self.index = {'events': [], 'total_events': 0}
    
    def _rebuild_index(self):
        """重建索引"""
        events = []
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        event = json.loads(line)
                        events.append({
                            'id': event.get('id', len(events) + 1),
                            'event_type': event['event_type'],
                            'agent_id': event['agent_id'],
                            'timestamp': event['timestamp'],
                            'importance': event['importance']
                        })
        
        self.index = {
            'schema': 'evolution.index.v1',
            'created_at': datetime.now().isoformat(),
            'total_events': len(events),
            'events': events
        }
        
        self._save_index()
    
    def _save_index(self):
        """保存索引"""
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)
    
    def _save_stats(self):
        """保存统计"""
        events = self.get_event_history(limit=1000)
        
        stats = {
            'schema': 'evolution.stats.v1',
            'generated_at': datetime.now().isoformat(),
            'total_events': len(events),
            'by_type': {},
            'by_agent': {},
            'importance_avg': sum(e.importance for e in events) / len(events) if events else 0
        }
        
        for e in events:
            stats['by_type'][e.event_type] = stats['by_type'].get(e.event_type, 0) + 1
            stats['by_agent'][e.agent_id] = stats['by_agent'].get(e.agent_id, 0) + 1
        
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
    
    def publish(self, event: EvolutionEvent) -> str:
        """发布事件"""
        # 生成事件 ID
        event_id = str(self.index.get('total_events', 0) + 1)
        
        # 创建完整事件记录
        event_record = {
            'schema': 'evolution.event.v1',
            'id': int(event_id),
            'event_type': event.event_type,
            'agent_id': event.agent_id,
            'timestamp': event.timestamp,
            'data': event.data,
            'importance': event.importance,
            'tags': event.tags,
            'created_at': datetime.now().isoformat()
        }
        
        # 追加到 JSONL 文件
        with open(EVENTS_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event_record, ensure_ascii=False) + '\n')
        
        # 更新索引
        self.index['events'].append({
            'id': int(event_id),
            'event_type': event.event_type,
            'agent_id': event.agent_id,
            'timestamp': event.timestamp,
            'importance': event.importance
        })
        self.index['total_events'] = int(event_id)
        self._save_index()
        
        # 更新统计
        self._save_stats()
        
        # 通知订阅者
        self._notify_subscribers(event)
        
        return event_id
    
    def subscribe(self, event_type: str, callback: Callable):
        """订阅事件"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def get_event_history(self, agent_id: str = None, since: datetime = None,
                          event_type: str = None, limit: int = 100) -> List[EvolutionEvent]:
        """获取事件历史"""
        events = []
        
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            data = json.loads(line)
                            event = EvolutionEvent(
                                event_type=data['event_type'],
                                agent_id=data['agent_id'],
                                timestamp=data['timestamp'],
                                data=data['data'],
                                importance=data.get('importance', 0.5),
                                tags=data.get('tags', [])
                            )
                            events.append(event)
                        except:
                            continue
        
        # 过滤
        if agent_id:
            events = [e for e in events if e.agent_id == agent_id]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        if since:
            events = [e for e in events if e.timestamp >= since.isoformat()]
        
        # 按时间倒序
        events.sort(key=lambda e: e.timestamp, reverse=True)
        
        return events[:limit]
    
    def get_stats(self, agent_id: str = None) -> Dict:
        """获取事件统计"""
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                stats = json.load(f)
            
            if agent_id:
                # 重新计算特定智能体的统计
                events = self.get_event_history(agent_id=agent_id, limit=1000)
                return {
                    'total_events': len(events),
                    'by_type': self._count_by_field(events, 'event_type'),
                    'importance_avg': sum(e.importance for e in events) / len(events) if events else 0
                }
            
            return {
                'total_events': stats.get('total_events', 0),
                'by_type': stats.get('by_type', {}),
                'importance_avg': stats.get('importance_avg', 0)
            }
        
        return {'total_events': 0, 'by_type': {}}
    
    def _count_by_field(self, events: List[EvolutionEvent], field: str) -> Dict:
        """按字段计数"""
        counts = {}
        for e in events:
            value = getattr(e, field, 'unknown')
            counts[value] = counts.get(value, 0) + 1
        return counts
    
    def _notify_subscribers(self, event: EvolutionEvent):
        """通知订阅者"""
        if event.event_type in self.subscribers:
            for callback in self.subscribers[event.event_type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error notifying subscriber: {e}")
    
    def get_event_by_id(self, event_id: int) -> Optional[EvolutionEvent]:
        """根据 ID 查询事件"""
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            data = json.loads(line)
                            if data.get('id') == event_id:
                                return EvolutionEvent(
                                    event_type=data['event_type'],
                                    agent_id=data['agent_id'],
                                    timestamp=data['timestamp'],
                                    data=data['data'],
                                    importance=data.get('importance', 0.5),
                                    tags=data.get('tags', [])
                                )
                        except:
                            continue
        return None
    
    def export_events(self, output_path: str, agent_id: str = None):
        """导出事件"""
        events = self.get_event_history(agent_id=agent_id, limit=10000)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump([e.to_dict() for e in events], f, indent=2, ensure_ascii=False)
        
        return len(events)


# ============================================================
# 便捷函数
# ============================================================

def create_event(event_type: EvolutionEventType, agent_id: str, data: Dict,
                 importance: float = 0.5, tags: List[str] = None) -> EvolutionEvent:
    """创建进化事件"""
    return EvolutionEvent(
        event_type=event_type.value,
        agent_id=agent_id,
        timestamp=datetime.now().isoformat(),
        data=data,
        importance=importance,
        tags=tags or []
    )


# ============================================================
# 测试
# ============================================================

def run_tests():
    """运行测试"""
    print("=" * 60)
    print("🧪 EvolutionEventBus 测试 (记忆集成版)")
    print("=" * 60)
    
    # 测试事件总线
    print("\n[1] 事件发布测试")
    bus = EvolutionEventBus()
    event = create_event(EvolutionEventType.CAPABILITY_LEARNED, 'lily', {'test': 'memory_integration'})
    event_id = bus.publish(event)
    print(f"   ✓ 发布事件成功，ID: {event_id}")
    
    # 测试历史查询
    print("\n[2] 历史查询测试")
    history = bus.get_event_history(agent_id='lily', limit=5)
    print(f"   ✓ 查询到 {len(history)} 条记录")
    if history:
        print(f"   ✓ 最新事件：{history[0].event_type}")
    
    # 测试统计
    print("\n[3] 统计信息测试")
    stats = bus.get_stats()
    print(f"   ✓ 总事件数：{stats['total_events']}")
    print(f"   ✓ 事件类型分布：{stats['by_type']}")
    
    # 测试事件查询
    print("\n[4] 事件查询测试")
    if event_id.isdigit():
        event = bus.get_event_by_id(int(event_id))
        if event:
            print(f"   ✓ 查询到事件：{event.event_type}")
    
    print("\n" + "=" * 60)
    print("✅ EvolutionEventBus 测试完成")
    print("=" * 60)


if __name__ == '__main__':
    run_tests()
