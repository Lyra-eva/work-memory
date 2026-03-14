# 📋 Work Memory 部署范围说明

**问题**: 安装后是否覆盖所有智能体？新建智能体是否自动部署？

**答案**: **不是全局覆盖，需要手动集成**

---

## 🏗️ 当前架构

### 安装方式

```bash
pip3 install --user git+https://github.com/Lyra-eva/work-memory.git
```

**安装位置**: 
- 用户级 Python 包 (`~/.local/lib/python3.6/site-packages/work_memory/`)
- **不是** OpenClaw 全局组件

---

## 📊 部署范围

### 当前状态

| 范围 | 状态 | 说明 |
|------|------|------|
| **OpenClaw 全局** | ❌ 未集成 | 不是 OpenClaw 内置组件 |
| **所有智能体** | ❌ 未覆盖 | 需要手动导入使用 |
| **新建智能体** | ❌ 不自动部署 | 需要手动安装 |
| **当前工作区** | ✅ 已安装 | 仅当前 Python 环境可用 |

---

## 🔧 使用方式

### 方式 1: 在智能体代码中导入

```python
# 在智能体代码中
from work_memory import WorkMemory

class MyAgent:
    def __init__(self, agent_id='lily'):
        # 每个智能体独立的记忆系统
        self.memory = WorkMemory(
            root_dir=f"~/work_memory_{agent_id}"
        )
```

**特点**:
- ✅ 每个智能体独立配置
- ✅ 可以自定义根目录
- ❌ 需要手动集成到每个智能体

---

### 方式 2: 作为 OpenClaw Skill

```python
# skills/work_memory_skill/__init__.py

from work_memory import WorkMemory

class WorkMemorySkill:
    def __init__(self):
        self.memory = WorkMemory()
    
    def create_project(self, name, data):
        return self.memory.create_project(name, data)
    
    # ... 其他方法
```

**特点**:
- ✅ 所有智能体可通过 skill 调用
- ✅ 统一管理
- ❌ 需要创建 skill 包

---

### 方式 3: 全局单例模式

```python
# global_memory.py

from work_memory import WorkMemory

# 全局单例
GLOBAL_MEMORY = WorkMemory(
    root_dir="~/openclaw/global_work_memory"
)

# 所有智能体共享
def get_memory():
    return GLOBAL_MEMORY
```

**特点**:
- ✅ 所有智能体共享同一记忆
- ✅ 统一管理
- ❌ 无隐私隔离

---

## 🎯 推荐方案

### 方案 A: 混合模式 (推荐) ⭐⭐⭐⭐⭐

```python
# integration/smart_agent.py

from work_memory import WorkMemory

class SmartAgent:
    def __init__(self, agent_id='lily'):
        # 全局记忆 (共享知识)
        self.global_memory = WorkMemory(
            root_dir="~/openclaw/workspace/global_work_memory"
        )
        
        # 个人记忆 (私有数据)
        self.personal_memory = WorkMemory(
            root_dir=f"~/openclaw/workspace/work_memory_{agent_id}"
        )
    
    def create_project(self, name, data):
        # 项目存全局
        return self.global_memory.create_project(name, data)
    
    def save_daily_log(self, date, data):
        # 日志存个人
        return self.personal_memory.save_daily_log(date, data)
```

**优势**:
- ✅ 知识共享
- ✅ 隐私保护
- ✅ 灵活配置

---

### 方案 B: Skill 模式 ⭐⭐⭐⭐

```python
# 1. 创建 skill 包
mkdir -p skills/work_memory

# 2. 实现 skill
cat > skills/work_memory/__init__.py << 'EOF'
from work_memory import WorkMemory

class WorkMemorySkill:
    def __init__(self, agent_id=None):
        root_dir = f"~/work_memory_{agent_id}" if agent_id else "~/work_memory"
        self.memory = WorkMemory(root_dir=root_dir)
    
    def create_project(self, project_id, data):
        return self.memory.create_project(project_id, data)
    
    # ... 其他方法

# 导出
__all__ = ['WorkMemorySkill']
EOF

# 3. 在智能体中使用
from skills.work_memory import WorkMemorySkill

skill = WorkMemorySkill(agent_id='lily')
skill.create_project('proj_001', {...})
```

