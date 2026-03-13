# Work Memory 部署指南

**版本**: 2.0.0  
**更新日期**: 2026-03-13

---

## 📦 安装方式

### 方式 1: 从 PyPI 安装 (推荐)

```bash
pip install work-memory
```

### 方式 2: 从 GitHub 安装

```bash
pip install git+https://github.com/openclaw/work-memory.git
```

### 方式 3: 本地安装

```bash
git clone https://github.com/openclaw/work-memory.git
cd work-memory
pip install -e .
```

---

## 🚀 快速开始

### 基础使用

```python
from work_memory import WorkMemory

# 初始化
wm = WorkMemory(root_dir="~/work_memory")

# 创建项目
wm.create_project("proj_001", {
    'name': '我的项目',
    'priority': 'high'
})

# 创建任务
wm.create_task("task_001", {
    'title': '我的任务',
    'priority': 1
})

# 查看统计
stats = wm.get_stats()
print(f"项目：{stats['projects']['active']}个")
```

---

## 🔄 记忆迁移

### 从旧版本迁移

```bash
# 从 v1.x 迁移到 v2.x
python3 -m scripts.migrate_memory \
  ~/old_work_memory \
  ~/work_memory \
  --type work_v1_to_v2
```

### 从默认记忆系统迁移

```bash
# 从 OpenClaw 默认记忆迁移
python3 -m scripts.migrate_memory \
  ~/openclaw/workspace/memory \
  ~/work_memory \
  --type default_to_work
```

### 迁移选项

| 选项 | 说明 |
|------|------|
| `--type auto` | 自动检测迁移类型 (默认) |
| `--type default_to_work` | 默认记忆 → 工作记忆 |
| `--type work_v1_to_v2` | 工作记忆 v1 → v2 |

---

## 📊 目录结构

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

## 🔧 配置选项

### 环境变量

```bash
# 设置记忆根目录
export WORK_MEMORY_ROOT="~/work_memory"

# Python 中使用
from work_memory import WorkMemory
import os
wm = WorkMemory(root_dir=os.getenv('WORK_MEMORY_ROOT'))
```

### 配置文件

```python
# config.py
MEMORY_CONFIG = {
    'root_dir': '~/work_memory',
    'backup_enabled': True,
    'auto_backup': True
}

wm = WorkMemory(**MEMORY_CONFIG)
```

---

## 📋 部署检查清单

### 部署前

- [ ] 确认 Python 版本 >= 3.6
- [ ] 安装依赖 `pip install work-memory`
- [ ] 准备记忆目录
- [ ] 备份旧数据 (如有)

### 部署后

- [ ] 验证安装 `python3 -c "from work_memory import WorkMemory"`
- [ ] 创建测试项目
- [ ] 验证备份功能
- [ ] 迁移旧数据 (如有需要)

---

## 🐛 故障排查

### 问题 1: 导入失败

```bash
# 错误：ModuleNotFoundError: No module named 'work_memory'

# 解决：
pip install work-memory
# 或
export PYTHONPATH=/path/to/work-memory:$PYTHONPATH
```

### 问题 2: 目录权限

```bash
# 错误：PermissionError

# 解决：
chmod -R 755 ~/work_memory
# 或
sudo chown -R $USER:$USER ~/work_memory
```

### 问题 3: 迁移失败

```bash
# 错误：迁移过程中断

# 解决：
# 1. 检查备份是否存在
ls ~/backup_*

# 2. 重新运行迁移
python3 -m scripts.migrate_memory source target --type auto
```

---

## 📚 API 参考

### WorkMemory 类

#### 初始化

```python
wm = WorkMemory(root_dir: str = "~/work_memory")
```

#### 核心方法

| 方法 | 说明 |
|------|------|
| `create_project(id, data)` | 创建项目 |
| `create_task(id, data)` | 创建任务 |
| `add_skill(name, data, category)` | 添加技能 |
| `save_document(id, content, category)` | 保存文档 |
| `add_contact(id, data, category)` | 添加联系人 |
| `save_meeting_note(id, data)` | 保存会议记录 |
| `save_daily_log(date, data)` | 保存日报 |
| `backup(path)` | 备份 |
| `restore(path)` | 恢复 |
| `get_stats()` | 获取统计 |

---

## 🎯 最佳实践

### 1. 定期备份

```python
# 每天备份
import schedule
schedule.every().day.at("02:00").do(lambda: wm.backup())
```

### 2. 分类管理

```python
# 按项目分类
wm.create_project("proj_web", {...})
wm.create_project("proj_mobile", {...})

# 按技能分类
wm.add_skill("python", {...}, category='technical')
wm.add_skill("communication", {...}, category='soft')
```

### 3. 版本控制

```bash
# 使用 git 管理记忆
cd ~/work_memory
git init
git add .
git commit -m "Initial memory"
```

---

## 📞 支持

- **文档**: https://github.com/openclaw/work-memory
- **Issues**: https://github.com/openclaw/work-memory/issues
- **邮箱**: support@openclaw.ai

---

**最后更新**: 2026-03-13
