#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记忆巩固模块 - Memory Consolidation

基于艾宾浩斯遗忘曲线的间隔重复算法
支持记忆强度管理、复习调度、保留率预测

版本：v3.4.0
创建：2026-03-15
"""

import json
import os
import sqlite3
import math
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from contextlib import contextmanager
import uuid

try:
    from .exceptions import (
        MemoryNotFoundError,
        InvalidRecallQualityError,
        MemoryConsolidationError
    )
except ImportError:
    from exceptions import (
        MemoryNotFoundError,
        InvalidRecallQualityError,
        MemoryConsolidationError
    )


# ============================================================
# 配置
# ============================================================

WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")
EVOLUTION_DIR = os.path.join(WORKSPACE_DIR, 'evolution')
DATA_DIR = os.path.join(EVOLUTION_DIR, 'data')
MC_DB_PATH = os.path.join(DATA_DIR, 'memory_consolidation.db')


# ============================================================
# 数据类
# ============================================================

@dataclass
class MemoryItem:
    """记忆项目"""
    id: str
    content: Dict
    strength: float = 0.0  # 记忆强度 0-1
    decay_rate: float = 0.1  # 衰减速率/小时
    last_reviewed: Optional[str] = None
    review_count: int = 0
    next_review: Optional[str] = None
    importance: float = 0.5  # 重要性 0-1
    emotional_intensity: float = 0.5  # 情感强度 0-1
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemoryItem':
        """从字典创建"""
        return cls(**data)


@dataclass
class ReviewSchedule:
    """复习计划"""
    memory_id: str
    scheduled_time: str
    priority: float
    estimated_duration: int  # 分钟
    review_type: str  # initial, reinforcement, rescue
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ============================================================
# 记忆巩固器
# ============================================================

class MemoryConsolidator:
    """
    记忆巩固器
    
    基于艾宾浩斯遗忘曲线的间隔重复系统
    
    功能:
    - 记忆项目管理
    - 遗忘曲线计算
    - 智能复习调度
    - 保留率预测
    - 记忆强度衰减模型
    """
    
    def __init__(self, db_path: str = MC_DB_PATH):
        """初始化记忆巩固器"""
        self.db_path = db_path
        self.memories: Dict[str, MemoryItem] = {}
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
                CREATE TABLE IF NOT EXISTS memory_items (
                    id TEXT PRIMARY KEY,
                    content JSON NOT NULL,
                    strength REAL DEFAULT 0.0,
                    decay_rate REAL DEFAULT 0.1,
                    last_reviewed TIMESTAMP,
                    review_count INTEGER DEFAULT 0,
                    next_review TIMESTAMP,
                    importance REAL DEFAULT 0.5,
                    emotional_intensity REAL DEFAULT 0.5,
                    metadata JSON DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS review_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_id TEXT NOT NULL,
                    review_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    quality REAL NOT NULL,
                    strength_before REAL,
                    strength_after REAL,
                    FOREIGN KEY (memory_id) REFERENCES memory_items(id)
                )
            """)
            
            # 索引
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mc_next_review ON memory_items(next_review)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mc_strength ON memory_items(strength)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mc_importance ON memory_items(importance)")
            
            # 复合索引（优化查询性能）
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mc_strength_due ON memory_items(strength, next_review)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mc_importance_strength ON memory_items(importance, strength)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_mc_review_history ON review_history(memory_id, review_time DESC)")
    
    def _load(self):
        """从数据库加载"""
        with self.transaction() as conn:
            cursor = conn.execute("SELECT * FROM memory_items")
            for row in cursor.fetchall():
                memory = MemoryItem(
                    id=row['id'],
                    content=json.loads(row['content']),
                    strength=row['strength'],
                    decay_rate=row['decay_rate'],
                    last_reviewed=row['last_reviewed'],
                    review_count=row['review_count'],
                    next_review=row['next_review'],
                    importance=row['importance'],
                    emotional_intensity=row['emotional_intensity'],
                    metadata=json.loads(row['metadata']) if row['metadata'] else {},
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
                self.memories[memory.id] = memory
    
    def _save_memory(self, memory: MemoryItem):
        """保存记忆"""
        with self.transaction() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO memory_items 
                (id, content, strength, decay_rate, last_reviewed, review_count, 
                 next_review, importance, emotional_intensity, metadata, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                memory.id,
                json.dumps(memory.content, ensure_ascii=False),
                memory.strength,
                memory.decay_rate,
                memory.last_reviewed,
                memory.review_count,
                memory.next_review,
                memory.importance,
                memory.emotional_intensity,
                json.dumps(memory.metadata, ensure_ascii=False),
                datetime.now().isoformat()
            ))
    
    # ========== 记忆项目管理 ==========
    
    def add_memory(self, memory: MemoryItem) -> str:
        """添加记忆项目"""
        # 计算首次复习时间
        memory.next_review = self.calculate_next_review(
            memory.strength,
            memory.importance,
            memory.review_count
        )
        
        self.memories[memory.id] = memory
        self._save_memory(memory)
        return memory.id
    
    def get_memory(self, memory_id: str) -> Optional[MemoryItem]:
        """获取记忆项目"""
        return self.memories.get(memory_id)
    
    def update_memory(self, memory_id: str, **kwargs) -> bool:
        """更新记忆项目"""
        memory = self.memories.get(memory_id)
        if not memory:
            return False
        
        for key, value in kwargs.items():
            if hasattr(memory, key):
                setattr(memory, key, value)
        
        memory.updated_at = datetime.now().isoformat()
        self._save_memory(memory)
        return True
    
    def delete_memory(self, memory_id: str) -> bool:
        """删除记忆项目"""
        if memory_id not in self.memories:
            return False
        
        del self.memories[memory_id]
        
        with self.transaction() as conn:
            conn.execute("DELETE FROM memory_items WHERE id = ?", (memory_id,))
        
        return True
    
    def list_memories(self, min_strength: float = None, 
                     due_only: bool = False) -> List[MemoryItem]:
        """列出记忆项目"""
        memories = list(self.memories.values())
        
        if min_strength is not None:
            memories = [m for m in memories if m.strength >= min_strength]
        
        if due_only:
            now = datetime.now()
            memories = [m for m in memories 
                       if m.next_review and 
                       datetime.fromisoformat(m.next_review) <= now]
        
        return memories
    
    # ========== 艾宾浩斯遗忘曲线 ==========
    
    def calculate_retention(self, memory: MemoryItem) -> float:
        """
        计算记忆保留率（艾宾浩斯遗忘曲线）
        
        公式：R = e^(-t/S)
        R: 保留率
        t: 经过时间
        S: 记忆强度相关的常数
        """
        if not memory.last_reviewed:
            return memory.strength
        
        # Python 3.6 兼容性处理
        try:
            last_review = datetime.fromisoformat(memory.last_reviewed)
        except AttributeError:
            # Python 3.6 不支持 fromisoformat
            last_review = datetime.strptime(memory.last_reviewed[:19], '%Y-%m-%dT%H:%M:%S')
        time_elapsed = (datetime.now() - last_review).total_seconds() / 3600  # 小时
        
        # S 是记忆强度相关的常数（半衰期）
        # 强度越高，半衰期越长
        S = 24 * (1 + memory.strength * 2)
        
        # 基础保留率
        retention = math.exp(-time_elapsed / S)
        
        # 重要性加成（重要记忆遗忘更慢）
        importance_factor = 0.5 + memory.importance * 0.5
        retention *= importance_factor
        
        # 情感强度加成（情感强烈的记忆更持久）
        emotion_factor = 0.7 + memory.emotional_intensity * 0.3
        retention *= emotion_factor
        
        return min(1.0, max(0.0, retention))
    
    def predict_forgetting_time(self, memory: MemoryItem, 
                               threshold: float = 0.3) -> float:
        """
        预测遗忘时间
        
        参数:
            memory: 记忆项目
            threshold: 遗忘阈值（低于此值认为已遗忘）
        
        返回:
            距离遗忘的小时数
        """
        current_retention = self.calculate_retention(memory)
        
        if current_retention <= threshold:
            return 0.0
        
        # 反向计算时间
        S = 24 * (1 + memory.strength * 2)
        importance_factor = 0.5 + memory.importance * 0.5
        emotion_factor = 0.7 + memory.emotional_intensity * 0.3
        
        # 解方程：threshold = current * e^(-t/S) * factor
        effective_factor = importance_factor * emotion_factor
        if effective_factor <= 0:
            return float('inf')
        
        target = threshold / effective_factor
        if target >= current_retention:
            return 0.0
        
        time_to_forget = -S * math.log(target / current_retention)
        return max(0.0, time_to_forget)
    
    # ========== 间隔重复算法 ==========
    
    def calculate_next_review(self, strength: float, importance: float, 
                             review_count: int) -> str:
        """
        计算下次复习时间
        
        间隔递增规则:
        - 第 1 次：1 天后
        - 第 2 次：2 天后
        - 第 3 次：4 天后
        - 第 4 次：8 天后
        - 第 5 次：16 天后
        - ...
        """
        # 基础间隔（小时）
        base_interval = 24  # 1 天
        
        # 强度因子：强度越高，间隔越长
        strength_factor = 1 + strength * 2
        
        # 重要性因子：越重要，间隔越短（需要更牢固）
        importance_factor = 1 + (1 - importance) * 0.5
        
        # 重复次数因子：指数增长
        if review_count == 0:
            repetition_factor = 1
        else:
            repetition_factor = math.pow(2, review_count)
        
        # 最终间隔
        interval_hours = base_interval * strength_factor * importance_factor * repetition_factor
        
        # 限制最大间隔为 30 天
        interval_hours = min(interval_hours, 24 * 30)
        
        next_review = datetime.now() + timedelta(hours=interval_hours)
        return next_review.isoformat()
    
    def review_memory(self, memory_id: str, recall_quality: float) -> MemoryItem:
        """
        复习记忆
        
        参数:
            memory_id: 记忆 ID
            recall_quality: 回忆质量 (0-1)
        
        返回:
            更新后的记忆项目
        
        异常:
            MemoryNotFoundError: 记忆不存在
            InvalidRecallQualityError: 回忆质量值无效
        """
        memory = self.memories.get(memory_id)
        if not memory:
            raise MemoryNotFoundError(memory_id)
        
        # 验证回忆质量
        if not 0.0 <= recall_quality <= 1.0:
            raise InvalidRecallQualityError(recall_quality)
        
        # 记录复习前强度
        strength_before = memory.strength
        
        # 根据回忆质量更新
        if recall_quality >= 0.8:  # 回忆良好
            memory.strength = min(1.0, memory.strength + 0.15)
            memory.decay_rate *= 0.85  # 减缓衰减
        elif recall_quality >= 0.6:  # 回忆一般
            memory.strength = min(1.0, memory.strength + 0.08)
        elif recall_quality >= 0.4:  # 回忆困难
            memory.strength *= 0.95  # 轻微下降
            memory.decay_rate *= 1.1  # 加快衰减
        else:  # 回忆失败
            memory.strength *= 0.8  # 明显下降
            memory.decay_rate *= 1.3  # 需要更频繁复习
        
        # 更新复习记录
        memory.review_count += 1
        memory.last_reviewed = datetime.now().isoformat()
        memory.next_review = self.calculate_next_review(
            memory.strength,
            memory.importance,
            memory.review_count
        )
        
        # 记录复习历史
        self._log_review(memory.id, recall_quality, 
                        strength_before, memory.strength)
        
        # 保存
        self._save_memory(memory)
        
        return memory
    
    def _log_review(self, memory_id: str, quality: float, 
                   strength_before: float, strength_after: float):
        """记录复习历史"""
        with self.transaction() as conn:
            conn.execute("""
                INSERT INTO review_history 
                (memory_id, quality, strength_before, strength_after)
                VALUES (?, ?, ?, ?)
            """, (memory_id, quality, strength_before, strength_after))
    
    # ========== 复习调度 ==========
    
    def get_due_memories(self, limit: int = 20) -> List[MemoryItem]:
        """获取需要复习的记忆"""
        now = datetime.now()
        due = []
        
        for memory in self.memories.values():
            if memory.next_review:
                try:
                    next_review = datetime.fromisoformat(memory.next_review)
                except AttributeError:
                    next_review = datetime.strptime(memory.next_review[:19], '%Y-%m-%dT%H:%M:%S')
                if next_review <= now:
                    due.append(memory)
        
        # 按优先级排序（重要性高 + 遗忘风险高的优先）
        due.sort(key=lambda m: (
            m.importance * 0.5 + 
            (1 - self.calculate_retention(m)) * 0.5
        ), reverse=True)
        
        return due[:limit]
    
    def generate_review_schedule(self, 
                                memories: List[MemoryItem] = None,
                                daily_capacity: int = 10) -> List[ReviewSchedule]:
        """
        生成复习计划
        
        参数:
            memories: 记忆列表（为空则使用所有记忆）
            daily_capacity: 每日复习容量
        
        返回:
            复习计划列表
        """
        if memories is None:
            memories = list(self.memories.values())
        
        schedule = []
        
        for memory in memories:
            # 计算遗忘风险
            retention = self.calculate_retention(memory)
            time_to_forget = self.predict_forgetting_time(memory)
            
            # 计算优先级
            urgency = 1.0 / (time_to_forget + 1)  # 越容易遗忘越紧急
            importance = memory.importance
            priority = urgency * (0.5 + importance * 0.5)
            
            # 确定复习类型
            if retention < 0.4:
                review_type = "rescue"  # 救援复习
                duration = 15
            elif retention < 0.7:
                review_type = "reinforcement"  # 强化复习
                duration = 10
            else:
                review_type = "initial"  # 常规复习
                duration = 5
            
            # 计算最佳复习时间
            try:
                optimal_time = self._calculate_optimal_review_time(memory)
            except:
                optimal_time = datetime.now().isoformat()
            
            schedule_item = ReviewSchedule(
                memory_id=memory.id,
                scheduled_time=optimal_time,
                priority=priority,
                estimated_duration=duration,
                review_type=review_type,
                metadata={
                    'retention': retention,
                    'time_to_forget_hours': time_to_forget,
                    'review_count': memory.review_count
                }
            )
            schedule.append(schedule_item)
        
        # 按优先级排序
        schedule.sort(key=lambda s: s.priority, reverse=True)
        
        # 限制每日容量
        return schedule[:daily_capacity]
    
    def _calculate_optimal_review_time(self, memory: MemoryItem) -> str:
        """计算最佳复习时间"""
        # 在记忆强度降到 0.6 时复习最佳
        target_retention = 0.6
        current_retention = self.calculate_retention(memory)
        
        if current_retention <= target_retention:
            # 已经需要复习
            return datetime.now().isoformat()
        
        # 预测何时会降到目标值
        time_to_target = self.predict_forgetting_time(memory, target_retention)
        optimal_time = datetime.now() + timedelta(hours=time_to_target * 0.8)  # 提前 20%
        
        return optimal_time.isoformat()
    
    # ========== 统计信息 ==========
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        memories = list(self.memories.values())
        
        if not memories:
            return {
                'total_memories': 0,
                'avg_strength': 0.0,
                'avg_retention': 0.0,
                'due_count': 0,
                'by_importance': {}
            }
        
        # 需要复习的数量
        due_count = len(self.get_due_memories(limit=1000))
        
        # 按重要性分组
        by_importance = {
            'high': len([m for m in memories if m.importance >= 0.7]),
            'medium': len([m for m in memories if 0.4 <= m.importance < 0.7]),
            'low': len([m for m in memories if m.importance < 0.4])
        }
        
        return {
            'total_memories': len(memories),
            'avg_strength': sum(m.strength for m in memories) / len(memories),
            'avg_retention': sum(self.calculate_retention(m) for m in memories) / len(memories),
            'due_count': due_count,
            'by_importance': by_importance,
            'total_reviews': sum(m.review_count for m in memories)
        }
    
    def export_to_json(self, output_path: str) -> Tuple[int, int]:
        """导出为 JSON"""
        data = {
            'schema': 'memory_consolidation.v1',
            'exported_at': datetime.now().isoformat(),
            'memories': [m.to_dict() for m in self.memories.values()]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return len(self.memories), 0


# ============================================================
# 便捷函数
# ============================================================

def create_memory(content: Dict, importance: float = 0.5, 
                 emotional_intensity: float = 0.5) -> MemoryItem:
    """创建记忆项目"""
    return MemoryItem(
        id=f"mem_{uuid.uuid4().hex[:12]}",
        content=content,
        importance=importance,
        emotional_intensity=emotional_intensity
    )


# ============================================================
# 测试
# ============================================================

def run_tests():
    """运行测试"""
    print("=" * 60)
    print("🧪 MemoryConsolidator 测试")
    print("=" * 60)
    
    # 初始化
    import os
    test_db = os.path.expanduser("~/.openclaw/workspace/evolution/data/mc_test.db")
    mc = MemoryConsolidator(test_db)
    
    print("\n✅ 记忆巩固器初始化成功")
    
    # 创建记忆
    print("\n【测试 1】创建记忆项目")
    mem1 = create_memory({
        'type': 'concept',
        'name': '艾宾浩斯遗忘曲线',
        'definition': '描述记忆遗忘速度的曲线'
    }, importance=0.9)
    
    mem2 = create_memory({
        'type': 'skill',
        'name': 'Python 编程',
        'level': 'intermediate'
    }, importance=0.7)
    
    mc.add_memory(mem1)
    mc.add_memory(mem2)
    print(f"  ✅ 创建 2 个记忆")
    
    # 计算保留率
    print("\n【测试 2】遗忘曲线计算")
    retention1 = mc.calculate_retention(mem1)
    retention2 = mc.calculate_retention(mem2)
    print(f"  记忆 1 保留率：{retention1:.1%}")
    print(f"  记忆 2 保留率：{retention2:.1%}")
    
    # 预测遗忘时间
    print("\n【测试 3】遗忘时间预测")
    time1 = mc.predict_forgetting_time(mem1)
    print(f"  记忆 1 距离遗忘：{time1:.1f}小时")
    
    # 复习记忆
    print("\n【测试 4】复习记忆")
    updated = mc.review_memory(mem1.id, recall_quality=0.85)
    print(f"  ✅ 复习完成")
    print(f"      强度：{mem1.strength:.2f} → {updated.strength:.2f}")
    print(f"      复习次数：{mem1.review_count}")
    
    # 生成复习计划
    print("\n【测试 5】生成复习计划")
    schedule = mc.generate_review_schedule(daily_capacity=5)
    print(f"  ✅ 生成 {len(schedule)} 项复习计划")
    for item in schedule[:3]:
        print(f"      • {item.memory_id[:8]}... (优先级：{item.priority:.2f}, {item.review_type})")
    
    # 统计信息
    print("\n【测试 6】统计信息")
    stats = mc.get_stats()
    print(f"  总记忆数：{stats['total_memories']}")
    print(f"  平均强度：{stats['avg_strength']:.2f}")
    print(f"  平均保留：{stats['avg_retention']:.2f}")
    print(f"  需要复习：{stats['due_count']}")
    
    # 清理
    if os.path.exists(test_db):
        os.remove(test_db)
    
    print("\n" + "=" * 60)
    print("✅ MemoryConsolidator 测试完成")
    print("=" * 60)


if __name__ == '__main__':
    run_tests()
