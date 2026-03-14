# Work Memory 架构文档

## 🎯 Plugin-Core 架构

Work Memory 采用 **Plugin-Core（插件 - 核心）架构**，将业务逻辑与框架集成完全分离。

---

## 📐 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│  ┌────────────────┐         ┌─────────────────────┐    │
│  │  OpenClaw Skill │         │  Python Application │    │
│  │  (命令处理)     │         │  (直接使用)          │    │
│  └────────┬───────┘         └──────────┬──────────┘    │
│           │                            │                 │
│           ▼                            ▼                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │      work_memory_plugin.py (轻薄包装器)          │   │
│  │      - OpenClaw 友好接口                         │   │
│  │      - 命令路由                                  │   │
│  │      - 用户交互                                  │   │
│  └────────┬────────────────────────────────────────┘   │
│           │                                            │
│           ▼                                            │
│  ┌─────────────────────────────────────────────────┐   │
│  │      work-memory (PyPI 包) - 核心库 ⭐           │   │
│  │      - 所有业务逻辑                              │   │
│  │      - 文件系统操作                              │   │
│  │      - 数据管理                                  │   │
│  │      - 不依赖任何框架                            │   │
│  └────────┬────────────────────────────────────────┘   │
│           │                                            │
│           ▼                                            │
│  ┌─────────────────────────────────────────────────┐   │
│  │         File System (work-memory-data/)          │   │
│  │  projects/ tasks/ skills/ logs/ ...             │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🏗️ 分层说明

### 1. 核心库层（Core Layer）

**位置**: `work-memory-project/` → PyPI 包 `work-memory`

**职责**:
- ✅ 所有业务逻辑实现
- ✅ 文件系统操作
- ✅ 数据格式管理
- ✅ 备份恢复

**特点**:
- ✅ **零依赖** - 不依赖 OpenClaw 或任何框架
- ✅ **可移植** - 可在任何 Python 项目中使用
- ✅ **可测试** - 独立单元测试
- ✅ **稳定** - API 稳定，向后兼容

**示例**:
```python
from work_memory import WorkMemory

wm = WorkMemory(root_dir="~/work-memory-data")
wm.create_project("proj_001", {'name': '项目名称'})
wm.create_task("task_001", {'title': '任务标题'})
```

---

### 2. 插件包装层（Plugin Layer）

**位置**: `skills/work-memory/work_memory_plugin.py`

**职责**:
- ✅ 提供 OpenClaw 友好的接口
- ✅ 简化 API 调用
- ✅ 命令处理（可选）

**特点**:
- ✅ **轻薄** - 只调用核心库，不包含业务逻辑
- ✅ **易维护** - 核心库变化时只需少量调整
- ✅ **向后兼容** - 保留旧 API

**示例**:
```python
from work_memory_plugin import WorkMemoryPlugin

plugin = WorkMemoryPlugin()
plugin.create_project("项目名称")  # 内部调用核心库
```

---

### 3. 技能层（Skill Layer）

**位置**: `skills/work-memory/work_memory_skill.py`

**职责**:
- ✅ OpenClaw 技能入口
- ✅ 命令解析和处理
- ✅ 用户交互

**特点**:
- ✅ **框架特定** - 依赖 OpenClaw 技能系统
- ✅ **易于替换** - 如果 OpenClaw 技能系统变化，可快速重写
- ✅ **用户友好** - 提供命令式交互

**示例**:
```python
# OpenClaw 技能调用
from work_memory_skill import handle_wm_command

response = handle_wm_command('project', ['create', '测试项目'])
```

---

## 📊 依赖关系

```
OpenClaw Framework
      ↓
work_memory_skill.py (技能层)
      ↓
work_memory_plugin.py (插件层)
      ↓
work_memory (核心库) ← 零依赖
      ↓
File System
```

**关键点**:
- ⬆️ **上层依赖下层**
- ⬇️ **下层不依赖上层**
- ✅ **核心库完全独立**

---

## 🎯 架构优势

### 1. 抗框架升级风险

| 变化类型 | 影响范围 | 工作量 |
|---------|---------|-------|
| OpenClaw 核心升级 | 技能层 | 小（可能无需改动） |
| 技能系统 API 变化 | 技能层 | 中（重写技能入口） |
| 数据格式变化 | 核心库 | 中（核心库更新） |
| Python 版本升级 | 核心库 | 小（兼容性测试） |

**关键**: 核心库不受 OpenClaw 升级影响。

---

### 2. 多平台支持

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  OpenClaw    │    │  LangChain   │    │  独立 CLI    │
│    Skill     │    │    Tool      │    │    Tool      │
└──────┬───────┘    └──────┬───────┘    └──────┬───────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           ↓
              ┌────────────────────────┐
              │   work_memory (Core)   │
              └───────────┬────────────┘
                          ↓
                   File System
