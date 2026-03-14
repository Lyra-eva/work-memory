#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进化自动触发器 - Auto Trigger

功能:
- 能力学习后自动执行流水线
- 定时模式挖掘
- 事件自动订阅和触发

版本：3.2.0 (自动触发版)
创建：2026-03-12
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

try:
    from .memory_event_bus import EvolutionEventBus, EvolutionEvent, EvolutionEventType, create_event
    from .evolution_pipeline import EvolutionPipeline, PatternMiner
except ImportError:
    from memory_event_bus import EvolutionEventBus, EvolutionEvent, EvolutionEventType, create_event
    from evolution_pipeline import EvolutionPipeline, PatternMiner


# ============================================================
# 配置
# ============================================================

WORKSPACE_DIR = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE_DIR, 'memory')
EVOLUTION_DIR = os.path.join(MEMORY_DIR, 'evolution')
AUTO_TRIGGER_CONFIG = os.path.join(EVOLUTION_DIR, 'auto_trigger_config.json')
AUTO_TRIGGER_LOG = os.path.join(EVOLUTION_DIR, 'auto_trigger.log')


# ============================================================
# 自动触发器配置
# ============================================================

@dataclass
class AutoTriggerConfig:
    """自动触发器配置"""
    enabled: bool = True
    auto_execute_pipeline: bool = True  # 能力学习后自动执行流水线
    auto_mine_patterns: bool = True     # 定时挖掘模式
    pattern_mining_interval_hours: int = 1  # 模式挖掘间隔（小时）
    log_enabled: bool = True            # 启用日志
    
    def to_dict(self) -> Dict:
        return {
            'enabled': self.enabled,
            'auto_execute_pipeline': self.auto_execute_pipeline,
            'auto_mine_patterns': self.auto_mine_patterns,
            'pattern_mining_interval_hours': self.pattern_mining_interval_hours,
            'log_enabled': self.log_enabled
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AutoTriggerConfig':
        return cls(**data)


# ============================================================
# 自动触发器
# ============================================================

class EvolutionAutoTrigger:
    """
    进化自动触发器
    
    功能:
    - 自动订阅进化事件
    - 能力学习后自动执行流水线
    - 定时模式挖掘
    - 自动日志记录
    """
    
    def __init__(self, bus: EvolutionEventBus = None, agent_id: str = "default"):
        """
        初始化自动触发器
        
        Args:
            bus: 事件总线实例
            agent_id: 智能体 ID
        """
        self.bus = bus or EvolutionEventBus()
        self.agent_id = agent_id
        self.pipeline = EvolutionPipeline(agent_id=agent_id)
        self.miner = PatternMiner(agent_id=agent_id)
        
        self.config = self._load_config()
        self._init_stats()
        
        # 自动订阅事件
        if self.config.enabled:
            self._subscribe_events()
    
    def _load_config(self) -> AutoTriggerConfig:
        """加载配置"""
        if os.path.exists(AUTO_TRIGGER_CONFIG):
            with open(AUTO_TRIGGER_CONFIG, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return AutoTriggerConfig.from_dict(data)
        return AutoTriggerConfig()
    
    def _save_config(self):
        """保存配置"""
        os.makedirs(EVOLUTION_DIR, exist_ok=True)
        with open(AUTO_TRIGGER_CONFIG, 'w', encoding='utf-8') as f:
            json.dump(self.config.to_dict(), f, indent=2, ensure_ascii=False)
    
    def _init_stats(self):
        """初始化统计"""
        self.stats = {
            'total_triggers': 0,
            'pipeline_executions': 0,
            'pattern_mining_runs': 0,
            'last_trigger_time': None,
            'last_pipeline_execution': None,
            'last_pattern_mining': None
        }
        self._load_stats()
    
    def _load_stats(self):
        """加载统计"""
        stats_file = os.path.join(EVOLUTION_DIR, 'auto_trigger_stats.json')
        if os.path.exists(stats_file):
            with open(stats_file, 'r', encoding='utf-8') as f:
                self.stats = json.load(f)
    
    def _save_stats(self):
        """保存统计"""
        stats_file = os.path.join(EVOLUTION_DIR, 'auto_trigger_stats.json')
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)
    
    def _subscribe_events(self):
        """订阅事件"""
        # 订阅能力学习事件
        self.bus.subscribe('capability_learned', self.on_capability_learned)
        self.bus.subscribe('capability_updated', self.on_capability_updated)
        self.bus.subscribe('skill_improved', self.on_skill_improved)
        
        self._log("自动触发器已启动，订阅了 3 个事件类型")
    
    def _log(self, message: str):
        """记录日志"""
        if self.config.log_enabled:
            timestamp = datetime.now().isoformat()
            log_entry = f"[{timestamp}] {message}\n"
            
            with open(AUTO_TRIGGER_LOG, 'a', encoding='utf-8') as f:
                f.write(log_entry)
    
    def on_capability_learned(self, event: EvolutionEvent):
        """
        能力学习事件处理
        
        自动执行进化流水线
        """
        if not self.config.enabled:
            return
        
        if not self.config.auto_execute_pipeline:
            self._log(f"跳过流水线执行 (已禁用): {event.event_type}")
            return
        
        self._log(f"检测到能力学习事件，开始执行流水线: {event.data.get('capability', 'unknown')}")
        
        try:
            # 自动执行流水线
            result = self.pipeline.execute_pipeline(event)
            
            self.stats['pipeline_executions'] += 1
            self.stats['last_pipeline_execution'] = datetime.now().isoformat()
            self._save_stats()
            
            self._log(f"流水线执行完成：{result.status}, 阶段：{result.stage.value}")
            
            # 如果是高重要性事件，立即挖掘模式
            if event.importance >= 0.8 and self.config.auto_mine_patterns:
                self._log("高重要性事件，触发模式挖掘")
                self._mine_patterns_now()
            
        except Exception as e:
            self._log(f"流水线执行失败：{e}")
    
    def on_capability_updated(self, event: EvolutionEvent):
        """能力更新事件处理"""
        self.on_capability_learned(event)
    
    def on_skill_improved(self, event: EvolutionEvent):
        """技能提升事件处理"""
        self.on_capability_learned(event)
    
    def _mine_patterns_now(self) -> Dict:
        """立即执行模式挖掘"""
        self._log("开始模式挖掘")
        
        try:
            patterns = self.miner.mine()
            
            self.stats['pattern_mining_runs'] += 1
            self.stats['last_pattern_mining'] = datetime.now().isoformat()
            self._save_stats()
            
            self._log(f"模式挖掘完成：{len(patterns['patterns'])} 个模式，{len(patterns['recommendations'])} 条建议")
            
            return patterns
            
        except Exception as e:
            self._log(f"模式挖掘失败：{e}")
            return {'patterns': [], 'recommendations': []}
    
    def trigger_pipeline(self, event: EvolutionEvent) -> Dict:
        """
        手动触发流水线
        
        Args:
            event: 进化事件
            
        Returns:
            执行结果
        """
        self.stats['total_triggers'] += 1
        self.stats['last_trigger_time'] = datetime.now().isoformat()
        self._save_stats()
        
        self._log(f"手动触发流水线：{event.event_type}")
        
        result = self.pipeline.execute_pipeline(event)
        
        return {
            'success': result.status == 'completed',
            'status': result.status,
            'stage': result.stage.value,
            'task_id': result.task_id
        }
    
    def mine_patterns_now(self) -> Dict:
        """
        手动触发模式挖掘
        
        Returns:
            挖掘结果
        """
        return self._mine_patterns_now()
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats.copy()
    
    def enable(self):
        """启用自动触发"""
        self.config.enabled = True
        self._subscribe_events()
        self._save_config()
        self._log("自动触发器已启用")
    
    def disable(self):
        """禁用自动触发"""
        self.config.enabled = False
        self._save_config()
        self._log("自动触发器已禁用")
    
    def configure(self, **kwargs):
        """
        配置自动触发器
        
        Args:
            **kwargs: 配置项
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        self._save_config()
        self._log(f"配置已更新：{kwargs}")
    
    def get_log(self, lines: int = 50) -> List[str]:
        """
        获取日志
        
        Args:
            lines: 返回行数
            
        Returns:
            日志列表
        """
        if not os.path.exists(AUTO_TRIGGER_LOG):
            return []
        
        with open(AUTO_TRIGGER_LOG, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            return all_lines[-lines:]


# ============================================================
# 定时任务调度器
# ============================================================

class EvolutionScheduler:
    """
    进化定时任务调度器
    
    功能:
    - 定时模式挖掘
    - 定时统计报告
    - 定时清理
    """
    
    def __init__(self, auto_trigger: EvolutionAutoTrigger = None):
        """
        初始化调度器
        
        Args:
            auto_trigger: 自动触发器实例
        """
        self.auto_trigger = auto_trigger
        self.jobs = []
        self.running = False
    
    def schedule_pattern_mining(self, interval_hours: int = 1):
        """
        安排定时模式挖掘
        
        Args:
            interval_hours: 间隔小时数
        """
        self.jobs.append({
            'type': 'pattern_mining',
            'interval_hours': interval_hours,
            'next_run': datetime.now() + timedelta(hours=interval_hours)
        })
        auto_trigger._log(f"已安排定时模式挖掘，间隔：{interval_hours}小时")
    
    def schedule_stats_report(self, interval_hours: int = 24):
        """
        安排定时统计报告
        
        Args:
            interval_hours: 间隔小时数
        """
        self.jobs.append({
            'type': 'stats_report',
            'interval_hours': interval_hours,
            'next_run': datetime.now() + timedelta(hours=interval_hours)
        })
        auto_trigger._log(f"已安排定时统计报告，间隔：{interval_hours}小时")
    
    def run_once(self):
        """运行一次检查"""
        now = datetime.now()
        
        for job in self.jobs:
            if now >= job['next_run']:
                if job['type'] == 'pattern_mining':
                    self.auto_trigger.mine_patterns_now()
                elif job['type'] == 'stats_report':
                    self._generate_stats_report()
                
                job['next_run'] = now + timedelta(hours=job['interval_hours'])
    
    def _generate_stats_report(self):
        """生成统计报告"""
        stats = self.auto_trigger.get_stats()
        report = {
            'generated_at': datetime.now().isoformat(),
            'stats': stats
        }
        
        report_file = os.path.join(EVOLUTION_DIR, 'stats_report.json')
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.auto_trigger._log(f"已生成统计报告：{report_file}")


# ============================================================
# 便捷函数
# ============================================================

def create_auto_trigger(agent_id: str = "default", **kwargs) -> EvolutionAutoTrigger:
    """
    创建自动触发器
    
    Args:
        agent_id: 智能体 ID
        **kwargs: 配置项
        
    Returns:
        自动触发器实例
    """
    auto_trigger = EvolutionAutoTrigger(agent_id=agent_id)
    
    if kwargs:
        auto_trigger.configure(**kwargs)
    
    return auto_trigger


def enable_auto_trigger(agent_id: str = "default"):
    """启用自动触发"""
    auto_trigger = create_auto_trigger(agent_id=agent_id)
    auto_trigger.enable()
    return auto_trigger


def disable_auto_trigger(agent_id: str = "default"):
    """禁用自动触发"""
    auto_trigger = create_auto_trigger(agent_id=agent_id)
    auto_trigger.disable()
    return auto_trigger


# ============================================================
# 测试
# ============================================================

def run_tests():
    """运行测试"""
    print("=" * 60)
    print("🧪 EvolutionAutoTrigger 测试")
    print("=" * 60)
    
    # 1. 创建自动触发器
    print("\n[1] 创建自动触发器")
    auto_trigger = create_auto_trigger(agent_id='test', auto_execute_pipeline=True)
    print(f"   ✅ 自动触发器已创建")
    print(f"      配置：{auto_trigger.config.to_dict()}")
    
    # 2. 测试事件触发
    print("\n[2] 测试事件触发")
    event = create_event(
        EvolutionEventType.CAPABILITY_LEARNED,
        'test',
        {'capability': 'auto_test', 'success': True},
        importance=0.85
    )
    
    # 手动触发回调
    auto_trigger.on_capability_learned(event)
    print(f"   ✅ 事件触发完成")
    
    # 3. 检查统计
    print("\n[3] 检查统计")
    stats = auto_trigger.get_stats()
    print(f"   总触发次数：{stats['total_triggers']}")
    print(f"   流水线执行：{stats['pipeline_executions']}")
    print(f"   模式挖掘：{stats['pattern_mining_runs']}")
    
    # 4. 测试手动触发
    print("\n[4] 测试手动触发")
    result = auto_trigger.trigger_pipeline(event)
    print(f"   ✅ 手动触发完成")
    print(f"      状态：{result['status']}")
    
    # 5. 测试模式挖掘
    print("\n[5] 测试模式挖掘")
    patterns = auto_trigger.mine_patterns_now()
    print(f"   ✅ 模式挖掘完成")
    print(f"      模式数：{len(patterns.get('patterns', []))}")
    
    # 6. 检查日志
    print("\n[6] 检查日志")
    log = auto_trigger.get_log(lines=5)
    print(f"   最近日志:")
    for line in log[-3:]:
        print(f"      {line.strip()}")
    
    print("\n" + "=" * 60)
    print("✅ EvolutionAutoTrigger 测试完成")
    print("=" * 60)


if __name__ == '__main__':
    run_tests()
