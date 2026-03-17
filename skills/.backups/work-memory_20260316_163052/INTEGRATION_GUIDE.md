# Work Memory OpenClaw 集成指南

## 🎯 集成架构

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw Framework                    │
│  (框架升级时自动更新，不影响插件)                         │
└─────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────┐
│              Skills/Plugins Layer (插件层)               │
│  ┌─────────────────────────────────────────────────┐   │
│  │  work-memory/                                    │   │
│  │  ├── SKILL.md           # 技能说明               │   │
│  │  ├── work_memory_plugin.py # 插件核心 ⭐         │   │
│  │  ├── example_usage.py   # 使用示例               │   │
│  │  ├── README.md          # 使用文档               │   │
│  │  └── install.sh         # 安装脚本               │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────┐
│              Work Memory Core (核心库)                   │
│  work-memory-project/                                    │
│  ├── work_memory/__init__.py  # 核心实现                │
│  ├── scripts/migrate_memory.py # 迁移工具               │
│  └── setup.py                 # 包管理                   │
└─────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────┐
│              File System (数据存储)                      │
│  ~/.openclaw/workspace/work-memory-data/                │
│  ├── projects/  # 项目数据                               │
│  ├── tasks/     # 任务数据                               │
│  ├── skills/    # 技能数据                               │
│  ├── logs/      # 工作日志                               │
│  └── backups/   # 备份                                   │
└─────────────────────────────────────────────────────────┘
```

---

## ✅ 集成优势

### 1. **不影响 OpenClaw 框架升级**
- ✅ 插件层与框架层解耦
- ✅ OpenClaw 升级时，插件不受影响
- ✅ 插件可以独立更新和维护

### 2. **数据隔离**
- ✅ 工作记忆数据：`work-memory-data/`
- ✅ OpenClaw 默认记忆：`memory/`
- ✅ 两者互不干扰，可按需使用

### 3. **灵活配置**
- ✅ 数据目录可配置
- ✅ 可选择性启用功能
- ✅ 支持多个实例（个人/团队隔离）

### 4. **易于扩展**
- ✅ 基于 Python 包，易于分发
- ✅ 可发布到 PyPI
- ✅ 可通过 ClawHub 分享

---

## 📦 安装方式

### 方式 1: 一键安装脚本（推荐）

```bash
cd ~/.openclaw/workspace/skills/work-memory
./install.sh
```

### 方式 2: 手动安装

```bash
# 1. 安装核心库
cd ~/.openclaw/workspace/work-memory-project
pip install -e .

# 2. 验证安装
python3 -c "from work_memory import WorkMemory; print('✅ 核心库 OK')"

# 3. 使用插件
cd ~/.openclaw/workspace/skills/work-memory
python3 -c "from work_memory_plugin import WorkMemoryPlugin; print('✅ 插件 OK')"
```

### 方式 3: 从 ClawHub 安装（未来）

```bash
clawhub install work-memory
```

---

## 🚀 使用方式

### 1. 在 OpenClaw 技能中直接使用

```python
# skills/my-skill/SKILL.md
from work_memory_plugin import WorkMemoryPlugin

class MySkill:
    def __init__(self):
        self.wm = WorkMemoryPlugin()
    
    def handle_request(self, user_message):
        if "项目" in user_message:
            return self.wm.create_project(user_message)
        elif "任务" in user_message:
            return self.wm.create_task(user_message)
        else:
            return "我可以帮你管理项目和任务"
```

### 2. 通过命令调用

```python
from work_memory_plugin import handle_wm_command

# 模拟用户输入 /wm stats
response = handle_wm_command('stats', [])
print(response)

# 模拟用户输入 /wm project create "测试项目"
response = handle_wm_command('project', ['create', '测试项目'])
print(response)
```

### 3. 作为独立工具使用

```bash
# 查看统计
python3 -c "from work_memory_plugin import WorkMemoryPlugin; p = WorkMemoryPlugin(); print(p.get_stats())"

