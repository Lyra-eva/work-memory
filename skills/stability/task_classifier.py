#!/usr/bin/env python3
"""
任务分类器
根据任务特征自动分类并分配资源
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    """任务类型"""
    SIMPLE = "simple"          # 简单任务
    COMPLEX = "complex"        # 复杂任务
    LONG_RUNNING = "long_running"  # 长运行任务
    IO_BOUND = "io_bound"      # IO 密集型
    CPU_BOUND = "cpu_bound"    # CPU 密集型


@dataclass
class TaskClassification:
    """任务分类结果"""
    task_type: TaskType
    priority: int  # 1-10, 10 最高
    estimated_time: int  # 预估时间（秒）
    resource_allocation: Dict
    
    def to_dict(self) -> Dict:
        return {
            "task_type": self.task_type.value,
            "priority": self.priority,
            "estimated_time": self.estimated_time,
            "resource_allocation": self.resource_allocation
        }


class TaskClassifier:
    """任务分类器"""
    
    def __init__(self):
        self.keywords = {
            TaskType.SIMPLE: ["search", "get", "list", "read"],
            TaskType.COMPLEX: ["analyze", "process", "generate", "create"],
            TaskType.LONG_RUNNING: ["download", "upload", "backup", "sync"],
            TaskType.IO_BOUND: ["file", "read", "write", "network"],
            TaskType.CPU_BOUND: ["calculate", "compute", "transform", "encrypt"],
        }
    
    def classify(self, task_name: str, task_description: str = "") -> TaskClassification:
        """分类任务"""
        text = f"{task_name} {task_description}".lower()
        
        # 匹配关键词
        scores = {}
        for task_type, keywords in self.keywords.items():
            score = sum(1 for kw in keywords if kw in text)
            scores[task_type] = score
        
        # 选择最高分的类型
        best_type = max(scores, key=scores.get) if any(scores.values()) else TaskType.SIMPLE
        
        # 分配资源
        resource_allocation = self._allocate_resources(best_type)
        
        # 预估时间
        estimated_time = self._estimate_time(best_type)
        
        # 优先级
        priority = self._calculate_priority(best_type, text)
        
        return TaskClassification(
            task_type=best_type,
            priority=priority,
            estimated_time=estimated_time,
            resource_allocation=resource_allocation
        )
    
    def _allocate_resources(self, task_type: TaskType) -> Dict:
        """分配资源"""
        allocations = {
            TaskType.SIMPLE: {"cpu": 1, "memory": "256MB", "timeout": 30},
            TaskType.COMPLEX: {"cpu": 2, "memory": "512MB", "timeout": 120},
            TaskType.LONG_RUNNING: {"cpu": 1, "memory": "256MB", "timeout": 600},
            TaskType.IO_BOUND: {"cpu": 1, "memory": "128MB", "timeout": 60},
            TaskType.CPU_BOUND: {"cpu": 4, "memory": "1GB", "timeout": 300},
        }
        return allocations.get(task_type, allocations[TaskType.SIMPLE])
    
    def _estimate_time(self, task_type: TaskType) -> int:
        """预估时间"""
        estimates = {
            TaskType.SIMPLE: 10,
            TaskType.COMPLEX: 60,
            TaskType.LONG_RUNNING: 300,
            TaskType.IO_BOUND: 30,
            TaskType.CPU_BOUND: 120,
        }
        return estimates.get(task_type, 30)
    
    def _calculate_priority(self, task_type: TaskType, text: str) -> int:
        """计算优先级"""
        base_priority = {
            TaskType.SIMPLE: 5,
            TaskType.COMPLEX: 7,
            TaskType.LONG_RUNNING: 3,
            TaskType.IO_BOUND: 6,
            TaskType.CPU_BOUND: 4,
        }
        
        priority = base_priority.get(task_type, 5)
        
        # 紧急关键词提升优先级
        urgent_keywords = ["urgent", "critical", "important", "now"]
        if any(kw in text for kw in urgent_keywords):
            priority += 3
        
        return min(priority, 10)
