# OpenClaw Workspace 架构文档

📅 版本：2026-03-16  
📊 状态：产品化重构完成

---

## 🏗️ 架构设计

### 开发与发布分离

```
┌─────────────────────────────────────────────────┐
│           OpenClaw Workspace                    │
├─────────────────────────────────────────────────┤
│                                                 │
│  src/              release/                     │
│  ┌────┐           ┌────────┐                   │
│  │开发 │           │ 发布   │                   │
│  │仓库 │           │ 仓库   │                   │
│  │    │           │        │                   │
│  │源码 │  ──────▶  │ 产品   │                   │
│  │开发 │  构建     │ 级     │                   │
│  │    │           │        │                   │
│  └────┘           └────────┘                   │
│       ╲              │                          │
│        ╲             ▼                          │
│         ╲       安装到系统                       │
│          ╲                                     │
│           ▼                                    │
│        运行时数据自动创建                        │
│        (work-memory-data/)                     │
│        (evolution-data/)                       │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 📁 目录结构

```
/home/admin/.openclaw/workspace/
│
├── 📂 src/                           # 【开发仓库】
│   ├── work-memory-v1/               # 工作记忆系统源码
│   ├── work-memory-project/          # 工作记忆项目开发
│   ├── work-memory-evolution/        # 工作记忆进化模块
│   ├── evolution-engine/             # 进化引擎源码
│   ├── evolution/                    # 进化模块
│   └── ...                           # 其他开发中项目
│
├── 📂 release/                       # 【发布仓库】⭐
│   ├── work-memory-release/          # ✅ 工作记忆发布包
│   │   ├── work_memory/              # Python 包
│   │   ├── skills/                   # OpenClaw 技能
│   │   ├── scripts/                  # 工具脚本
│   │   ├── docs/                     # 文档
│   │   ├── examples/                 # 示例
│   │   ├── setup.py                  # 安装脚本
│   │   ├── pyproject.toml            # 项目配置
│   │   ├── README.md                 # 文档
│   │   ├── LICENSE                   # 许可证
│   │   ├── VERSION                   # 版本号
│   │   └── CHANGELOG.md              # 变更日志
│   │
│   └── evolution-engine-release/     # ✅ 进化引擎发布包
│       ├── evolution_engine/         # Python 包
│       ├── skills/                   # OpenClaw 技能
│       ├── scripts/                  # 工具脚本
│       ├── examples/                 # 示例
│       ├── setup.py                  # 安装脚本
│       ├── README.md                 # 文档
│       ├── LICENSE                   # 许可证
│       └── VERSION                   # 版本号
│
├── 📂 skills/                        # 【OpenClaw 技能】
│   ├── work-memory/                  # 工作记忆技能
│   ├── evolution-engine/             # 进化引擎技能
│   ├── agent-browser/                # 浏览器自动化
│   ├── find-skills/                  # 技能发现
│   ├── github-skill/                 # GitHub 操作
│   ├── proactive-agent/              # 主动代理
│   ├── qq-email/                     # QQ 邮箱
│   ├── searxng/                      # 隐私搜索
│   ├── self-improving-agent/         # 自我改进
│   ├── skill-vetter/                 # 技能安全审查
│   └── stability/                    # 稳定性模块
│
├── 📂 运行时数据 (自动创建)
│   ├── work-memory-data/             # 工作记忆数据
│   │   ├── projects/                 # 项目
│   │   ├── tasks/                    # 任务
│   │   ├── skills/                   # 技能
│   │   ├── knowledge/                # 知识
│   │   ├── contacts/                 # 联系人
│   │   ├── meetings/                 # 会议
│   │   ├── logs/                     # 日志
│   │   └── backups/                  # 备份
│   │
│   └── evolution-data/               # 进化引擎数据
│       ├── events/                   # 事件
│       ├── capabilities/             # 能力
│       ├── patterns/                 # 模式
│       ├── skills/                   # 技能
│       ├── backups/                  # 备份
│       └── logs/                     # 日志
│
├── 📂 其他系统
│   ├── memory/                       # 认知记忆系统
│   ├── evacore-stability/            # Evacore 稳定性
│   ├── stability-system/             # 稳定性系统
│   └── lily/                         # Lily 项目
│
├── 📄 setup.sh                       # 【安装脚本】从 release 安装
├── 📄 README.md                      # 项目说明
├── 📄 ARCHITECTURE.md                # 架构文档（本文件）
├── 📄 .gitignore                     # Git 忽略规则
└── 📄 TOOLS.md                       # 工具配置
```

---

## 🔄 工作流程

### 1. 开发流程

```bash
# 在 src/ 目录进行开发
cd src/work-memory-project
# ... 编写代码、测试 ...

