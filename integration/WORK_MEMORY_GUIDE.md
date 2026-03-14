# 💼 工作记忆系统 (WorkMemory)

**版本**: 1.0.0  
**创建日期**: 2026-03-13  
**设计理念**: 借鉴 memU 文件系统架构，专为工作场景设计

---

## 📋 系统概览

### 核心特性

| 特性 | 说明 |
|------|------|
| **文件系统架构** | 类文件夹分层结构，直观易用 |
| **项目管理** | 全生命周期管理 (active/completed/archived) |
| **任务管理** | 待办/进行中/已完成状态流转 |
| **技能成长** | 技术/软技能/证书分类管理 |
| **知识文档** | 技术/业务/模板文档管理 |
| **人际关系** | 同事/客户/合作伙伴管理 |
| **会议记录** | 会议纪要 + 待办事项追踪 |
| **工作日志** | 日报/周报/月报自动归档 |

---

## 🏗️ 目录结构

```
work_memory/
├── projects/              # 项目管理
│   ├── active/           # 进行中项目
│   ├── completed/        # 已完成项目
│   └── archived/         # 已归档项目
│
├── tasks/                # 任务管理
│   ├── pending/          # 待办任务
│   ├── in_progress/      # 进行中任务
│   └── completed/        # 已完成任务
│
├── skills/               # 技能成长
│   ├── technical/        # 技术技能
│   ├── soft/             # 软技能
│   └── certifications/   # 证书资质
│
├── knowledge/            # 文档知识
│   ├── technical/        # 技术文档
│   ├── business/         # 业务知识
│   └── templates/        # 模板文档
│
├── contacts/             # 人际关系
│   ├── colleagues/       # 同事
│   ├── clients/          # 客户
│   └── partners/         # 合作伙伴
│
├── meetings/             # 会议记录
│   ├── notes/            # 会议笔记
│   └── action_items/     # 会议待办
│
├── logs/                 # 工作日志
│   ├── daily/            # 日报
│   ├── weekly/           # 周报
│   └── monthly/          # 月报
│
├── backups/              # 备份
└── relationships/        # 关系索引
```

---

## 🚀 快速开始

### 初始化

```python
from integration.work_memory import WorkMemory

# 创建工作记忆系统
wm = WorkMemory(root_dir="~/openclaw/workspace/work_memory")
```

---

## 📖 使用指南

### 1. 项目管理

#### 创建项目

```python
wm.create_project("proj_001", {
    'name': '进化引擎 5.0',
    'description': '下一代进化引擎',
    'start_date': '2026-03-01',
    'priority': 'high',
    'team': ['张三', '李四']
})
```

#### 更新项目状态

```python
# 项目完成
wm.update_project_status("proj_001", "completed")

# 项目归档
wm.update_project_status("proj_001", "archived")
```

#### 列出项目

```python
# 查看进行中项目
active_projects = wm.list_projects(status='active')

# 查看已完成项目
completed_projects = wm.list_projects(status='completed')
```

#### 获取项目详情

```python
project = wm.get_project("proj_001")
print(project['name'])  # 进化引擎 5.0
print(project['priority'])  # high
```

---

### 2. 任务管理

#### 创建任务

```python
wm.create_task("task_001", {
    'title': '实现图谱关系完善',
    'description': '建立 DERIVED_FROM/DEPENDS_ON 关系',
    'priority': 1,  # 1=最高优先级
    'due_date': '2026-03-15',
    'project_id': 'proj_001',
    'assignee': '张三'
})
```

#### 完成任务

```python
wm.complete_task("task_001")
```

#### 获取待办任务

```python
# 获取所有待办
pending_tasks = wm.get_pending_tasks()

# 按项目获取待办
proj_tasks = wm.get_pending_tasks(project_id='proj_001')
```

---

### 3. 技能管理

#### 添加技能

```python
# 技术技能
wm.add_skill("python_advanced", {
    'level': 'expert',
    'learned_at': '2026-03-01',
    'description': '高级 Python 编程',
    'resources': ['链接 1', '链接 2']
}, category='technical')

# 软技能
wm.add_skill("communication", {
    'level': 'intermediate',
    'description': '沟通技巧'
}, category='soft')

# 证书
wm.add_skill("aws_saa", {
    'name': 'AWS Solutions Architect Associate',
    'obtained_at': '2026-01-01',
    'expires_at': '2029-01-01'
}, category='certifications')
```

#### 获取技能列表

