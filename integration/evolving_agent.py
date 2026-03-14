#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能体进化集成模块

将 OODA 认知循环集成到智能体，实现自主进化能力
集成记忆同步器，实现双记忆系统同步
"""

import sys
import os
import logging
from typing import Dict, Optional, Any

# 添加进化引擎路径
EVOLUTION_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    'evolution-engine',
    'examples'
)
sys.path.insert(0, os.path.abspath(EVOLUTION_PATH))

from ooda_demo import OODATrigger, EventBuilder

# 添加记忆同步器
sys.path.insert(0, os.path.dirname(__file__))
from memory_sync import MemorySync

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================
# 进化智能体装饰器
# ============================================================

class EvolutionAgentMixin:
    """
    进化智能体混入类
    
    使用方式:
        class MyAgent(EvolutionAgentMixin):
            def __init__(self):
                super().__init__(agent_id='my_agent')
            
            def learn(self, skill):
                # 学习逻辑
                super().on_capability_learned(skill, success=True)
    """
    
    def __init__(self, agent_id: str = 'default', enable_evolution: bool = True, enable_memory_sync: bool = True):
        """
        初始化进化智能体
        
        Args:
            agent_id: 智能体 ID
            enable_evolution: 是否启用进化 (默认 True)
            enable_memory_sync: 是否启用记忆同步 (默认 True)
        """
        self.agent_id = agent_id
        self.enable_evolution = enable_evolution
        self.enable_memory_sync = enable_memory_sync
        
        if enable_evolution:
            logger.info(f"🧬 初始化进化引擎 (agent: {agent_id})...")
            self.evolution_trigger = OODATrigger(agent_id=agent_id)
            logger.info("✅ 进化引擎已就绪")
        else:
            self.evolution_trigger = None
            logger.info("⚠️ 进化引擎已禁用")
        
        if enable_memory_sync:
            logger.info(f"🧠 初始化记忆同步器 (agent: {agent_id})...")
            self.memory_sync = MemorySync()
            # 同步偏好到图谱
            self.memory_sync.sync_preferences_to_graph()
            logger.info("✅ 记忆同步器已就绪")
        else:
            self.memory_sync = None
            logger.info("⚠️ 记忆同步器已禁用")
    
    def on_capability_learned(self, capability: str, success: bool = True, 
                             message: str = "") -> Optional[Dict]:
        """
        能力学习后触发进化
        
        Args:
            capability: 能力名称
            success: 是否成功
            message: 消息
            
        Returns:
            dict: OODA 结果，如果禁用则返回 None
        """
        if not self.enable_evolution:
            logger.debug("⚠️ 进化引擎禁用，跳过")
            return None
        
        logger.info(f"📚 能力学习：{capability} ({'成功' if success else '失败'})")
        
        # 构建事件
        event = EventBuilder.capability_learned(
            agent_id=self.agent_id,
            capability=capability,
            success=success,
            message=message or f"{'成功' if success else '失败'}学会 {capability}"
        )
        
        # 触发 OODA 循环
        try:
            result = self.evolution_trigger.trigger(event)
            logger.info(f"✅ 进化完成：{result['decision_type']}")
            
            # 同步到 MEMORY.md (高重要性事件)
            if self.enable_memory_sync and self.memory_sync:
                if success and result.get('decision_type') in ['evolve', 'optimize']:
                    self.memory_sync.sync_milestone(
                        milestone_type='capability_learned',
                        description=f'学会 {capability} 技能',
                        importance=0.95
                    )
            
            return result
        except Exception as e:
            logger.error(f"❌ 进化失败：{e}")
            return None
    
    def on_capability_error(self, capability: str, error_type: str, 
                           error_msg: str) -> Optional[Dict]:
        """
        能力错误时触发进化
        
        Args:
            capability: 能力名称
            error_type: 错误类型
            error_msg: 错误消息
            
        Returns:
            dict: OODA 结果
        """
        if not self.enable_evolution:
            return None
        
        logger.warning(f"❌ 能力错误：{capability} - {error_type}")
        
        # 构建错误事件
        event = {
            'event_type': 'capability_error',
            'agent_id': self.agent_id,
            'data': {
                'capability': capability,
                'error_type': error_type,
                'error_message': error_msg,
                'success': False
            },
            'importance': 0.9
        }
        
        try:
            result = self.evolution_trigger.trigger(event)
            logger.info(f"✅ 错误处理完成：{result['decision_type']}")
            return result
        except Exception as e:
            logger.error(f"❌ 错误处理失败：{e}")
            return None
    
    def on_user_feedback(self, rating: int, comment: str = "") -> Optional[Dict]:
        """
        用户反馈时触发进化
        
        Args:
            rating: 评分 (1-5)
            comment: 评论
            
        Returns:
            dict: OODA 结果
        """
        if not self.enable_evolution:
            return None
        
        logger.info(f"💬 用户反馈：{'⭐' * rating} ({rating}/5)")
        
        event = EventBuilder.user_feedback(
            agent_id=self.agent_id,
            rating=rating,
            comment=comment
        )
        
        try:
            result = self.evolution_trigger.trigger(event)
            logger.info(f"✅ 反馈处理完成：{result['decision_type']}")
            return result
        except Exception as e:
            logger.error(f"❌ 反馈处理失败：{e}")
            return None
    
    def cleanup_evolution(self):
        """清理进化引擎资源"""
        if hasattr(self, 'evolution_trigger') and self.evolution_trigger:
            logger.info("🧹 清理进化引擎资源...")
            # OODATrigger 没有 close 方法，这里预留
        
        # 清理记忆同步器
        if hasattr(self, 'memory_sync') and self.memory_sync:
            logger.info("🧹 清理记忆同步器...")
            self.memory_sync.close()
        
        logger.info("✅ 清理完成")


# ============================================================
# 示例智能体
# ============================================================

class EvolvingAgent(EvolutionAgentMixin):
    """
    示例：具有进化能力的智能体
    
    使用方式:
        agent = EvolvingAgent('lily')
        agent.learn('web_search')
        agent.handle_feedback(5, '非常好用！')
        agent.cleanup()
    """
    
    def __init__(self, agent_id: str = 'my_agent'):
        super().__init__(agent_id=agent_id, enable_evolution=True)
        self.capabilities = set()
        logger.info(f"🤖 智能体 {agent_id} 已创建")
    
    def learn(self, skill_name: str) -> bool:
        """
        学习技能
        
        Args:
            skill_name: 技能名称
            
        Returns:
            bool: 是否成功
        """
        logger.info(f"📚 学习技能：{skill_name}")
        
        # 模拟学习逻辑
        success = True  # 这里可以是实际的学习逻辑
        
        if success:
            self.capabilities.add(skill_name)
            logger.info(f"✅ 学会：{skill_name}")
        
        # 触发进化
        self.on_capability_learned(skill_name, success)
        
        return success
    
    def handle_feedback(self, rating: int, comment: str = "") -> Dict:
        """
        处理用户反馈
        
        Args:
            rating: 评分 (1-5)
            comment: 评论
            
        Returns:
            dict: OODA 结果
        """
        return self.on_user_feedback(rating, comment)
    
    def handle_error(self, error_msg: str, capability: str = 'unknown') -> Dict:
        """
        处理错误
        
        Args:
            error_msg: 错误消息
            capability: 相关能力
            
        Returns:
            dict: OODA 结果
        """
        return self.on_capability_error(capability, 'runtime', error_msg)
    
    def get_capabilities(self) -> set:
        """获取已掌握的能力"""
        return self.capabilities.copy()
    
    def cleanup(self):
        """清理资源"""
        self.cleanup_evolution()
        logger.info(f"✅ 智能体 {self.agent_id} 已清理")


# ============================================================
# 使用示例
# ============================================================

def demo():
    """演示进化智能体的使用"""
    print("=" * 60)
    print("🧬 进化智能体演示")
    print("=" * 60)
    
    # 创建智能体
    agent = EvolvingAgent('lily')
    
    try:
        # 场景 1: 学习技能
        print("\n【场景 1】学习技能")
        print("-" * 60)
        agent.learn('web_search')
        agent.learn('image_recognition')
        
        # 场景 2: 用户反馈
        print("\n【场景 2】用户反馈")
        print("-" * 60)
        agent.handle_feedback(5, '太棒了！非常好用！')
        
        # 场景 3: 处理错误
        print("\n【场景 3】处理错误")
        print("-" * 60)
        agent.handle_error('搜索超时', 'web_search')
        
        # 总结
        print("\n【能力列表】")
        print("-" * 60)
        for cap in agent.get_capabilities():
            print(f"  ✓ {cap}")
        
    finally:
        agent.cleanup()
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")
    print("=" * 60)


if __name__ == '__main__':
    demo()