# 构建发布版本
cd ../../release/work-memory-release
# ... 更新发布内容 ...

# 推送到 GitHub
git add -A && git commit -m "feat: ..."
git push origin main
```

### 2. 安装流程

```bash
# 从 release/ 安装产品
cd /home/admin/.openclaw/workspace
./setup.sh

# 验证安装
python3 -c "from work_memory import WorkMemory; print('✅')"
```

### 3. 升级流程

```bash
# 更新发布仓库
cd release/work-memory-release
git pull origin main

# 重新安装
cd ../../
./setup.sh
```

---

## 📦 产品列表

### 工作记忆系统 (v1.0.0)

| 属性 | 值 |
|------|-----|
| **发布仓库** | `release/work-memory-release/` |
| **GitHub** | https://github.com/Lyra-eva/work-memory |
| **安装方式** | `pip install -e . --user` |
| **数据目录** | `work-memory-data/` (自动创建) |
| **状态** | ✅ 产品级 |

### 进化引擎系统 (v2.0.0)

| 属性 | 值 |
|------|-----|
| **发布仓库** | `release/evolution-engine-release/` |
| **GitHub** | https://github.com/Lyra-eva/evolution-engine |
| **安装方式** | `pip install -e . --user` |
| **数据目录** | `evolution-data/` (自动创建) |
| **状态** | ✅ 产品级 |

---

## 🎯 设计原则

### 1. 开发与发布分离

| 仓库 | 用途 | 质量要求 |
|------|------|---------|
| `src/` | 开发、测试、实验 | 可运行 |
| `release/` | 产品发布 | **产品级** ✅ |

**规则**: 
- ✅ 永远从 `release/` 安装
- ❌ 不从 `src/` 直接安装

### 2. 产品级质量标准

`release/` 目录必须满足：

- ✅ 可安装（`pip install -e .` 成功）
- ✅ 可使用（导入无错误）
- ✅ 文档完整（README, LICENSE, VERSION）
- ✅ 版本明确（VERSION 文件）
- ✅ 安装脚本（setup.py, pyproject.toml）

### 3. 数据自然分离

- 运行时数据由系统自动创建
- 数据目录不纳入 Git 管理
- 代码升级不影响数据

### 4. 单向依赖

```
src/ ──构建──▶ release/ ──安装──▶ 运行时数据
  (开发)          (产品)         (自动创建)
```

---

## 🔧 配置说明

### TOOLS.md

```markdown
### Work Memory

- **数据目录**: `work-memory-data/`
- **自动备份**: 每天 23:00

### Evolution Engine

- **数据目录**: `evolution-data/`
- **自动启用**: true
- **OODA 循环间隔**: 30 秒
```

### .gitignore

```gitignore
# 运行时数据
work-memory-data/
evolution-data/
*.db
*.log

# Python
__pycache__/
*.egg-info/
```

---

## 📊 状态总览

| 组件 | 开发仓库 | 发布仓库 | 安装状态 |
|------|---------|---------|---------|
| 工作记忆系统 | ✅ src/ | ✅ release/ | ✅ 已安装 |
| 进化引擎系统 | ✅ src/ | ✅ release/ | ✅ 已安装 |

---

## 🚀 快速开始

```bash
# 1. 安装产品
cd /home/admin/.openclaw/workspace
./setup.sh

# 2. 验证安装
python3 -c "from work_memory import WorkMemory; wm = WorkMemory(); print('✅')"
python3 -c "from evolution_engine import EvolutionEngine; e = EvolutionEngine(); print('✅')"

# 3. 开始使用
# ...
```

---

**架构版本**: 2026-03-16  
**维护者**: Lyra-eva
