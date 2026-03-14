"""进化引擎核心模块（记忆集成版 v3.2.0 - 自动触发）"""

from .memory_event_bus import (
    EvolutionEventBus,
    EvolutionEvent,
    EvolutionEventType,
    create_event,
)

from .evolution_pipeline import (
    EvolutionPipeline,
    EvolutionValidator,
    PatternMiner,
    EvolutionStage,
    EvolutionPriority,
)

from .auto_trigger import (
    EvolutionAutoTrigger,
    EvolutionScheduler,
    AutoTriggerConfig,
    create_auto_trigger,
    enable_auto_trigger,
    disable_auto_trigger,
)

from .memory_event_bus import (
    ValidationStatus,
    ValidationLevel,
)

__all__ = [
    # 事件总线
    'EvolutionEventBus',
    'EvolutionEvent',
    'EvolutionEventType',
    'create_event',
    
    # 流水线
    'EvolutionPipeline',
    'EvolutionValidator',
    'PatternMiner',
    'EvolutionStage',
    'EvolutionPriority',
    
    # 自动触发
    'EvolutionAutoTrigger',
    'EvolutionScheduler',
    'AutoTriggerConfig',
    'create_auto_trigger',
    'enable_auto_trigger',
    'disable_auto_trigger',
    
    # 验证
    'ValidationStatus',
    'ValidationLevel',
]

__version__ = "3.2.0"