**优势**:
- ✅ 统一接口
- ✅ 易于管理
- ✅ 可配置

---

### 方案 C: 环境变量配置 ⭐⭐⭐

```bash
# 设置全局记忆目录
export WORK_MEMORY_ROOT="~/openclaw/workspace/global_work_memory"

# Python 中使用
import os
from work_memory import WorkMemory

wm = WorkMemory(root_dir=os.getenv('WORK_MEMORY_ROOT'))
```

**优势**:
- ✅ 集中配置
- ✅ 易于部署
- ❌ 无隐私隔离

---

## 📋 部署检查清单

### 全局部署 (所有智能体)

- [ ] 创建全局记忆目录
- [ ] 配置环境变量
- [ ] 创建全局 Skill
- [ ] 更新智能体基类
- [ ] 测试共享功能

### 个人部署 (单个智能体)

- [ ] 安装 work-memory 包
- [ ] 在智能体代码中导入
- [ ] 配置个人记忆目录
- [ ] 测试基本功能

### 新建智能体自动部署

- [ ] 创建智能体模板
- [ ] 在模板中包含 work-memory
- [ ] 配置自动安装脚本
- [ ] 测试新智能体

---

## 🚀 实施建议

### 对于当前环境

**推荐**: 方案 A (混合模式)

```python
# 在现有智能体中添加
from work_memory import WorkMemory

# 全局记忆
global_wm = WorkMemory(root_dir="~/openclaw/workspace/global_work_memory")

# 个人记忆
personal_wm = WorkMemory(root_dir="~/openclaw/workspace/work_memory_lily")
```

---

### 对于新建智能体

**推荐**: 创建智能体模板

```bash
# 模板结构
agent_template/
├── __init__.py
├── agent.py
├── requirements.txt  # 包含 work-memory
└── config.py        # 记忆配置
```

**requirements.txt**:
```txt
work-memory>=2.0.0
```

**config.py**:
```python
import os
from work_memory import WorkMemory

# 全局记忆
GLOBAL_MEMORY = WorkMemory(
    root_dir=os.getenv('GLOBAL_WORK_MEMORY', '~/global_work_memory')
)

# 个人记忆
PERSONAL_MEMORY = WorkMemory(
    root_dir=os.getenv('PERSONAL_WORK_MEMORY', '~/personal_work_memory')
)
```

---

## 📊 对比总结

| 方案 | 覆盖范围 | 隐私性 | 灵活性 | 推荐场景 |
|------|---------|-------|-------|---------|
| **全局单例** | 所有智能体 | ❌ 低 | ⚠️ 中 | 知识共享 |
| **Skill 模式** | 所有智能体 | ✅ 中 | ✅ 高 | 统一管理 |
| **混合模式** | 可配置 | ✅ 高 | ✅ 高 | 推荐 |
| **个人部署** | 单个智能体 | ✅ 高 | ✅ 高 | 独立使用 |

---

## 🎯 最终答案

**Q**: 安装后是否覆盖所有智能体？

**A**: ❌ **不会**。work-memory 是独立 Python 包，需要手动集成到每个智能体。

---

**Q**: 新建智能体是否自动部署？

**A**: ❌ **不会**。需要在新智能体的 requirements.txt 中添加并导入使用。

---

**Q**: 如何实现全局覆盖？

**A**: 创建 OpenClaw Skill 或基类，所有智能体继承使用。

---

**Q**: 推荐方案？

**A**: 混合模式 - 全局记忆共享知识 + 个人记忆保护隐私。

---

**总结**: work-memory 是**可选组件**，需要**手动集成**，**不会自动覆盖**所有智能体。
