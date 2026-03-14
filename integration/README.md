# 🧬 智能体进化集成指南

**版本**: 1.0.0  
**日期**: 2026-03-13  
**状态**: ✅ 生产就绪

---

## 🎯 快速开始

### 3 步集成进化能力

```python
# 1. 导入
from integration.evolving_agent import EvolutionAgentMixin

# 2. 继承
class MyAgent(EvolutionAgentMixin):
    def __init__(self):
        super().__init__(agent_id='lily')
    
    def learn(self, skill):
        # 学习逻辑
        super().on_capability_learned(skill, success=True)

# 3. 使用
agent = MyAgent()
agent.learn('web_search')
```

---

## 📖 完整示例

### 方式 1: 使用混入类 (推荐)

```python
from integration.evolving_agent import EvolutionAgentMixin

class MyAgent(EvolutionAgentMixin):
    """具有进化能力的智能体"""
    
    def __init__(self, agent_id='my_agent'):
        # 初始化进化引擎
        super().__init__(agent_id=agent_id, enable_evolution=True)
        self.capabilities = []
    
    def learn(self, skill_name):
        """学习技能"""
        # 实际学习逻辑
        success = True
        
        # 触发进化
        self.on_capability_learned(skill_name, success)
    
    def on_feedback(self, rating, comment):
        """处理反馈"""
        self.on_user_feedback(rating, comment)
    
    def on_error(self, error_msg, capability):
        """处理错误"""
        self.on_capability_error(capability, 'runtime', error_msg)

# 使用
agent = MyAgent('lily')
agent.learn('web_search')
agent.on_feedback(5, '非常好用！')
```

---

### 方式 2: 使用示例智能体

```python
from integration.evolving_agent import EvolvingAgent

# 创建智能体
agent = EvolvingAgent('lily')

# 学习技能
agent.learn('web_search')
agent.learn('image_recognition')

# 处理反馈
agent.handle_feedback(5, '太棒了！')

# 处理错误
agent.handle_error('搜索超时', 'web_search')

# 查看能力
print(agent.get_capabilities())
# 输出：{'web_search', 'image_recognition'}

# 清理
agent.cleanup()
```

---

### 方式 3: 直接调用 OODA

```python
import sys
sys.path.insert(0, '/home/admin/.openclaw/workspace/evolution-engine/examples')
from ooda_demo import OODATrigger, EventBuilder

# 初始化
trigger = OODATrigger(agent_id='lily')

# 触发进化
event = EventBuilder.capability_learned(
    agent_id='lily',
    capability='web_search',
    success=True
)
result = trigger.trigger(event)

print(f"决策：{result['decision_type']}")
```

---

## 🎯 触发时机

### 1. 能力学习后

```python
def learn_skill(self, skill_name):
    # ... 学习逻辑 ...
    success = True
    
    # 触发进化
    self.on_capability_learned(skill_name, success)
```

**输出**:
```
📚 能力学习：web_search (成功)
📊 触发 OODA 循环：capability_learned
【1】Observe - 感知事件...
  ✓ 情绪极性：0.80
  ✓ 用户意图：learn
【2】Orient - 定向分析...
  ✓ 相似事件：8 个
【3】Decide - 生成决策...
  ✓ 决策类型：evolve
【4】Act - 执行决策...
  ✓ 执行成功：True
✅ 进化完成：evolve
```

---

### 2. 用户反馈时

```python
def on_feedback(self, rating, comment):
    self.on_user_feedback(rating, comment)
```

**输出**:
```
💬 用户反馈：⭐⭐⭐⭐⭐ (5/5)
📊 触发 OODA 循环：user_feedback
✅ 反馈处理完成：maintain
```

---

### 3. 发生错误时

```python
def on_error(self, error_msg, capability):
    self.on_capability_error(capability, 'runtime', error_msg)
```

**输出**:
```
❌ 能力错误：web_search - runtime
📊 触发 OODA 循环：capability_error
✅ 错误处理完成：optimize
```

---

## 📊 决策类型说明

| 决策类型 | 含义 | 触发场景 |
|---------|------|---------|
| `evolve` | 进化新能力 | 成功学习、正面反馈 |
| `optimize` | 优化现有能力 | 错误、负面反馈 |
| `maintain` | 保持现状 | 中性事件 |
| `deprecate` | 废弃能力 | 长期未使用 |
| `investigate` | 进一步调查 | 不确定情况 |

---

## 🔧 配置选项

### 启用/禁用进化