```python
# 获取所有技能
all_skills = wm.get_skills()

# 只获取技术技能
tech_skills = wm.get_skills(category='technical')
```

---

### 4. 知识文档

#### 保存文档

```python
wm.save_document(
    doc_id="python_tips",
    content="""# Python 技巧

## 列表推导式
```python
squares = [x**2 for x in range(10)]
```

## 装饰器
```python
@decorator
def func():
    pass
```
""",
    category="technical",
    metadata={
        'title': 'Python 技巧',
        'tags': 'python,tips,programming',
        'author': '张三'
    }
)
```

#### 搜索文档

```python
# 搜索技术文档
results = wm.search_documents("Python", category='technical')

for doc in results:
    print(f"文档 ID: {doc['id']}")
    print(f"分类：{doc['category']}")
    print(f"预览：{doc['preview']}")
```

---

### 5. 人际关系

#### 添加联系人

```python
# 同事
wm.add_contact("contact_001", {
    'name': '张三',
    'role': '技术经理',
    'company': '某某公司',
    'email': 'zhangsan@example.com',
    'phone': '138-0000-0000',
    'notes': '项目负责人'
}, category='colleagues')

# 客户
wm.add_contact("client_001", {
    'name': '李四',
    'role': '采购经理',
    'company': '客户公司',
    'email': 'lisi@client.com'
}, category='clients')
```

#### 获取联系人

```python
contact = wm.get_contact("contact_001")
print(contact['name'])  # 张三
print(contact['role'])  # 技术经理
```

---

### 6. 会议管理

#### 保存会议记录

```python
wm.save_meeting_note("meeting_001", {
    'title': '项目启动会',
    'date': '2026-03-13',
    'attendees': ['张三', '李四', '王五'],
    'notes': """
## 讨论内容

1. 项目范围确认
2. 时间表讨论
3. 资源分配

## 决议

- 采用敏捷开发模式
- 每周一次站会
""",
    'action_items': [
        '完成需求文档 - 张三 - 2026-03-15',
        '制定开发计划 - 李四 - 2026-03-17'
    ]
})
```

---

### 7. 工作日志

#### 保存日报

```python
wm.save_daily_log("2026-03-13", {
    'tasks_completed': [
        '实现工作记忆系统',
        '编写测试代码',
        '更新文档'
    ],
    'issues': [
        '无重大问题'
    ],
    'notes': '今天进展顺利，完成了预期目标',
    'mood': '😊'  # 可选：心情
})
```

#### 保存周报

```python
wm.save_daily_log("2026-W11", {  # 2026 年第 11 周
    'tasks_completed': [
        '完成进化引擎 4.0',
        '启动 5.0 规划'
    ],
    'issues': [
        'memU 集成遇到网络问题'
    ],
    'next_week_plan': [
        '继续 5.0 开发',
        '完善文档'
    ]
})
```

---

### 8. 交叉引用

#### 创建关联

```python
# 任务关联项目
wm.link_items("task_001", "proj_001", "belongs_to")

# 任务之间关联
wm.link_items("task_002", "task_001", "blocks")

# 文档关联技能
wm.link_items("python_tips", "python_advanced", "supports")
```

---

### 9. 备份恢复

#### 备份

```python
# 自动命名备份
backup_path = wm.backup()
# → work_memory/backups/work_memory_20260313_165557

# 自定义备份路径
wm.backup(backup_path="/path/to/backup")
```

#### 恢复

```python
wm.restore(backup_path="/path/to/backup")
```

---

### 10. 统计报告

#### 获取统计信息

```python
stats = wm.get_stats()

print(f"项目数：{stats['projects']['active']} 个进行中")
print(f"任务数：{stats['tasks']['pending']} 个待办")
print(f"技能数：{stats['skills']} 个")
print(f"文档数：{stats['documents']} 个")
print(f"联系人数：{stats['contacts']} 个")
print(f"总大小：{stats['total_size_kb']}KB")
```

#### 打印目录树

```python
wm.print_tree(max_depth=2)
```

**输出**:
```
📂 /home/admin/openclaw/workspace/work_memory
├── backups
├── contacts
│   ├── clients
│   ├── colleagues
│   └── partners
├── knowledge
│   ├── business
│   ├── technical
│   └── templates
├── logs
│   ├── daily
│   ├── monthly
│   └── weekly
├── meetings
│   ├── action_items
│   └── notes
├── projects
│   ├── active
│   ├── archived
│   └── completed
├── relationships
├── skills
│   ├── certifications
│   ├── soft
│   └── technical
└── tasks
    ├── completed
    ├── in_progress
    └── pending
```

