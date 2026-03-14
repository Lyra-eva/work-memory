# Work Memory 技能

工作记忆系统 - 专为工作场景设计的记忆管理技能，与 OpenClaw 默认记忆系统互补共存。

## 🎯 定位

- **独立运行** - 不影响 OpenClaw 核心记忆系统
- **按需调用** - 通过命令或 API 显式使用
- **物理隔离** - 数据存储在独立目录
- **未来友好** - 不依赖 OpenClaw 内部 API，框架升级不受影响

## 📦 安装

```bash
# 方式 1: 从 ClawHub 安装（推荐）
clawhub install work-memory

# 方式 2: 手动安装
cd ~/.openclaw/workspace/skills
git clone https://github.com/Lyra-eva/work-memory.git
cd work-memory
pip install -e .
```

## 🚀 快速开始

### Python API

```python
from work_memory import WorkMemory

# 初始化（首次使用自动创建目录）
wm = WorkMemory(root_dir="~/.openclaw/workspace/work-memory-data")

# 创建项目
wm.create_project("proj_001", {
    'name': 'A 股交易智能体',
    'priority': 'high',
    'description': '量化交易自动化系统'
})

# 创建任务
wm.create_task("task_001", {
    'title': '数据验证模块',
    'priority': 1,
    'project_id': 'proj_001'
})

# 写日报
wm.save_daily_log("2026-03-14", {
    'tasks_completed': ['完成数据验证', '编写测试'],
    'issues': ['API 限流问题'],
    'notes': '进展顺利'
})

# 获取统计
stats = wm.get_stats()
print(f"项目数：{stats['projects']['active']}")
print(f"任务数：{stats['tasks']['pending']}")
print(f"技能数：{stats['skills']['count']}")
```

### 命令行

```bash
# 创建项目
python -m work_memory project create "A 股智能体" --priority high

# 添加任务
python -m work_memory task add "数据验证" --project proj_001

# 查看统计
python -m work_memory stats
```

## 📋 核心功能

| 模块 | 功能 | API 示例 |
|------|------|---------|
| 项目管理 | 全生命周期管理 | `create_project()`, `update_project_status()` |
| 任务管理 | 状态流转追踪 | `create_task()`, `complete_task()` |
| 技能成长 | 分类管理 | `add_skill()`, `get_skills()` |
| 知识文档 | 存储与搜索 | `save_document()`, `search_documents()` |
| 人际关系 | 联系人管理 | `add_contact()`, `get_contact()` |
| 会议记录 | 纪要 + 待办 | `save_meeting_note()` |
| 工作日志 | 日报/周报/月报 | `save_daily_log()` |
| 备份恢复 | 完整备份 | `backup()`, `restore()` |

## 🔧 配置

在 `TOOLS.md` 中添加工作记忆配置：

```markdown
### Work Memory

- 数据目录：`~/.openclaw/workspace/work-memory-data/`
- 备份目录：`~/.openclaw/workspace/work-memory-backups/`
- 自动备份：每天 23:00
- 默认项目：无（需手动指定）
```

## 📊 与 OpenClaw 默认记忆的关系

| 维度 | OpenClaw 默认记忆 | Work Memory |
|------|-----------------|-------------|
| **用途** | 对话记忆、用户偏好、AI 进化 | 工作管理、项目追踪 |
| **存储** | `memory/cognition/graph.db` | `work-memory-data/` |
| **调用方式** | 自动管理 | 显式调用 |
| **数据格式** | SQLite + Markdown | JSON + Markdown |
| **人类可读性** | 需工具查看 | 直接浏览编辑 |

**最佳实践**：
- 用户偏好、对话历史 → 用 OpenClaw 默认记忆
- 项目、任务、工作日志 → 用 Work Memory

## 🔄 数据迁移

从 OpenClaw 默认记忆迁移：

```bash
# 一键迁移（一次性）
python scripts/migrate_memory.py --opclaw
```

迁移内容：
- `MEMORY.md` → `work-memory-data/preferences/`
- `memory/YYYY-MM-DD.md` → `work-memory-data/logs/daily/`

## 🛡️ 安全与隐私

- ✅ 数据本地存储
- ✅ 不上传云端
- ✅ 支持加密备份
- ✅ 与 OpenClaw 默认记忆隔离

## 📖 更多文档

- [架构说明](ARCHITECTURE.md)
- [API 参考](API_REFERENCE.md)
- [使用示例](examples/)
- [迁移指南](MIGRATION.md)
