---
name: evolution-engine-v2
description: "AI 自主进化系统 - 自动记录经验、反思模式、注入上下文，让 AI 持续变聪明。支持事件收集、智能反思、Prompt 注入、cron 自动化。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🧬",
        "requires": { "bins": ["tsx"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "tsx",
              "bins": ["tsx"],
              "label": "安装 tsx (npm)",
            },
          ],
        "homepage": "https://github.com/openclaw/skill-evolution-engine-v2",
      },
  }
---

# Evolution Engine v2 - AI 自主进化系统 🧬

让 AI 真正"变聪明"的完整解决方案。通过记录经验、反思模式、注入上下文，实现持续学习和改进。

## 何时使用

✅ **使用此技能：**
- 记录重要对话的成功/失败/教训事件
- 定期反思，发现行为模式和用户习惯
- 在会话开始时加载历史经验到 prompt
- 自动 cron 调度（每天凌晨反思）

❌ **不使用此技能：**
- 简单的笔记记录 → 使用 memory 技能
- 一次性任务执行 → 无需进化系统
- 不需要持续学习的场景

## 安装

### 方式 1: ClawHub 安装（推荐）

```bash
# 一键安装（自动初始化）
clawhub install evolution-engine-v2

# 安装后自动执行：
# 1. 创建数据目录 ~/.openclaw/workspace/memory/evolution
# 2. 创建默认配置文件
# 3. 安装依赖 (tsx)
```

### 方式 2: Git 安装

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/openclaw/skill-evolution-engine-v2.git
cd evolution-engine-v2

# 安装依赖
npm install  # 或 pnpm install

# 初始化配置
npx tsx src/openclaw-integration.ts init
```

### 安装后验证

```bash
# 检查安装
npx tsx src/event-collector.ts stats

# 应显示：
# 📊 进化事件统计
# 总事件数：0
```

## 快速开始

### 1. 初始化配置

```bash
cd ~/.openclaw/workspace/skills/evolution-engine-v2
npx tsx src/openclaw-integration.ts init
```

### 2. 启用自动进化

```bash
npx tsx src/openclaw-integration.ts enable
```

这会自动：
- 启用事件自动收集
- 设置每天凌晨 3 点自动反思
- 启用会话上下文注入

### 3. 记录事件

```bash
# 成功事件
npx tsx src/event-collector.ts collect --type success --data '{"task":"完成任务","duration_ms":1200}'

# 失败事件
npx tsx src/event-collector.ts collect --type failure --data '{"task":"浏览器自动化","error":"timeout"}'

# 经验教训
npx tsx src/event-collector.ts collect --type lesson --data '{"what":"用户纠正","learned":"需要确认时区"}'

# 用户纠正
npx tsx src/event-collector.ts collect --type correction --data '{"what":"错误信息","corrected":"正确信息"}'
```

### 4. 查看统计

```bash
npx tsx src/event-collector.ts stats
```

### 5. 执行反思

```bash
# 预演模式
npx tsx src/reflector.ts --dry-run

# 实际运行（更新 MEMORY.md）
npx tsx src/reflector.ts
```

### 6. 查看注入内容

```bash
npx tsx src/context-injector.ts
```

## 命令参考

### 事件收集器

```bash
# 收集事件
npx tsx src/event-collector.ts collect --type <类型> --data '<JSON>'

# 查看统计
npx tsx src/event-collector.ts stats

# 列出事件
npx tsx src/event-collector.ts list [--limit <数量>]
```

**事件类型：**
- `success` - 成功事件
- `failure` - 失败事件
- `lesson` - 经验教训
- `pattern` - 发现模式
- `capability` - 新能力
- `correction` - 用户纠正

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
# 初始化配置
npx tsx src/openclaw-integration.ts init

# 启用
npx tsx src/openclaw-integration.ts enable

# 禁用
npx tsx src/openclaw-integration.ts disable

# 查看状态
npx tsx src/openclaw-integration.ts status
```

## 配置

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

**配置项说明：**
- `enabled`: 是否启用进化引擎
- `autoCollect`: 会话结束后自动收集事件
- `autoReflect`: 反思频率 (`disabled` | `daily` | `weekly`)
- `reflectTime`: cron 表达式，反思时间
- `maxEvents`: 最大保留事件数
- `injectContext`: 会话开始时注入历史上下文

