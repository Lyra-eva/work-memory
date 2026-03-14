# Work Memory 快速开始指南

## 🚀 30 秒快速开始

### 步骤 1: 安装（10 秒）

```bash
# 只需这一个命令！
clawhub install work-memory
```

**说明**：
- ✅ 自动下载技能
- ✅ 自动安装核心库
- ✅ 自动配置完成

---

### 步骤 2: 使用（20 秒）

```
/wm project create "我的第一个项目"
/wm task add "第一个任务"
/wm stats
```

**完成！🎉**

---

## 📋 常用命令

### 项目管理

```bash
# 创建项目
/wm project create "项目名称"

# 列出项目
/wm project list

# 完成项目
/wm project complete proj_xxx
```

### 任务管理

```bash
# 添加任务
/wm task add "任务标题"

# 列出任务
/wm task list

# 完成任务
/wm task complete task_xxx
```

### 工作日志

```bash
# 写日报
/wm log daily --tasks "任务 1,任务 2" --notes "今天进展顺利"
```

### 查看统计

```bash
# 查看统计
/wm stats
```

---

## 💡 进阶使用

### Python API

```python
from work_memory import WorkMemory

wm = WorkMemory()
wm.create_project("proj_001", {'name': '项目名称'})
wm.create_task("task_001", {'title': '任务标题'})
```

### 查看帮助

```bash
# 查看技能文档
cat ~/.openclaw/workspace/skills/work-memory/README.md
```

---

## ❓ 遇到问题？

### 问题 1: 命令不存在

**解决**：
```bash
# 重新安装
clawhub install work-memory

# 重启 OpenClaw
```

### 问题 2: 核心库未安装

**解决**：
```bash
# 手动安装核心库
pip install work-memory
```

### 问题 3: 其他问题

**查看文档**：
```bash
cat ~/.openclaw/workspace/skills/work-memory/README.md
```

---

## 🎯 下一步

- 📖 阅读完整文档：`README.md`
- 🏗️ 了解架构：`ARCHITECTURE.md`
- 💻 查看示例：`example_usage.py`

---

**Happy Coding! 🚀**
