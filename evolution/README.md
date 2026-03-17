# 🧬 进化引擎 - 最小可行版本

让 AI 真正"变聪明"的简单系统。

## 核心理念

```
聪明 = 经验 + 反思 + 固化 + 复用
```

## 快速开始

### 1️⃣ 收集事件（每次对话后）

```bash
# 成功事件
tsx evolution/collect-event.ts success '{"task":"回答用户问题","duration_ms":1200}'

# 失败事件
tsx evolution/collect-event.ts failure '{"task":"浏览器自动化","error":"timeout"}'

# 经验教训
tsx evolution/collect-event.ts lesson '{"what":"用户纠正了我","learned":"需要确认时区"}'
```

### 2️⃣ 定期反思（每天/每周）

```bash
# 预演模式（先看效果）
tsx evolution/reflect.ts --dry-run

# 实际运行（更新 MEMORY.md）
tsx evolution/reflect.ts
```

### 3️⃣ 会话前注入上下文

```bash
# 生成 prompt 注入内容
tsx evolution/inject-context.ts
```

## 自动化设置

### 添加 cron 任务（每天凌晨 3 点反思）

```bash
crontab -e

# 添加这行：
0 3 * * * cd ~/.openclaw/workspace && tsx evolution/reflect.ts >> evolution/reflect.log 2>&1
```

### OpenClaw 会话后钩子

在 OpenClaw 的 agent 运行时中添加：

```typescript
// 会话结束后
afterSession(async (session) => {
  const eventType = session.success ? 'success' : 'failure';
  const data = JSON.stringify({
    task: session.task,
    duration_ms: session.duration,
    ...(session.error ? { error: session.error } : {}),
  });
  
  await exec(`tsx evolution/collect-event.ts ${eventType} '${data}'`);
});
```

## 事件类型说明

| 类型 | 用途 | 示例 |
|------|------|------|
| `success` | 记录成功 | 完成任务、用户满意 |
| `failure` | 记录失败 | 超时、错误、用户纠正 |
| `lesson` | 记录教训 | 学到的经验、规则更新 |
| `pattern` | 记录模式 | 发现的用户习惯、重复场景 |
| `capability` | 记录能力 | 新学会的技能、工具使用 |

## 数据流向

```
对话 → 收集事件 → events.jsonl
                   ↓
              定期反思
                   ↓
              patterns.json → MEMORY.md
                   ↓
              会话前注入 → prompt
```

## 文件结构

```
~/.openclaw/workspace/
├── evolution/
│   ├── collect-event.ts    # 事件收集器
│   ├── reflect.ts          # 反思引擎
│   ├── inject-context.ts   # 上下文注入
│   └── README.md           # 本文档
└── memory/
    └── evolution/
        ├── events.jsonl    # 原始事件日志
        ├── patterns.json   # 发现的模式
        └── index.json      # 事件索引
```

## 示例工作流

```bash
# 1. 完成一次成功的对话
tsx evolution/collect-event.ts success '{"task":"解答编程问题","user_feedback":"满意"}'

# 2. 遇到一个错误
tsx evolution/collect-event.ts failure '{"task":"执行 shell 命令","error":"权限不足"}'

# 3. 学到教训
tsx evolution/collect-event.ts lesson '{"what":"权限问题","learned":"先检查 elevated 权限"}'

# 4. 晚上反思
tsx evolution/reflect.ts

# 5. 明天会话前
tsx evolution/inject-context.ts
# → 输出内容添加到 system prompt
```

## 下一步优化

1. **自动收集** - 修改 OpenClaw 运行时，自动记录事件
2. **智能分析** - 用 AI 分析事件，提取更深层模式
3. **能力固化** - 将模式转化为具体技能/规则
4. **反馈闭环** - 用户点赞/纠正 → 自动学习

---

**版本**: 1.0.0  
**创建**: 2026-03-17  
**状态**: 🚀 可用
