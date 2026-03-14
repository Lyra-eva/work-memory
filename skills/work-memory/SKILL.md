---
name: work-memory
description: Work Memory - 工作记忆系统，专为工作场景设计的项目/任务/日志管理工具
author: OpenClaw Community
version: 2.0.0
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3", "pip"] }
      }
  }
---

# Work Memory Skill

工作记忆系统 - 专为工作场景设计的文件系统记忆架构。

## 🚀 一键安装

**只需一个命令**：

```bash
clawhub install work-memory
```

**说明**：
- ✅ 自动下载技能
- ✅ 自动安装 Python 核心库（`pip install work-memory`）
- ✅ 自动配置完成

如果自动安装失败，请手动执行：
```bash
pip install work-memory
```

---

## 📋 快速开始

### 命令式使用

```
/wm project create "A 股智能体" --priority high
/wm task add "数据验证" --project proj_001
/wm stats
/wm log daily --tasks "任务 1,任务 2" --notes "进展顺利"
```

### Python API

```python
from work_memory import WorkMemory

wm = WorkMemory()
wm.create_project("proj_001", {'name': '项目名称'})
wm.create_task("task_001", {'title': '任务标题'})
```

---

## 📦 完整文档

- [使用文档](README.md)
- [快速开始](QUICKSTART.md)
- [架构说明](ARCHITECTURE.md)
- [集成指南](INTEGRATION_GUIDE.md)

---

## 🎯 核心功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 项目管理 | `/wm project create <name>` | 创建/列出/完成项目 |
| 任务管理 | `/wm task add <title>` | 添加/列出/完成任务 |
| 工作日志 | `/wm log daily` | 日报/周报/月报 |
| 技能追踪 | `/wm skill add <name>` | 记录技能成长 |
| 统计信息 | `/wm stats` | 查看工作统计 |

---

## 🔧 配置

在 `TOOLS.md` 中添加：

```markdown
### Work Memory

- 数据目录：`~/.openclaw/workspace/work-memory-data/`
- 自动备份：每天 23:00
```

---

**Happy Coding! 🚀**
