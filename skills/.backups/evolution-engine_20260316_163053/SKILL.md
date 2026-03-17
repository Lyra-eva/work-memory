---
name: evolution-engine
description: 进化引擎 v2.0 - 热插拔 AI 进化系统
author: OpenClaw Community
version: 2.0.0
---

# Evolution Engine Skill

进化引擎 - AI 自主进化系统（热插拔版本）

## 🎯 特性

- ✅ **热插拔设计** - 可随时安装/卸载
- ✅ **独立运行** - 不依赖 OpenClaw 核心
- ✅ **可选启用** - 用户可选择是否启用
- ✅ **数据隔离** - 独立数据存储
- ✅ **OODA 循环** - 自主决策进化

## 📦 安装

### 方式 1: 一键安装

```bash
cd ~/.openclaw/workspace/skills/evolution-engine
./install.sh
```

### 方式 2: 手动安装

```bash
# 安装核心库
cd ~/.openclaw/workspace/evolution-engine-v2
pip3 install --user -e .

# 创建数据目录
mkdir -p ~/.openclaw/workspace/evolution-data/{events,capabilities,patterns,skills,backups}
```

## 🚀 使用

### 启用进化引擎

```python
from evolution_engine import EvolutionEngine

engine = EvolutionEngine()
engine.enable()
```

### 查看状态

```python
status = engine.get_status()
print(f"引擎状态：{'启用' if status['enabled'] else '禁用'}")
```

## 📊 与 OpenClaw 记忆的关系

| 功能 | OpenClaw 记忆 | 进化引擎 |
|------|-------------|---------|
| 对话记忆 | ✅ | ❌ |
| 用户偏好 | ✅ | ❌ |
| AI 进化 | ⚠️ 基础 | ✅ 专业 |
| 技能进化 | ⚠️ 基础 | ✅ 专业 |
| 模式挖掘 | ❌ | ✅ |

**互补关系，不是替代**

## 🔧 配置

在 `TOOLS.md` 中添加：

```markdown
### Evolution Engine

- 数据目录：`~/.openclaw/workspace/evolution-data/`
- 自动启用：true
- OODA 循环间隔：30 秒
```

## 🗑️ 卸载

```bash
cd ~/.openclaw/workspace/skills/evolution-engine
./uninstall.sh
```

---

**版本**: 2.0.0  
**发布**: 2026-03-14  
**状态**: ✅ 生产就绪
