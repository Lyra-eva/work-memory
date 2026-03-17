# 🧬 Evolution Engine v2 - AI 自主进化系统

[![ClawHub](https://img.shields.io/badge/ClawHub-evolution--engine--v2-blue)](https://clawhub.com/skills/evolution-engine-v2)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node Version](https://img.shields.io/badge/node-%3E%3D18-green.svg)](https://nodejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](https://www.typescriptlang.org/)

让 AI 真正"变聪明"的完整解决方案。通过记录经验、反思模式、注入上下文，实现持续学习和改进。

## ✨ 特性

| 特性 | 说明 |
|------|------|
| **自动事件收集** | 会话结束后自动记录成功/失败/教训 |
| **AI 驱动反思** | 使用 AI 分析事件，提取深层模式 |
| **Prompt 注入** | 会话开始时自动加载历史经验 |
| **能力固化** | 将教训转化为可复用规则 |
| **用户习惯识别** | 自动发现用户活跃时间、偏好 |
| **cron 自动化** | 定时反思，无需手动触发 |
| **OpenClaw 原生** | TypeScript 实现，无缝集成 |

## 🚀 快速开始

### 1. 安装

```bash
# 方式 1: ClawHub 安装（推荐）
clawhub install evolution-engine-v2

# 方式 2: Git 克隆
cd ~/.openclaw/workspace/skills
git clone https://github.com/openclaw/skill-evolution-engine-v2.git
```

### 2. 初始化

```bash
cd ~/.openclaw/workspace/skills/evolution-engine-v2
npx tsx src/openclaw-integration.ts init
npx tsx src/openclaw-integration.ts enable
```

### 3. 开始使用

```bash
# 记录事件
npx tsx src/event-collector.ts collect --type success --data '{"task":"完成任务"}'

# 查看统计
npx tsx src/event-collector.ts stats

# 执行反思
npx tsx src/reflector.ts
```

## 📖 文档

- **[SKILL.md](SKILL.md)** - OpenClaw 技能说明和使用指南
- **[README.md](README.md)** - 本文档，完整使用说明
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - 部署报告和验证结果
- **[CHANGELOG.md](CHANGELOG.md)** - 版本更新日志

## 🎯 核心功能

### 事件收集

```bash
# 成功事件
npx tsx src/event-collector.ts collect --type success --data '{"task":"代码审查","feedback":"用户满意"}'

# 失败事件
npx tsx src/event-collector.ts collect --type failure --data '{"task":"浏览器","error":"timeout"}'

# 经验教训
npx tsx src/event-collector.ts collect --type lesson --data '{"what":"复杂问题","learned":"需要分步骤解释"}'

# 用户纠正
npx tsx src/event-collector.ts collect --type correction --data '{"what":"时区错误","corrected":"Asia/Shanghai"}'
```

### 反思引擎

```bash
# 预演模式
npx tsx src/reflector.ts --dry-run

# 实际运行
npx tsx src/reflector.ts
```

反思会自动：
- 分析事件模式（成功/失败/习惯）
- 生成改进建议
- 更新 MEMORY.md
- 保存模式到 patterns.json

### 上下文注入

```bash
npx tsx src/context-injector.ts
```

生成 prompt 注入内容，包含：
- 已验证的成功方法
- 需要避免的错误
- 积累的经验教训
- 用户习惯模式

## 📊 数据流

```
会话开始 → 加载历史模式 → 注入到 prompt
                          ↓
                    会话进行
                          ↓
会话结束 → 自动收集事件 → events.jsonl
                          ↓
                    定期反思 (cron)
                          ↓
                    patterns.json → MEMORY.md
```

## ⚙️ 配置

配置文件：`~/.openclaw/workspace/evolution-config.json`

```json
{
  "enabled": true,
  "autoCollect": true,
  "autoReflect": "daily",
  "reflectTime": "0 3 * * *",
  "maxEvents": 10000,
  "injectContext": true
}
```

## 🔧 命令参考

### 事件收集器

```bash
# 收集事件
npx tsx src/event-collector.ts collect --type <类型> --data '<JSON>'

# 查看统计
npx tsx src/event-collector.ts stats

# 列出事件
npx tsx src/event-collector.ts list --limit 10
```

### 反思引擎

```bash
# 执行反思
npx tsx src/reflector.ts [--dry-run]
```

### 上下文注入

```bash
# 查看注入内容
npx tsx src/context-injector.ts [--json]
```

### 集成管理

```bash
# 初始化
npx tsx src/openclaw-integration.ts init

# 启用
npx tsx src/openclaw-integration.ts enable

# 禁用
npx tsx src/openclaw-integration.ts disable

# 状态
npx tsx src/openclaw-integration.ts status
```

## 🏗️ 架构

```
src/
├── event-collector.ts      # 事件收集器 (~320 行)
├── reflector.ts            # 反思引擎 (~380 行)
├── context-injector.ts     # 上下文注入 (~180 行)
└── openclaw-integration.ts # OpenClaw 集成 (~380 行)

总计：~1,260 行 TypeScript
```

## 📦 文件结构

```
evolution-engine-v2/
├── src/                      # 源代码
│   ├── event-collector.ts
│   ├── reflector.ts
│   ├── context-injector.ts
│   └── openclaw-integration.ts
├── SKILL.md                  # OpenClaw 技能说明
├── README.md                 # 本文档
├── DEPLOYMENT.md             # 部署报告
├── CHANGELOG.md              # 更新日志
├── package.json              # 依赖配置
├── install.sh                # 安装脚本
├── .gitignore
└── .github/
    └── workflows/
        └── publish.yml       # ClawHub 发布工作流
```

## 🎓 最佳实践

### 1. 事件记录

```bash
# ✅ 好的记录 - 包含具体信息
npx tsx src/event-collector.ts collect --type success --data '{"task":"代码审查","feedback":"用户满意","duration_ms":2500}'

# ❌ 差的记录 - 信息不足
npx tsx src/event-collector.ts collect --type success --data '{"task":"xxx"}'
```

### 2. 定期反思

```bash
# 手动反思（建议每周一次）
npx tsx src/reflector.ts

# 自动反思（已设置，每天凌晨 3 点）
# crontab -l 查看
```

### 3. 查看进度

```bash
# 事件统计
npx tsx src/event-collector.ts stats

# 注入内容
npx tsx src/context-injector.ts

# MEMORY.md 进化部分
cat ~/.openclaw/workspace/MEMORY.md | grep -A 50 "🧬 进化引擎"
```

## 📈 预期效果

| 时间 | 预期效果 |
|------|---------|
| **第 1 周** | 积累 20-50 个事件，发现初步模式 |
| **第 2 周** | MEMORY.md 包含丰富进化内容，AI 回答更准确 |
| **第 1 月** | 形成稳定的成功/失败模式，重复错误减少 50%+ |
| **第 3 月** | AI 明显"变聪明"，主动预测用户需求 |

## 🔍 故障排除

### 事件没有自动收集

```bash
# 检查配置
npx tsx src/openclaw-integration.ts status

# 重新启用
npx tsx src/openclaw-integration.ts enable
```

### 反思没有更新 MEMORY.md

```bash
# 手动运行
npx tsx src/reflector.ts

# 检查日志
cat ~/.openclaw/workspace/memory/evolution/reflect.log
```

### cron 任务没有执行

```bash
# 检查 crontab
crontab -l

# 重新设置
npx tsx src/openclaw-integration.ts disable
npx tsx src/openclaw-integration.ts enable
```

## 🤝 贡献

欢迎贡献！请查看：

1. [GitHub Issues](https://github.com/openclaw/skill-evolution-engine-v2/issues) - 报告问题或提出建议
2. [ClawHub](https://clawhub.com/skills/evolution-engine-v2) - 查看和分享技能

## 📄 许可

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🔗 链接

- **ClawHub**: https://clawhub.com/skills/evolution-engine-v2
- **GitHub**: https://github.com/openclaw/skill-evolution-engine-v2
- **OpenClaw**: https://openclaw.ai
- **文档**: https://docs.openclaw.ai

---

**版本**: 2.0.0  
**创建**: 2026-03-17  
**状态**: 🚀 生产就绪  
**维护者**: OpenClaw Community
