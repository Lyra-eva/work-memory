# Work Memory 技能 - OpenClaw 集成指南

## 📦 安装步骤

### 1. 安装工作记忆核心库

```bash
cd ~/.openclaw/workspace/work-memory-project
pip install -e .
```

### 2. 复制技能文件

技能文件已放置在：
```
~/.openclaw/workspace/skills/work-memory/
├── SKILL.md                    # 技能说明
├── work_memory_plugin.py       # 插件核心
├── example_usage.py            # 使用示例
└── README.md                   # 本文档
```

### 3. 配置数据目录（可选）

在 `~/.openclaw/workspace/TOOLS.md` 中添加：

```markdown
### Work Memory

- 数据目录：`~/.openclaw/workspace/work-memory-data/`
- 备份目录：`~/.openclaw/workspace/work-memory-backups/`
- 自动备份：每天 23:00
```

---

## 🚀 快速开始

### 方式 1: Python API

```python
from work_memory_plugin import WorkMemoryPlugin

# 初始化
plugin = WorkMemoryPlugin()

# 创建项目
result = plugin.create_project("A 股智能体", priority="high")
print(result['message'])

# 添加任务
result = plugin.create_task("数据验证", project_id=result['project_id'])
print(result['message'])

# 查看统计
stats = plugin.get_stats()
print(f"项目数：{stats['projects']['active']}")
```

### 方式 2: 命令处理

```python
from work_memory_plugin import handle_wm_command

# 模拟用户输入
response = handle_wm_command('stats', [])
print(response)

response = handle_wm_command('project', ['create', '测试项目'])
print(response)
```

---

## 📋 在 OpenClaw 技能中使用

### 示例：项目助手技能

创建 `~/.openclaw/workspace/skills/project-assistant/SKILL.md`:

```markdown
# Project Assistant 技能

项目助手 - 基于 Work Memory 的项目管理技能

## 依赖

```bash
pip install -e ~/.openclaw/workspace/work-memory-project
```

## 用法

在技能代码中导入 Work Memory:

```python
from work_memory_plugin import WorkMemoryPlugin

class ProjectAssistant:
    def __init__(self):
        self.wm = WorkMemoryPlugin()
    
    def create_project(self, name, priority='medium'):
        result = self.wm.create_project(name, priority=priority)
        return result['message']
    
    def add_task(self, title, project_id=None):
        result = self.wm.create_task(title, project_id=project_id)
        return result['message']
```
```

---

## 🔧 配置选项

### 环境变量

```bash
# 设置数据目录
export WORK_MEMORY_DATA_DIR="~/.openclaw/workspace/work-memory-data"

# 设置备份目录
export WORK_MEMORY_BACKUP_DIR="~/.openclaw/workspace/work-memory-backups"
```

### Python 配置

```python
# 自定义数据目录
plugin = WorkMemoryPlugin(data_dir="/path/to/your/data")

# 使用默认配置（从 TOOLS.md 读取）
plugin = WorkMemoryPlugin()
```

---

## 📊 与 OpenClaw 默认记忆的协作

### 职责划分

| 场景 | 使用哪个系统 | 示例 |
|------|------------|------|
| 用户偏好记忆 | OpenClaw 默认 | "记住我喜欢吃辣" |
| 对话历史 | OpenClaw 默认 | 自动记录 |
| AI 进化决策 | OpenClaw 默认 | OODA 循环 |
| 项目管理 | Work Memory | "创建一个项目" |
| 任务追踪 | Work Memory | "添加待办事项" |
| 工作日志 | Work Memory | "写日报" |
| 技能成长 | Work Memory | "记录新学的技能" |

### 同时使用两个系统

```python
# OpenClaw 默认记忆（自动管理，无需显式调用）
# - 对话历史
# - 用户偏好
# - 情绪识别

# Work Memory（显式调用）
from work_memory_plugin import WorkMemoryPlugin
wm = WorkMemoryPlugin()

# 工作相关数据
wm.create_project("A 股智能体")
wm.save_daily_log(tasks_completed=[...])
```

---

## 🔄 数据迁移

### 从 OpenClaw 默认记忆迁移

```bash
# 一键迁移（一次性）
python ~/.openclaw/workspace/work-memory-project/scripts/migrate_memory.py --opclaw
```

迁移内容：
- `MEMORY.md` → `work-memory-data/preferences/`
- `memory/YYYY-MM-DD.md` → `work-memory-data/logs/daily/`

### 迁移后验证

```python
from work_memory_plugin import WorkMemoryPlugin

plugin = WorkMemoryPlugin()
stats = plugin.get_stats()

print(f"迁移了 {stats['projects']['active']} 个项目")
print(f"迁移了 {stats['tasks']['pending']} 个任务")
```

---

## 🛡️ 安全与隐私

- ✅ **数据本地存储** - 所有数据在本地文件系统
- ✅ **不上传云端** - 无网络请求
- ✅ **与 OpenClaw 隔离** - 独立目录，互不影响
- ✅ **支持备份** - 可手动或自动备份

### 备份策略

```python
# 手动备份
plugin = WorkMemoryPlugin()
result = plugin.backup()
print(f"备份到：{result['backup_path']}")

# 自动备份（通过 cron）
# 在 ~/.openclaw/workspace/cron/work-memory-backup.py 中:
from work_memory_plugin import WorkMemoryPlugin
plugin = WorkMemoryPlugin()
plugin.backup()
```

---

## 🧪 测试

运行示例代码：

```bash
cd ~/.openclaw/workspace/skills/work-memory
python example_usage.py
```

---

## 📖 更多资源

- [Work Memory 核心库文档](../../work-memory-project/README.md)
- [架构说明](../../work-memory-project/ARCHITECTURE_EXPLANATION.md)
- [API 参考](../../work-memory-project/API_REFERENCE.md)
- [迁移指南](../../work-memory-project/MIGRATION.md)

---

## ❓ 常见问题

### Q: 会影响 OpenClaw 升级吗？

A: **不会**。Work Memory 是独立技能，不修改 OpenClaw 核心代码。

### Q: 数据存在哪里？

A: 默认在 `~/.openclaw/workspace/work-memory-data/`，可配置。

### Q: 如何卸载？

A: 
```bash
# 删除技能
rm -rf ~/.openclaw/workspace/skills/work-memory

# 删除数据（可选）
rm -rf ~/.openclaw/workspace/work-memory-data
```

### Q: 可以和默认记忆系统一起用吗？

A: **可以且推荐**。两个系统互补：
- 默认记忆：对话/偏好/进化
- Work Memory: 项目/任务/日志

---

## 🎯 最佳实践

1. **明确分工** - 对话用默认记忆，工作用 Work Memory
2. **定期备份** - 设置每天自动备份
3. **项目归档** - 完成的项目及时归档
4. **任务清理** - 已完成的任务定期清理
5. **日志习惯** - 每天写工作日志

---

**Happy Coding! 🚀**