## 数据流

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

## 文件结构

```
~/.openclaw/workspace/
├── skills/
│   └── evolution-engine-v2/
│       ├── SKILL.md              # 技能说明
│       ├── package.json          # 依赖配置
│       ├── install.sh            # 安装脚本
│       ├── README.md             # 完整文档
│       └── src/
│           ├── event-collector.ts    # 事件收集器
│           ├── reflector.ts          # 反思引擎
│           ├── context-injector.ts   # 上下文注入
│           └── openclaw-integration.ts # OpenClaw 集成
└── memory/
    └── evolution/
        ├── events.jsonl          # 事件日志
        ├── patterns.json         # 发现的模式
        ├── index.json            # 事件索引
        └── evolution-config.json # 配置文件
```

## OpenClaw 集成

### 在运行时中集成

```typescript
import { onSessionStart, onSessionEnd, onUserCorrection } from './skills/evolution-engine-v2/src/openclaw-integration.js';

// 会话开始
beforeEachSession(async (session) => {
  const context = await onSessionStart(session.id, session.chatId);
  if (context) {
    systemPrompt += '\n\n' + context;
  }
});

// 会话结束
afterEachSession(async (session) => {
  await onSessionEnd(session.id, {
    success: session.success,
    task: session.task,
    input: session.input,
    output: session.output,
    error: session.error,
    duration_ms: session.duration,
  });
});

// 用户纠正
onUserMessage(async (message) => {
  if (message.isCorrection) {
    await onUserCorrection(message.sessionId, {
      what: message.correctionTopic,
      corrected: message.correctedValue,
      original: message.originalValue,
    });
  }
});
```

### 或在 openclaw.json 中配置

```json
{
  "skills": {
    "entries": {
      "evolution-engine-v2": {
        "enabled": true,
        "config": {
          "autoCollect": true,
          "autoReflect": "daily"
        }
      }
    }
  }
}
```

## 最佳实践

### 1. 事件记录要点

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

# 自动反思已设置（每天凌晨 3 点）
# 查看 crontab: crontab -l
```

### 3. 查看进化进度

```bash
# 查看事件统计
npx tsx src/event-collector.ts stats

# 查看注入内容
npx tsx src/context-injector.ts

# 查看 MEMORY.md 中的进化部分
cat ~/.openclaw/workspace/MEMORY.md | grep -A 50 "🧬 进化引擎"
```

## 故障排除

### 问题：事件没有自动收集

**解决：**
1. 检查配置：`npx tsx src/openclaw-integration.ts status`
2. 确认已启用：`npx tsx src/openclaw-integration.ts enable`
3. 检查 OpenClaw 是否正确调用钩子

### 问题：反思没有更新 MEMORY.md

**解决：**
1. 手动运行：`npx tsx src/reflector.ts`
2. 检查文件权限：`ls -la ~/.openclaw/workspace/MEMORY.md`
3. 查看日志：`cat ~/.openclaw/workspace/memory/evolution/reflect.log`

### 问题：cron 任务没有执行

**解决：**
1. 检查 crontab：`crontab -l`
2. 重新启用：`npx tsx src/openclaw-integration.ts disable && enable`
3. 检查 cron 服务：`systemctl status cron`

## 预期效果

| 时间 | 预期效果 |
|------|---------|
| **第 1 周** | 积累 20-50 个事件，发现初步模式 |
| **第 2 周** | MEMORY.md 包含丰富进化内容，AI 回答更准确 |
| **第 1 月** | 形成稳定的成功/失败模式，重复错误减少 50%+ |
| **第 3 月** | AI 明显"变聪明"，主动预测用户需求 |

## 相关链接

- **完整文档**: [README.md](https://github.com/openclaw/skill-evolution-engine-v2/blob/main/README.md)
- **部署报告**: [DEPLOYMENT.md](https://github.com/openclaw/skill-evolution-engine-v2/blob/main/DEPLOYMENT.md)
- **ClawHub**: https://clawhub.com/skills/evolution-engine-v2
- **问题反馈**: https://github.com/openclaw/skill-evolution-engine-v2/issues

---

**版本**: 2.0.0  
**作者**: OpenClaw Community  
**许可**: MIT  
**状态**: 🚀 生产就绪