```python
# 启用 (默认)
agent = MyAgent(agent_id='lily', enable_evolution=True)

# 禁用
agent = MyAgent(agent_id='lily', enable_evolution=False)
```

### 日志级别

```python
import logging
logging.basicConfig(level=logging.INFO)  # DEBUG/INFO/WARNING/ERROR
```

---

## 🎯 最佳实践

### 1. 在关键事件点触发

```python
class MyAgent(EvolutionAgentMixin):
    def learn(self, skill):
        success = self._do_learn(skill)
        self.on_capability_learned(skill, success)  # ✅ 触发
    
    def execute(self, capability, *args):
        try:
            return self._do_execute(capability, *args)
        except Exception as e:
            self.on_capability_error(capability, type(e).__name__, str(e))  # ✅ 触发
            raise
```

---

### 2. 统一资源管理

```python
agent = MyAgent('lily')
try:
    agent.learn('web_search')
    agent.on_feedback(5, '好用！')
finally:
    agent.cleanup()  # ✅ 清理资源
```

---

### 3. 异常处理

```python
def on_capability_learned(self, capability, success):
    try:
        result = super().on_capability_learned(capability, success)
        logger.info(f"进化完成：{result['decision_type']}")
    except Exception as e:
        logger.error(f"进化失败：{e}")  # ✅ 记录日志
        # 不影响主流程
```

---

## 📋 运行演示

```bash
cd /home/admin/.openclaw/workspace
python3 integration/evolving_agent.py
```

**输出预览**:
```
============================================================
🧬 进化智能体演示
============================================================
🧠 初始化进化引擎 (agent: lily)...
✅ 进化引擎已就绪

【场景 1】学习技能
📚 学习技能：web_search
📊 触发 OODA 循环：capability_learned
  ✓ Observe: 情绪=0.80, 意图=learn
  ✓ Orient: 相似事件=8 个
  ✓ Decide: evolve, 置信度=0.80
  ✓ Act: 执行成功
✅ 进化完成：evolve

【场景 2】用户反馈
💬 用户反馈：⭐⭐⭐⭐⭐ (5/5)
✅ 反馈处理完成：maintain

【场景 3】处理错误
❌ 能力错误：web_search
✅ 错误处理完成：maintain

✅ 演示完成！
```

---

## 🐛 故障排查

### 问题 1: 模块导入失败

```bash
# 确保路径正确
cd /home/admin/.openclaw/workspace
python3 -c "from integration.evolving_agent import EvolutionAgentMixin; print('✅ 导入成功')"
```

### 问题 2: 图谱数据库不存在

```bash
# 运行迁移脚本
cd evolution-engine
python3 scripts/migrate_to_graph.py
```

### 问题 3: 情绪分析不准确

确保 message 字段包含明确情感词：
- ✅ "太棒了！成功学会了！"
- ❌ "学会了"

---

## 📚 API 参考

### EvolutionAgentMixin

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `__init__` | agent_id, enable_evolution | - | 初始化 |
| `on_capability_learned` | capability, success, message | dict | 能力学习触发 |
| `on_capability_error` | capability, error_type, error_msg | dict | 错误触发 |
| `on_user_feedback` | rating, comment | dict | 反馈触发 |
| `cleanup_evolution` | - | - | 清理资源 |

### EvolvingAgent

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `__init__` | agent_id | - | 初始化 |
| `learn` | skill_name | bool | 学习技能 |
| `handle_feedback` | rating, comment | dict | 处理反馈 |
| `handle_error` | error_msg, capability | dict | 处理错误 |
| `get_capabilities` | - | set | 获取能力列表 |
| `cleanup` | - | - | 清理资源 |

---

## 🎯 集成检查清单

- [ ] 导入 `EvolutionAgentMixin`
- [ ] 继承并调用 `super().__init__()`
- [ ] 在学习方法中调用 `on_capability_learned()`
- [ ] 在错误处理中调用 `on_capability_error()`
- [ ] 在反馈处理中调用 `on_user_feedback()`
- [ ] 在清理方法中调用 `cleanup_evolution()`
- [ ] 运行演示验证

---

## 📚 更多资源

- [OODA 演示](../evolution-engine/examples/ooda_demo.py)
- [使用指南](../evolution-engine/docs/USAGE_GUIDE.md)
- [架构评估](../evolution-engine/docs/ARCHITECTURE_REVIEW.md)

---

**最后更新**: 2026-03-13 12:55  
**维护者**: OpenClaw Evolution Team 🌱