---

## 💡 实际应用场景

### 场景 1: 新项目启动

```python
# 1. 创建项目
wm.create_project("proj_new", {
    'name': '新客户项目',
    'start_date': '2026-03-15',
    'priority': 'high'
})

# 2. 创建任务
wm.create_task("task_req", {
    'title': '需求分析',
    'priority': 1,
    'due_date': '2026-03-20',
    'project_id': 'proj_new'
})

# 3. 保存会议记录
wm.save_meeting_note("meeting_kickoff", {
    'title': '项目启动会',
    'date': '2026-03-15',
    'attendees': ['客户', '项目经理'],
    'notes': '...',
    'action_items': ['完成需求文档']
})

# 4. 记录日报
wm.save_daily_log("2026-03-15", {
    'tasks_completed': ['项目启动会'],
    'notes': '新客户项目启动'
})
```

---

### 场景 2: 技能成长追踪

```python
# 1. 记录学习的技能
wm.add_skill("kubernetes", {
    'level': 'beginner',
    'started_at': '2026-03-01',
    'resources': ['K8s 官方文档']
})

# 2. 保存学习笔记
wm.save_document(
    doc_id="k8s_notes",
    content="# Kubernetes 学习笔记\n\n## Pod 概念\n...",
    category="technical",
    metadata={'tags': 'k8s,devops'}
)

# 3. 关联技能和文档
wm.link_items("k8s_notes", "kubernetes", "supports")
```

---

### 场景 3: 客户关系管理

```python
# 1. 添加客户联系人
wm.add_contact("client_ceo", {
    'name': '王总',
    'role': 'CEO',
    'company': '重要客户',
    'email': 'wang@vip-client.com'
}, category='clients')

# 2. 记录客户会议
wm.save_meeting_note("meeting_client", {
    'title': '客户需求讨论',
    'attendees': ['王总', '我'],
    'notes': '客户对 X 功能感兴趣',
    'action_items': ['准备演示']
})

# 3. 关联客户和项目
wm.link_items("client_ceo", "proj_new", "interested_in")
```

---

## 📊 最佳实践

### 1. 项目命名规范

```python
# 推荐格式
proj_{domain}_{name}_{version}
# 示例
proj_evolution_engine_v5
proj_website_redesign
```

### 2. 任务优先级

```python
# 优先级定义
1 = 紧急且重要 (立即处理)
2 = 重要不紧急 (安排时间)
3 = 紧急不重要 (委托他人)
4 = 不紧急不重要 (最后处理)
```

### 3. 文档标签

```python
metadata={
    'tags': 'python,automation,script',  # 逗号分隔
    'author': '张三',
    'version': '1.0'
}
```

### 4. 定期备份

```python
# 每周五备份
import schedule

schedule.every().friday.at("18:00").do(lambda: wm.backup())
```

### 5. 定期清理

```python
# 每月归档已完成项目
for proj_id in wm.list_projects('completed'):
    project = wm.get_project(proj_id)
    if project['metadata']['updated_at'] < '2026-02-01':
        wm.update_project_status(proj_id, 'archived')
```

---

## 🔧 高级功能

### 自定义目录结构

```python
# 创建自定义目录
wm = WorkMemory(root_dir="~/work_memory")

# 添加自定义分类
os.makedirs(os.path.join(wm.root_dir, "projects", "research"))
os.makedirs(os.path.join(wm.root_dir, "knowledge", "ai_ml"))
```

### 批量操作

```python
# 批量完成任务
task_ids = ["task_001", "task_002", "task_003"]
for task_id in task_ids:
    wm.complete_task(task_id)
```

### 数据导出

```python
import json

# 导出所有项目
projects = {}
for status in ['active', 'completed', 'archived']:
    for proj_id in wm.list_projects(status):
        projects[proj_id] = wm.get_project(proj_id)

with open('projects_export.json', 'w') as f:
    json.dump(projects, f, indent=2, ensure_ascii=False)
```

---

## 📚 相关文档

1. [进化引擎功能回顾](FUNCTION_REVIEW.md)
2. [回滚报告](ROLLBACK_REPORT.md)
3. [memU 集成方案](MEMU_INTEGRATION_PLAN.md)

---

**文档完成！** 📋

工作记忆系统已就绪，专为工作场景设计！💼
