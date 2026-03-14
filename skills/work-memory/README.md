# Work Memory - OpenClaw 技能集成

工作记忆系统的 OpenClaw 技能包装器。

## 🎯 架构说明

本技能采用 **Plugin-Core 模式**：

```
┌─────────────────────────────────────────┐
│         work-memory (PyPI 包)            │  ← 核心库（独立）
│  - 所有业务逻辑                          │
│  - 不依赖 OpenClaw                       │
│  - 可在任何 Python 项目使用               │
└─────────────────────────────────────────┘
              ↕ 依赖
┌─────────────────────────────────────────┐
│    work-memory-skill (本技能)            │  ← 技能层（轻薄）
│  - OpenClaw 集成                         │
│  - 命令处理                              │
│  - 用户交互                              │
└─────────────────────────────────────────┘
```

**优势**：
- ✅ 核心库独立，不受 OpenClaw 升级影响
- ✅ 技能层轻薄，易于维护
- ✅ 可在非 OpenClaw 环境使用核心库

---

## 📦 安装

### 方式 1: ClawHub 安装（推荐 OpenClaw 用户）

```bash
clawhub install work-memory
```

### 方式 2: PyPI 安装核心库 + 手动配置技能

```bash
# 1. 安装核心库
pip install work-memory

# 2. 技能文件放在 workspace/skills/work-memory/
```

### 方式 3: 开发模式

```bash
# 1. 安装核心库
cd ~/.openclaw/workspace/work-memory-project
pip install -e .

# 2. 技能已链接
# ~/.openclaw/workspace/skills/work-memory/
```

---

## 🚀 使用方式

### 方式 A: 命令式（通过 OpenClaw 技能）

```
/wm project create "A 股智能体" --priority high
/wm task add "数据验证" --project proj_001
/wm stats
/wm log daily --tasks "任务 1,任务 2" --notes "进展顺利"
```

### 方式 B: Python API（技能包装器）

```python
from work_memory_plugin import WorkMemoryPlugin

plugin = WorkMemoryPlugin()

# 创建项目
result = plugin.create_project("A 股智能体", priority="high")
print(f"项目 ID: {result['project_id']}")

# 添加任务
result = plugin.create_task("数据验证", project_id=result['project_id'])
print(f"任务 ID: {result['task_id']}")

# 查看统计
stats = plugin.get_stats()
print(f"项目数：{stats['projects']['active']}")
```

### 方式 C: 直接使用核心库（推荐开发者）

```python
from work_memory import WorkMemory

wm = WorkMemory(root_dir="~/work-memory-data")

# 创建项目
wm.create_project("proj_001", {'name': 'A 股智能体'})

# 添加任务
wm.create_task("task_001", {'title': '数据验证', 'project_id': 'proj_001'})

# 查看统计
stats = wm.get_stats()
```

---

## 📋 核心功能

### 项目管理

```python
# 创建
plugin.create_project("项目名称", priority="high")

# 列出
projects = plugin.list_projects('active')

# 完成
plugin.complete_project("proj_001")
```

### 任务管理

```python
# 添加
plugin.create_task("任务标题", project_id="proj_001")

# 获取待办
tasks = plugin.get_pending_tasks()

# 完成
plugin.complete_task("task_001")
```

### 工作日志

```python
plugin.save_daily_log(
    date="2026-03-14",
    tasks_completed=["任务 1", "任务 2"],
    issues=["问题 1"],
    notes="备注"
)
```

### 技能追踪

```python
plugin.add_skill("Python", level="expert", category="technical")
skills = plugin.get_skills()
```

### 统计信息

```python
stats = plugin.get_stats()
print(stats)
```

---

## 🔧 配置

在 `TOOLS.md` 中添加：

```markdown
### Work Memory

- 数据目录：`~/.openclaw/workspace/work-memory-data/`
- 备份目录：`~/.openclaw/workspace/work-memory-backups/`
- 自动备份：每天 23:00
```

或在代码中指定：

```python
# 自定义数据目录
plugin = WorkMemoryPlugin(root_dir="~/my-work-memory")
```

---

## 📊 与 OpenClaw 默认记忆的关系

| 维度 | OpenClaw 默认记忆 | Work Memory |
|------|-----------------|-------------|
| **用途** | 对话记忆、用户偏好、AI 进化 | 工作管理、项目追踪 |
| **存储** | `memory/cognition/graph.db` | `work-memory-data/` |
| **调用方式** | 自动管理 | 显式调用 |
| **数据格式** | SQLite + Markdown | JSON + Markdown |

**协作方式**：互补共存，互不影响

---

## 🧪 测试

```bash
# 测试技能
cd ~/.openclaw/workspace/skills/work-memory
python3 work_memory_skill.py

# 测试插件
python3 work_memory_plugin.py

# 测试核心库
cd ~/.openclaw/workspace/work-memory-project
python3 -m work_memory
```

---

## 📖 更多文档

- [技能说明](SKILL.md)
- [集成指南](INTEGRATION_GUIDE.md)
- [完成总结](SUMMARY.md)
- [核心库文档](../../work-memory-project/README.md)
- [使用示例](example_usage.py)

---

## ❓ 常见问题

### Q: 必须安装核心库吗？

A: 是的。技能只是包装器，核心功能在 `work-memory` PyPI 包中。

### Q: 可以只用核心库不用技能吗？

A: 可以。在非 OpenClaw 环境中，直接使用 `from work_memory import WorkMemory`。

### Q: 会影响 OpenClaw 升级吗？

A: 不会。核心库完全独立，技能层轻薄，OpenClaw 升级影响极小。

### Q: 数据存在哪里？

A: 默认在 `~/.openclaw/workspace/work-memory-data/`，可配置。

---

**Happy Coding! 🚀**
