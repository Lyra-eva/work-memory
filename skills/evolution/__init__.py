# Evolution Engine - 进化引擎 v3.2.0 (自动触发版)

"""
进化引擎核心模块（自动触发版）

新增自动触发器，实现：
- 能力学习后自动执行流水线
- 定时模式挖掘
- 自动事件订阅

模块:
- engine: 进化引擎核心（事件总线、流水线、验证器、模式挖掘、自动触发）
"""

__version__ = "3.2.0"

from .engine import (
    EvolutionPipeline,
    EvolutionValidator,
    PatternMiner,
    EvolutionEventBus,
    EvolutionEvent,
    EvolutionEventType,
    create_event,
    # 自动触发
    EvolutionAutoTrigger,
    EvolutionScheduler,
    create_auto_trigger,
    enable_auto_trigger,
    disable_auto_trigger,
    # 验证
    ValidationStatus,
    ValidationLevel,
)

__all__ = [
    # 核心模块
    'EvolutionPipeline',
    'EvolutionValidator',
    'PatternMiner',
    
    # 事件总线
    'EvolutionEventBus',
    'EvolutionEvent',
    'EvolutionEventType',
    'create_event',
    
    # 自动触发
    'EvolutionAutoTrigger',
    'EvolutionScheduler',
    'create_auto_trigger',
    'enable_auto_trigger',
    'disable_auto_trigger',
    
    # 验证
    'ValidationStatus',
    'ValidationLevel',
]
