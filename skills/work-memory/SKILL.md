# Work Memory Skill - OpenClaw 技能集成

工作记忆系统的 OpenClaw 技能包装器，提供便捷的命令式交互。

## 🎯 定位

本技能是 **Work Memory 核心库** 的 OpenClaw 集成层：
- **核心库** (`work-memory` PyPI 包) - 独立 Python 包，包含所有业务逻辑
- **技能层** (本技能) - OpenClaw 包装器，提供命令处理和用户交互

## 📦 安装

### 方式 1: ClawHub 安装（推荐 OpenClaw 用户）

```bash
# 自动安装核心库 + 技能
clawhub install work-memory
```

### 方式 2: 手动安装

```bash
# 1. 先安装核心库（PyPI）
pip install work-memory

# 2. 技能会自动加载（如果在 workspace/skills/ 目录）
```

### 方式 3: 开发模式

```bash
# 1. 安装核心库
cd ~/.openclaw/workspace/work-memory-project
pip install -e .

# 2. 技能已链接
# ~/.openclaw/workspace/skills/work-memory/
```

## 🚀 快速开始

### 命令式使用

```
/wm project create "A 股智能体" --priority high
/wm task add "数据验证" --project proj_001
/wm stats
/wm log daily
```

### Python API 使用

```python
from work_memory import WorkMemory

# 直接使用核心库
wm = WorkMemory(root_dir="~/work-memory-data")
wm.create_project("项目名称")
wm.create_task("任务标题")
```

## 📋 可用命令

### 项目管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `/wm project create <name>` | 创建项目 | `/wm project create "A 股智能体"` |
| `/wm project list` | 列出项目 | `/wm project list --status active` |
| `/wm project complete <id>` | 完成项目 | `/wm project complete proj_001` |

### 任务管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `/wm task add <title>` | 添加任务 | `/wm task add "数据验证"` |
| `/wm task list` | 列出任务 | `/wm task list --status pending` |
| `/wm task complete <id>` | 完成任务 | `/wm task complete task_001` |

### 工作日志

| 命令 | 说明 | 示例 |
|------|------|------|
| `/wm log daily` | 写日报 | `/wm log daily` |
| `/wm log weekly` | 写周报 | `/wm log weekly` |

### 统计信息

| 命令 | 说明 | 示例 |
|------|------|------|
| `/wm stats` | 查看统计 | `/wm stats` |

## 🔧 配置

在 `TOOLS.md` 中添加：

```markdown
### Work Memory

- 数据目录：`~/.openclaw/workspace/work-memory-data/`
- 备份目录：`~/.openclaw/workspace/work-memory-backups/`
- 自动备份：每天 23:00
```

## 📊 架构说明

```
OpenClaw Session
      ↕
Work Memory Skill (技能层 - 本技能)
      ↕
work-memory (核心库 - PyPI 包)
      ↕
File System (work-memory-data/)
```

**优势**：
- ✅ 核心库独立，不依赖 OpenClaw
- ✅ 技能层轻薄，易于维护
- ✅ 可在非 OpenClaw 环境使用核心库
- ✅ OpenClaw 升级不影响核心库

## 🛡️ 与 OpenClaw 默认记忆的关系

| 维度 | OpenClaw 默认记忆 | Work Memory |
|------|-----------------|-------------|
| **用途** | 对话记忆、用户偏好、AI 进化 | 工作管理、项目追踪 |
| **存储** | `memory/cognition/graph.db` | `work-memory-data/` |
| **调用方式** | 自动管理 | 显式调用 |
| **数据格式** | SQLite + Markdown | JSON + Markdown |

**协作方式**：互补共存，互不影响

## 📖 更多文档

- [核心库文档](https://pypi.org/project/work-memory/)
- [GitHub 仓库](https://github.com/openclaw/work-memory)
- [集成指南](INTEGRATION_GUIDE.md)
- [使用示例](example_usage.py)

## ❓ 常见问题

### Q: 必须安装核心库吗？

A: 是的。技能只是包装器，核心功能在 `work-memory` PyPI 包中。

### Q: 可以只用核心库不用技能吗？

A: 可以。在非 OpenClaw 环境中，直接使用 `from work_memory import WorkMemory`。

### Q: 会影响 OpenClaw 升级吗？

A: 不会。核心库完全独立，技能层轻薄，OpenClaw 升级影响极小。

---

**Happy Coding! 🚀**
