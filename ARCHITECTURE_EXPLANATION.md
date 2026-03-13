# 📋 工作记忆系统架构说明

**问题**: 记忆系统是全局性的还是当前智能体的？

**答案**: **支持两种模式**，可配置！

---

## 🏗️ 架构设计

### 模式 1: 单智能体模式 (默认)

```python
from work_memory import WorkMemory

# 每个智能体有自己的记忆目录
wm = WorkMemory(root_dir="~/work_memory_agent_lily")
```

**特点**:
- ✅ 记忆隔离
- ✅ 隐私保护
- ✅ 独立备份
- ❌ 无法共享记忆

**适用场景**:
- 个人使用
- 多用户环境
- 需要隐私隔离

---

### 模式 2: 全局共享模式

```python
from work_memory import WorkMemory

# 所有智能体共享同一个记忆目录
wm = WorkMemory(root_dir="~/openclaw/workspace/work_memory")
```

**特点**:
- ✅ 记忆共享
- ✅ 跨智能体协作
- ✅ 统一知识管理
- ❌ 无隐私隔离

**适用场景**:
- 团队协作
- 多智能体协作
- 知识共享

---

### 模式 3: 混合模式 (推荐)

```python
# 全局记忆 + 个人记忆
class EvolvingAgent:
    def __init__(self, agent_id='lily'):
        # 全局记忆 (共享)
        self.global_memory = WorkMemory(
            root_dir="~/openclaw/workspace/work_memory"
        )
        
        # 个人记忆 (隔离)
        self.personal_memory = WorkMemory(
            root_dir=f"~/openclaw/workspace/work_memory_{agent_id}"
        )
```

**特点**:
- ✅ 全局知识共享
- ✅ 个人隐私保护
- ✅ 灵活配置
- ✅ 最佳实践

---

## 📊 当前配置

### 进化引擎集成

```python
# integration/evolving_agent.py
class EvolvingAgent(EvolutionAgentMixin):
    def __init__(self, agent_id='lily'):
        super().__init__(agent_id=agent_id)
        
        # 工作记忆 (可配置)
        self.work_memory = WorkMemory(
            root_dir="~/openclaw/workspace/work_memory"  # ← 可修改
        )
```

**当前配置**: 
- 根目录：`~/openclaw/workspace/work_memory`
- 作用域：**全局共享** (所有智能体共用)

---

## 🔧 配置方式

### 方式 1: 修改根目录

```python
# 全局记忆
wm = WorkMemory(root_dir="~/openclaw/workspace/work_memory")

# 个人记忆
wm = WorkMemory(root_dir="~/openclaw/workspace/work_memory_lily")

# 团队记忆
wm = WorkMemory(root_dir="~/openclaw/workspace/work_memory_team")
```

---

### 方式 2: 环境变量配置

```bash
# 设置记忆目录
export WORK_MEMORY_ROOT="~/openclaw/workspace/work_memory"

# Python 中使用
import os
wm = WorkMemory(root_dir=os.getenv('WORK_MEMORY_ROOT'))
```

---

### 方式 3: 配置文件

```python
# config.py
MEMORY_CONFIG = {
    'global': '~/openclaw/workspace/work_memory',
    'personal': '~/openclaw/workspace/work_memory_{agent_id}',
    'team': '~/openclaw/workspace/work_memory_team'
}

# 使用
wm = WorkMemory(root_dir=MEMORY_CONFIG['global'])
```

---

## 📋 推荐方案

### 个人使用

```python
# 个人独立记忆
wm = WorkMemory(root_dir="~/work_memory")
```

---

### 团队使用

```python
# 全局共享记忆
wm = WorkMemory(root_dir="~/team_work_memory")

# 个人私有记忆
wm_personal = WorkMemory(root_dir="~/work_memory_{agent_id}")
```

---

### 多智能体协作

```python
class MultiAgentSystem:
    def __init__(self):
        # 共享记忆池
        self.shared_memory = WorkMemory(
            root_dir="~/shared_work_memory"
        )
        
        # 智能体私有记忆
        self.agent_memories = {}
        for agent_id in ['lily', 'jack', 'rose']:
            self.agent_memories[agent_id] = WorkMemory(
                root_dir=f"~/work_memory_{agent_id}"
            )
```

---

## 🎯 最佳实践

### 1. 按场景选择

| 场景 | 推荐模式 | 目录 |
|------|---------|------|
| 个人使用 | 个人模式 | `~/work_memory` |
| 团队协作 | 全局模式 | `~/team_work_memory` |
| 多智能体 | 混合模式 | `~/shared_` + `~/personal_` |

---

### 2. 记忆分类

```
work_memory/
├── global/              # 全局共享
│   ├── projects/
│   └── knowledge/
├── personal/            # 个人隐私
│   ├── lily/
│   ├── jack/
│   └── rose/
└── team/                # 团队专用
    └── projects/
```

---

### 3. 访问控制

```python
class SecureWorkMemory(WorkMemory):
    def __init__(self, root_dir, agent_id=None):
        super().__init__(root_dir)
        self.agent_id = agent_id
    
    def save_personal(self, key, data):
        """保存个人数据"""
        if self.agent_id:
            path = os.path.join(self.root_dir, "personal", self.agent_id)
            # 保存到个人目录
```

---

## 📊 对比总结

| 维度 | 全局模式 | 个人模式 | 混合模式 |
|------|---------|---------|---------|
| **共享性** | ✅ 高 | ❌ 无 | ✅ 中 |
| **隐私性** | ❌ 低 | ✅ 高 | ✅ 中 |
| **协作性** | ✅ 高 | ❌ 低 | ✅ 中 |
| **灵活性** | ⚠️ 低 | ⚠️ 低 | ✅ 高 |
| **推荐度** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🚀 当前建议

**对于当前进化引擎**:

```python
# 推荐使用混合模式
class EvolvingAgent(EvolutionAgentMixin):
    def __init__(self, agent_id='lily'):
        super().__init__(agent_id=agent_id)
        
        # 全局记忆 (共享知识)
        self.global_memory = WorkMemory(
            root_dir="~/openclaw/workspace/work_memory"
        )
        
        # 个人记忆 (私有数据)
        self.personal_memory = WorkMemory(
            root_dir=f"~/openclaw/workspace/work_memory_{agent_id}"
        )
```

**使用方式**:
```python
# 共享知识保存到全局
agent.global_memory.save_document(...)

# 个人数据保存到个人
agent.personal_memory.save_daily_log(...)
```

---

**总结**: 工作记忆系统**支持灵活配置**，可根据需求选择全局/个人/混合模式！