# 创建项目
python3 -c "from work_memory_plugin import WorkMemoryPlugin; p = WorkMemoryPlugin(); print(p.create_project('测试项目'))"
```

---

## 📊 与 OpenClaw 默认记忆的协作

### 职责划分

| 功能 | OpenClaw 默认记忆 | Work Memory | 说明 |
|------|-----------------|-------------|------|
| **对话历史** | ✅ 自动管理 | ❌ 不涉及 | 记住用户说过的话 |
| **用户偏好** | ✅ 自动管理 | ❌ 不涉及 | 如"喜欢用表格" |
| **情绪识别** | ✅ 自动分析 | ❌ 不涉及 | 理解用户情感 |
| **AI 进化** | ✅ OODA 循环 | ❌ 不涉及 | 自主决策改进 |
| **项目管理** | ❌ 不支持 | ✅ 专业支持 | 全生命周期管理 |
| **任务追踪** | ❌ 不支持 | ✅ 专业支持 | 状态流转 |
| **工作日志** | ❌ 不支持 | ✅ 专业支持 | 日报/周报/月报 |
| **技能成长** | ⚠️ 基础支持 | ✅ 专业支持 | 分类追踪 |
| **会议记录** | ❌ 不支持 | ✅ 专业支持 | 纪要 + 待办 |
| **人际关系** | ❌ 不支持 | ✅ 专业支持 | 联系人管理 |

### 同时使用示例

```python
# 场景：用户说"帮我记住这个项目的进展"

# 1. OpenClaw 默认记忆自动记录对话
# - 用户偏好：喜欢用表格
# - 对话历史：用户提到了项目
# - 情绪分析：用户很满意

# 2. Work Memory 显式记录工作数据
from work_memory_plugin import WorkMemoryPlugin
wm = WorkMemoryPlugin()

# 更新项目状态
wm.update_project_status("proj_001", "completed")

# 记录工作日志
wm.save_daily_log(tasks_completed=["完成项目"], notes="用户很满意")
```

---

## 🔧 配置选项

### 1. 数据目录配置

在 `TOOLS.md` 中配置：

```markdown
### Work Memory

- 数据目录：`~/.openclaw/workspace/work-memory-data/`
- 备份目录：`~/.openclaw/workspace/work-memory-backups/`
```

或在代码中指定：

```python
# 使用自定义目录
plugin = WorkMemoryPlugin(data_dir="/path/to/custom/data")

# 使用默认配置（从 TOOLS.md 读取）
plugin = WorkMemoryPlugin()
```

### 2. 多实例配置

```python
# 个人工作记忆
personal_wm = WorkMemoryPlugin(
    data_dir="~/.openclaw/workspace/work-memory-personal"
)

# 团队工作记忆
team_wm = WorkMemoryPlugin(
    data_dir="~/.openclaw/workspace/work-memory-team"
)

# 根据场景选择
if is_personal_task:
    wm = personal_wm
else:
    wm = team_wm
```

---

## 🔄 数据迁移

### 从 OpenClaw 默认记忆迁移

```bash
# 一键迁移
python3 ~/.openclaw/workspace/work-memory-project/scripts/migrate_memory.py --opclaw
```

迁移内容：
- `MEMORY.md` → `work-memory-data/preferences/MEMORY.md`
- `memory/YYYY-MM-DD.md` → `work-memory-data/logs/daily/`

### 迁移后验证

```python
from work_memory_plugin import WorkMemoryPlugin

plugin = WorkMemoryPlugin()
stats = plugin.get_stats()

print(f"迁移了 {stats['projects']['active']} 个项目")
print(f"迁移了 {stats['logs']['daily']} 篇日志")
```

---

## 🛡️ 安全与隐私

### 数据安全

- ✅ **本地存储** - 所有数据在本地文件系统
- ✅ **无网络请求** - 不上传云端
- ✅ **Git 友好** - 可版本控制（可选）
- ✅ **加密备份** - 支持加密备份（未来）

### 隐私保护

```python
# 个人数据隔离
personal_wm = WorkMemoryPlugin(
    data_dir="~/.openclaw/workspace/work-memory-private"
)

