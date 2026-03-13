# Work Memory - 工作记忆系统

<div align="center">

![Work Memory Banner](docs/assets/banner.png)

[![PyPI version](https://badge.fury.io/py/work-memory.svg)](https://badge.fury.io/py/work-memory)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**专为工作场景设计的文件系统记忆架构**

[English](README.md) | [中文](docs/README_zh.md)

</div>

---

## 📋 简介

Work Memory 是一个专为工作场景设计的记忆系统，借鉴了 memU 的文件系统设计理念，提供：

- 📁 **项目管理** - 全生命周期管理 (active/completed/archived)
- ✅ **任务管理** - 状态流转追踪 (pending/in_progress/completed)
- 📚 **技能成长** - 分类管理 (technical/soft/certifications)
- 📄 **知识文档** - 文档存储与搜索
- 👥 **人际关系** - 联系人管理 (colleagues/clients/partners)
- 📝 **会议记录** - 会议纪要 + 待办事项
- 📊 **工作日志** - 日报/周报/月报

---

## 🚀 快速开始

### 安装

```bash
# 从 PyPI 安装
pip install work-memory

# 从 GitHub 安装
pip install git+https://github.com/openclaw/work-memory.git

# 开发模式安装
git clone https://github.com/openclaw/work-memory.git
cd work-memory
pip install -e .
```

### 基础使用

```python
from work_memory import WorkMemory

# 初始化
wm = WorkMemory(root_dir="~/work_memory")

# 创建项目
wm.create_project("proj_001", {
    'name': '进化引擎 5.0',
    'description': '下一代进化引擎',
    'priority': 'high'
})

# 创建任务
wm.create_task("task_001", {
    'title': '实现图谱关系',
    'priority': 1,
    'due_date': '2026-03-15',
    'project_id': 'proj_001'
})

# 添加技能
wm.add_skill("python_advanced", {
    'level': 'expert',
    'description': '高级 Python 编程'
})

# 保存文档
wm.save_document(
    doc_id="python_tips",
    content="# Python 技巧\n\n...",
    category="technical"
)

# 统计信息
stats = wm.get_stats()
print(f"项目数：{stats['projects']['active']}")
print(f"任务数：{stats['tasks']['pending']}")
```

---

## 📖 功能特性

### 1. 项目管理

```python
# 创建项目
wm.create_project("proj_001", {
    'name': '项目名称',
    'description': '项目描述',
    'start_date': '2026-03-01',
    'priority': 'high'
})

# 更新状态
wm.update_project_status("proj_001", "completed")

# 列出项目
projects = wm.list_projects(status='active')
```

### 2. 任务管理

```python
# 创建任务
wm.create_task("task_001", {
    'title': '任务标题',
    'priority': 1,
    'due_date': '2026-03-15'
})

# 完成任务
wm.complete_task("task_001")

# 获取待办
tasks = wm.get_pending_tasks()
```

### 3. 技能管理

```python
# 添加技能
wm.add_skill("python", {
    'level': 'expert',
    'description': 'Python 编程'
}, category='technical')

# 获取技能
skills = wm.get_skills()
```

### 4. 知识文档

```python
# 保存文档
wm.save_document(
    doc_id="doc_001",
    content="# 文档内容",
    category="technical"
)

# 搜索文档
results = wm.search_documents("Python")
```

### 5. 会议记录

```python
wm.save_meeting_note("meeting_001", {
    'title': '会议标题',
    'date': '2026-03-13',
    'attendees': ['张三', '李四'],
    'notes': '会议内容',
    'action_items': ['待办 1', '待办 2']
})
```

### 6. 工作日志

```python
wm.save_daily_log("2026-03-13", {
    'tasks_completed': ['任务 1', '任务 2'],
    'issues': ['问题 1'],
    'notes': '备注'
})
```

---

## 🏗️ 目录结构

```
work_memory/
├── projects/              # 项目管理
│   ├── active/           # 进行中
│   ├── completed/        # 已完成
│   └── archived/         # 已归档
├── tasks/                # 任务管理
├── skills/               # 技能成长
├── knowledge/            # 知识文档
├── contacts/             # 人际关系
├── meetings/             # 会议记录
├── logs/                 # 工作日志
├── backups/              # 备份
└── relationships/        # 关系索引
```

---

## 📊 使用示例

### 完整工作流

```python
from work_memory import WorkMemory

wm = WorkMemory()

# 1. 创建项目
wm.create_project("proj_new", {
    'name': '新客户项目',
    'priority': 'high'
})

# 2. 创建任务
wm.create_task("task_req", {
    'title': '需求分析',
    'priority': 1,
    'project_id': 'proj_new'
})

# 3. 保存会议记录
wm.save_meeting_note("meeting_kickoff", {
    'title': '项目启动会',
    'attendees': ['客户', '项目经理'],
    'action_items': ['完成需求文档']
})

# 4. 记录日报
wm.save_daily_log("2026-03-13", {
    'tasks_completed': ['项目启动会'],
    'notes': '新客户项目启动'
})

# 5. 查看统计
stats = wm.get_stats()
print(f"项目数：{stats['projects']['active']}")
print(f"任务数：{stats['tasks']['pending']}")
```

---

## 🔧 API 参考

### WorkMemory 类

#### 初始化

```python
wm = WorkMemory(root_dir: str = "~/work_memory")
```

#### 项目方法

| 方法 | 说明 |
|------|------|
| `create_project(project_id, data)` | 创建项目 |
| `get_project(project_id)` | 获取项目 |
| `update_project_status(project_id, status)` | 更新项目状态 |
| `list_projects(status)` | 列出项目 |

#### 任务方法

| 方法 | 说明 |
|------|------|
| `create_task(task_id, data)` | 创建任务 |
| `complete_task(task_id)` | 完成任务 |
| `get_pending_tasks(project_id)` | 获取待办任务 |

#### 技能方法

| 方法 | 说明 |
|------|------|
| `add_skill(name, data, category)` | 添加技能 |
| `get_skills(category)` | 获取技能列表 |

#### 文档方法

| 方法 | 说明 |
|------|------|
| `save_document(doc_id, content, category)` | 保存文档 |
| `search_documents(query, category)` | 搜索文档 |

#### 其他方法

| 方法 | 说明 |
|------|------|
| `add_contact(contact_id, data, category)` | 添加联系人 |
| `save_meeting_note(meeting_id, data)` | 保存会议记录 |
| `save_daily_log(date, data)` | 保存日报 |
| `backup(backup_path)` | 备份 |
| `restore(backup_path)` | 恢复 |
| `get_stats()` | 获取统计 |
| `print_tree(max_depth)` | 打印目录树 |

---

## 🧪 测试

```bash
# 运行测试
pytest tests/

# 带覆盖率
pytest --cov=work_memory tests/
```

---

## 📚 文档

完整文档请访问：[https://github.com/openclaw/work-memory/docs](https://github.com/openclaw/work-memory/docs)

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 开源协议

本项目采用 [MIT](LICENSE) 协议开源。

---

## 🙏 致谢

- 灵感来自 [memU](https://github.com/NevaMind-AI/memU) 的文件系统记忆设计
- OpenClaw 社区支持

---

## 📬 联系方式

- GitHub Issues: [提交问题](https://github.com/openclaw/work-memory/issues)
- 邮箱：support@openclaw.ai

---

<div align="center">

**Made with ❤️ for OpenClaw Community**

</div>
