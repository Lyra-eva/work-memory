#!/usr/bin/env python3
"""
Cron 超时执行器
为定时任务提供超时保护和重试机制
"""

import time
import threading
from datetime import datetime
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum


class CronStatus(Enum):
    """Cron 任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class CronTask:
    """Cron 任务"""
    task_id: str
    name: str
    schedule: str  # cron 表达式
    timeout_seconds: int = 60
    max_retries: int = 3
    status: CronStatus = CronStatus.PENDING
    last_run: Optional[str] = None
    next_run: Optional[str] = None
    retry_count: int = 0
    error: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "name": self.name,
            "schedule": self.schedule,
            "timeout_seconds": self.timeout_seconds,
            "max_retries": self.max_retries,
            "status": self.status.value,
            "last_run": self.last_run,
            "next_run": self.next_run,
            "retry_count": self.retry_count,
            "error": self.error
        }


class CronTimeoutExecutor:
    """Cron 超时执行器"""
    
    def __init__(self):
        self.tasks: Dict[str, CronTask] = {}
        self.running = False
    
    def add_task(self, name: str, schedule: str, timeout_seconds: int = 60, max_retries: int = 3) -> CronTask:
        """添加 Cron 任务"""
        task_id = f"cron_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.tasks)}"
        task = CronTask(
            task_id=task_id,
            name=name,
            schedule=schedule,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries
        )
        self.tasks[task_id] = task
        return task
    
    def execute_with_timeout(self, task_id: str, func: Callable, *args, **kwargs) -> Dict:
        """带超时保护执行任务"""
        if task_id not in self.tasks:
            return {"success": False, "error": "Task not found"}
        
        task = self.tasks[task_id]
        task.status = CronStatus.RUNNING
        task.last_run = datetime.now().isoformat()
        
        result = {"success": False, "data": None, "error": None}
        
        def target():
            try:
                data = func(*args, **kwargs)
                result["success"] = True
                result["data"] = data
            except Exception as e:
                result["error"] = str(e)
        
        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout=task.timeout_seconds)
        
        if thread.is_alive():
            task.status = CronStatus.TIMEOUT
            task.error = f"Timeout after {task.timeout_seconds}s"
            result["error"] = task.error
        elif result["success"]:
            task.status = CronStatus.COMPLETED
            task.retry_count = 0
        else:
            task.status = CronStatus.FAILED
            task.error = result["error"]
            task.retry_count += 1
        
        return result
    
    def get_task(self, task_id: str) -> Optional[CronTask]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> list:
        """获取所有任务"""
        return list(self.tasks.values())
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "total": len(self.tasks),
            "running": sum(1 for t in self.tasks.values() if t.status == CronStatus.RUNNING),
            "completed": sum(1 for t in self.tasks.values() if t.status == CronStatus.COMPLETED),
            "failed": sum(1 for t in self.tasks.values() if t.status == CronStatus.FAILED),
            "timeout": sum(1 for t in self.tasks.values() if t.status == CronStatus.TIMEOUT),
        }
