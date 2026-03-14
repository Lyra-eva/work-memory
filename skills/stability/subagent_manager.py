#!/usr/bin/env python3
"""
子任务管理器
管理子任务的创建、执行和超时控制
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class SubTask:
    """子任务"""
    task_id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    timeout_seconds: int = 300
    result: Optional[Dict] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "name": self.name,
            "status": self.status.value,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "timeout_seconds": self.timeout_seconds,
            "result": self.result,
            "error": self.error
        }


class SubagentManager:
    """子任务管理器"""
    
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.tasks: Dict[str, SubTask] = {}
        self.running_count = 0
    
    def create_task(self, name: str, timeout_seconds: int = 300) -> SubTask:
        """创建子任务"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.tasks)}"
        task = SubTask(
            task_id=task_id,
            name=name,
            timeout_seconds=timeout_seconds
        )
        self.tasks[task_id] = task
        return task
    
    def start_task(self, task_id: str) -> bool:
        """启动任务"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        if self.running_count >= self.max_concurrent:
            return False
        
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now().isoformat()
        self.running_count += 1
        return True
    
    def complete_task(self, task_id: str, result: Dict = None) -> bool:
        """完成任务"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now().isoformat()
        task.result = result
        self.running_count -= 1
        return True
    
    def fail_task(self, task_id: str, error: str) -> bool:
        """失败任务"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.status = TaskStatus.FAILED
        task.completed_at = datetime.now().isoformat()
        task.error = error
        self.running_count -= 1
        return True
    
    def check_timeout(self, task_id: str) -> bool:
        """检查任务是否超时"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        if task.status != TaskStatus.RUNNING or not task.started_at:
            return False
        
        started = datetime.fromisoformat(task.started_at)
        elapsed = (datetime.now() - started).total_seconds()
        
        if elapsed > task.timeout_seconds:
            task.status = TaskStatus.TIMEOUT
            task.error = f"Timeout after {elapsed:.0f}s (limit: {task.timeout_seconds}s)"
            self.running_count -= 1
            return True
        
        return False
    
    def get_task(self, task_id: str) -> Optional[SubTask]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[SubTask]:
        """获取所有任务"""
        return list(self.tasks.values())
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        stats = {
            "total": len(self.tasks),
            "running": self.running_count,
            "completed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED),
            "failed": sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED),
            "timeout": sum(1 for t in self.tasks.values() if t.status == TaskStatus.TIMEOUT),
            "pending": sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING),
        }
        return stats