```

**核心库可被多个框架复用**。

---

### 3. 易于测试

```python
# 核心库测试（独立）
def test_create_project():
    wm = WorkMemory(root_dir="/tmp/test")
    wm.create_project("proj_001", {'name': 'Test'})
    assert os.path.exists(...)

# 技能层测试（Mock 核心库）
def test_skill_command():
    with patch('work_memory.WorkMemory') as MockWM:
        response = handle_wm_command('stats', [])
        assert '统计' in response
```

---

### 4. 分发灵活

**渠道 1: PyPI**
```bash
pip install work-memory
```

**渠道 2: ClawHub**
```bash
clawhub install work-memory
```

**渠道 3: 源码**
```bash
git clone https://github.com/openclaw/work-memory
cd work-memory-project
pip install -e .
```

---

## 🔄 数据流

### 创建项目的数据流

```
用户输入：/wm project create "A 股智能体"
    ↓
OpenClaw 技能系统
    ↓
work_memory_skill.py (解析命令)
    ↓
work_memory_plugin.py (可选层)
    ↓
WorkMemory.create_project() (核心库)
    ↓
FileSystem: ~/work-memory-data/projects/active/proj_xxx.json
```

---

## 🛡️ 安全边界

```
┌─────────────────────────────────────┐
│         Trust Boundary              │
│                                     │
│  ┌─────────────────────────────┐   │
│  │   Skill/Plugin Layer        │   │
│  │   - 输入验证                │   │
│  │   - 命令解析                │   │
│  │   - 错误处理                │   │
│  └─────────────┬───────────────┘   │
│                │                    │
│  ┌─────────────▼───────────────┐   │
│  │   Core Layer                │   │
│  │   - 业务逻辑                │   │
│  │   - 数据验证                │   │
│  │   - 文件系统操作            │   │
│  └─────────────┬───────────────┘   │
│                │                    │
└────────────────┼────────────────────┘
                 ↓
          File System
```

**安全原则**:
- ✅ 上层处理输入验证
- ✅ 核心库假设输入已验证
- ✅ 文件系统操作在沙箱内

---

## 📈 演进路线

### Phase 1 (2026 Q2): Skill-First

```
OpenClaw Skill (主要入口)
      ↓
work_memory (核心库)
```

**目标**: 快速融入 OpenClaw 生态

---

### Phase 2 (2026 Q3-Q4): Plugin-Core

```
OpenClaw Skill + PyPI (双渠道)
      ↓              ↓
work_memory_plugin  work_memory (核心库)
```

**目标**: 降低耦合，支持多平台

**状态**: ✅ **当前阶段**

---

### Phase 3 (2027+): Ecosystem

```
OpenClaw + LangChain + CLI + Web
      ↓         ↓         ↓       ↓
         work_memory (核心库)
```

**目标**: 成为工作记忆标准

---

## 🎯 设计决策

### 为什么选择 Plugin-Core？

**对比 Pure-Skill**:
| 维度 | Pure-Skill | Plugin-Core |
|------|-----------|-------------|
| OpenClaw 集成 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 框架升级风险 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 可移植性 | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| 维护成本 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**对比 Pure-Plugin**:
| 维度 | Pure-Plugin | Plugin-Core |
|------|------------|-------------|
| OpenClaw 集成 | ⭐⭐ | ⭐⭐⭐⭐ |
| 用户便利性 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 生态整合 | ⭐⭐ | ⭐⭐⭐⭐⭐ |

**结论**: Plugin-Core 结合了两者优势。

---

## 📋 最佳实践

### 1. 核心库使用

```python
# ✅ 推荐：直接使用核心库
from work_memory import WorkMemory
wm = WorkMemory()
wm.create_project(...)

# ⚠️ 不推荐：在业务逻辑中使用技能层
from work_memory_skill import handle_wm_command
```

### 2. 技能层使用

```python
# ✅ 推荐：在 OpenClaw 技能中使用
from work_memory_skill import handle_wm_command
response = handle_wm_command('stats', [])

# ✅ 推荐：在技能中调用插件层
from work_memory_plugin import WorkMemoryPlugin
plugin = WorkMemoryPlugin()
```

### 3. 测试

```python
# ✅ 推荐：核心库独立测试
def test_core():
    wm = WorkMemory(root_dir="/tmp/test")
    ...

# ✅ 推荐：技能层 Mock 测试
def test_skill():
    with patch('work_memory.WorkMemory'):
        ...
```

---

## 🔗 相关文档

- [技能说明](SKILL.md)
- [使用文档](README.md)
- [集成指南](INTEGRATION_GUIDE.md)
- [核心库文档](../../work-memory-project/README.md)

---

**Architecture Version**: 2.0 (Plugin-Core)  
**Last Updated**: 2026-03-14
