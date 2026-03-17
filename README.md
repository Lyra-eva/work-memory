# OpenClaw Workspace

🧠 开放智能体工作空间 - 集成工作记忆与进化引擎

---

## 🏗️ 架构设计

```
workspace/
├── src/                    # 【开发仓库】源代码开发
│   ├── work-memory-v1/     # 工作记忆系统源码
│   ├── work-memory-project/
│   ├── evolution-engine/   # 进化引擎源码
│   └── ...
│
├── release/                # 【发布仓库】产品化版本
│   ├── work-memory-release/    # ✅ 工作记忆发布包
│   └── evolution-engine-release/ # ✅ 进化引擎发布包
│
├── skills/                 # 【OpenClaw 技能】
│   ├── work-memory/
│   ├── evolution-engine/
│   └── ...
│
├── work-memory-data/       # 【运行时数据】由系统自动创建
├── evolution-data/         # 【运行时数据】由系统自动创建
├── memory/                 # 【认知记忆】
└── setup.sh                # 【安装脚本】从 release 安装
```

---

## 🚀 快速开始

### 1. 安装产品

```bash
cd /home/admin/.openclaw/workspace
./setup.sh
```

这会从 `release/` 目录安装：
- ✅ 工作记忆系统 (work-memory)
- ✅ 进化引擎系统 (evolution-engine)

### 2. 验证安装

```bash
# 工作记忆
python3 -c "from work_memory import WorkMemory; wm = WorkMemory(); print('✅')"

# 进化引擎
python3 -c "from evolution_engine import EvolutionEngine; e = EvolutionEngine(); print('✅')"
```

---

## 📦 产品列表

### 工作记忆系统 (v1.0.0)

**功能**: 项目、任务、技能、知识、会议记录管理

```python
from work_memory import WorkMemory

wm = WorkMemory()
wm.create_session("project_x", {"name": "项目 X"})
```

**发布仓库**: `release/work-memory-release/`  
**GitHub**: https://github.com/Lyra-eva/work-memory

### 进化引擎系统 (v2.0.0)

**功能**: AI 自主进化、OODA 循环、技能进化、模式挖掘

```python
from evolution_engine import EvolutionEngine

engine = EvolutionEngine()
engine.enable()
```

**发布仓库**: `release/evolution-engine-release/`  
**GitHub**: https://github.com/Lyra-eva/evolution-engine

---

## 🛠️ 开发流程

### 开发新产品

```bash
# 1. 在 src/ 目录开发
cd src/work-memory-project
# ... 开发 ...

# 2. 构建发布包
cd ../../release/work-memory-release
# ... 更新发布内容 ...

# 3. 推送到 GitHub
git add -A && git commit -m "feat: ..."
git push origin main
```

### 测试安装

```bash
# 从 release 安装测试
cd /home/admin/.openclaw/workspace
./setup.sh
```

---

## 📁 目录说明

| 目录 | 用途 | 是否 Git 仓库 |
|------|------|-------------|
| `src/` | 源代码开发 | ✅ 是 |
| `release/` | 产品发布 | ✅ 是 (独立) |
| `skills/` | OpenClaw 技能 | ⚠️ 部分 |
| `work-memory-data/` | 工作记忆数据 | ❌ 否 |
| `evolution-data/` | 进化引擎数据 | ❌ 否 |
| `memory/` | 认知记忆 | ❌ 否 |

---

## 🎯 设计原则

1. **开发与发布分离**: `src/` 开发，`release/` 发布
2. **产品级质量**: `release/` 必须是可安装、可使用的产品
3. **从发布安装**: 永远从 `release/` 安装，不使用 `src/`
4. **数据自然分离**: 运行时数据由系统自动创建和管理

---

## 📄 许可证

MIT License

---

**版本**: 2026-03-16  
**作者**: Lyra-eva  
**GitHub**: https://github.com/Lyra-eva