# 敏感项目单独存储
sensitive_project = personal_wm.create_project(
    "机密项目",
    data_dir="~/.openclaw/workspace/work-memory-encrypted"
)
```

---

## 🧪 测试与调试

### 运行测试

```bash
# 测试核心库
cd ~/.openclaw/workspace/work-memory-project
python3 -m pytest tests/

# 测试插件
cd ~/.openclaw/workspace/skills/work-memory
python3 example_usage.py

# 快速验证
python3 -c "from work_memory_plugin import WorkMemoryPlugin; p = WorkMemoryPlugin(); print(p.get_stats())"
```

### 调试技巧

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from work_memory_plugin import WorkMemoryPlugin
plugin = WorkMemoryPlugin()

# 查看详细日志
plugin.create_project("测试", debug=True)
```

---

## 📈 性能优化

### 1. 批量操作

```python
# ❌ 低效：逐个创建
for task in tasks:
    plugin.create_task(task)

# ✅ 高效：批量创建（未来支持）
plugin.create_tasks_batch(tasks)
```

### 2. 缓存统计

```python
# 缓存统计结果，避免频繁读取
from functools import lru_cache

@lru_cache(maxsize=1)
def get_cached_stats():
    return plugin.get_stats()
```

### 3. 定期清理

```python
# 清理已完成的任务
completed_tasks = plugin.get_completed_tasks()
for task in completed_tasks:
    if is_old(task):  # 超过 30 天
        plugin.archive_task(task)
```

---

## 🎯 最佳实践

### 1. 明确分工

```python
# ✅ 好：职责清晰
# OpenClaw 默认记忆：处理对话
# Work Memory: 处理工作

# ❌ 差：混为一谈
# 把所有数据都存入 Work Memory
```

### 2. 定期备份

```python
# 在 cron 中设置每天备份
# ~/.openclaw/workspace/cron/backup-work-memory.py

from work_memory_plugin import WorkMemoryPlugin
plugin = WorkMemoryPlugin()
plugin.backup()
```

### 3. 项目归档

```python
# 项目完成后及时归档
plugin.complete_project(project_id)

# 定期清理归档项目
plugin.archive_old_projects(days=90)
```

### 4. 日志习惯

```python
# 每天写工作日志
plugin.save_daily_log(
    tasks_completed=[...],
    issues=[...],
    notes="..."
)
```

---

## ❓ 常见问题

### Q: 会影响 OpenClaw 升级吗？

**A**: 不会。插件层与框架层完全解耦，OpenClaw 升级不影响插件。

### Q: 两个记忆系统会冲突吗？

**A**: 不会。物理隔离，各自独立运行。

### Q: 如何卸载？

```bash
# 删除技能
rm -rf ~/.openclaw/workspace/skills/work-memory

# 删除数据（可选）
rm -rf ~/.openclaw/workspace/work-memory-data

# 卸载核心库（可选）
pip uninstall work-memory
```

### Q: 可以只使用其中一个系统吗？

**A**: 可以。三个选项：
1. 只用 OpenClaw 默认记忆（默认）
2. 只用 Work Memory（工作场景）
3. 两者共存（推荐）

### Q: 数据会丢失吗？

**A**: 不会。建议：
- 定期备份（每天）
- 使用 Git 版本控制（可选）
- 迁移前先备份

---

## 📚 相关文档

- [技能说明](SKILL.md)
- [使用文档](README.md)
- [使用示例](example_usage.py)
- [核心库文档](../../work-memory-project/README.md)
- [架构说明](../../work-memory-project/ARCHITECTURE_EXPLANATION.md)
- [迁移指南](../../work-memory-project/MIGRATION.md)

---

## 🚀 未来计划

- [ ] 发布到 PyPI
- [ ] ClawHub 技能市场
- [ ] Web UI 管理界面
- [ ] 加密备份支持
- [ ] 团队协作功能
- [ ] 与 OpenClaw 深度集成（可选）

---

**Happy Coding! 🎉**
