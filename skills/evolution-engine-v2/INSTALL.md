# 📦 Evolution Engine v2 - 安装指南

## 快速安装（推荐）

### 一键安装

```bash
clawhub install evolution-engine-v2
```

安装过程会自动：
1. ✅ 下载技能到 `~/.openclaw/workspace/skills/evolution-engine-v2`
2. ✅ 创建数据目录 `~/.openclaw/workspace/memory/evolution`
3. ✅ 创建默认配置文件
4. ✅ 安装依赖 (tsx)

### 验证安装

```bash
cd ~/.openclaw/workspace/skills/evolution-engine-v2
npx tsx src/event-collector.ts stats
```

应显示：
```
📊 进化事件统计
总事件数：0
```

---

## 手动安装

### 步骤 1: 克隆仓库

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/openclaw/skill-evolution-engine-v2.git
cd evolution-engine-v2
```

### 步骤 2: 安装依赖

```bash
# 使用 npm
npm install

# 或使用 pnpm
pnpm install
```

### 步骤 3: 初始化配置

```bash
npx tsx src/openclaw-integration.ts init
```

这会创建：
- 数据目录：`~/.openclaw/workspace/memory/evolution`
- 配置文件：`~/.openclaw/workspace/evolution-config.json`

---

## 安装后配置

### 1. 启用自动进化

```bash
npx tsx src/openclaw-integration.ts enable
```

这会：
- ✅ 启用事件自动收集
- ✅ 设置每天凌晨 3 点自动反思
- ✅ 启用会话上下文注入

### 2. 测试功能

```bash
# 记录测试事件
npx tsx src/event-collector.ts collect --type success --data '{"task":"安装测试"}'

# 查看统计
npx tsx src/event-collector.ts stats

# 执行反思
npx tsx src/reflector.ts
```

---

## 系统要求

| 要求 | 版本 | 检查命令 |
|------|------|---------|
| **Node.js** | ≥18.0.0 | `node --version` |
| **npm** | ≥9.0.0 | `npm --version` |
| **OpenClaw** | ≥2026.3.0 | `openclaw --version` |
| **tsx** | 自动安装 | - |

### 检查 Node.js 版本

```bash
node --version
# 应显示：v18.x.x 或更高
```

如果版本过低，请升级：
```bash
# 使用 nvm
nvm install 20
nvm use 20

# 或直接下载
# https://nodejs.org/
```

---

## 目录结构

安装后的目录结构：

```
~/.openclaw/workspace/
├── skills/
│   └── evolution-engine-v2/
│       ├── src/                    # 源代码
│       │   ├── event-collector.ts
│       │   ├── reflector.ts
│       │   ├── context-injector.ts
│       │   └── openclaw-integration.ts
│       ├── SKILL.md                # 技能说明
│       ├── README.md               # 使用文档
│       ├── package.json            # 依赖配置
│       └── scripts/
│           └── post-install.ts     # 安装后脚本
│
└── memory/
    └── evolution/                  # 数据目录（自动创建）
        ├── events.jsonl            # 事件日志
        ├── patterns.json           # 模式数据
        └── index.json              # 索引
```

---

## 故障排除

### 问题 1: clawhub 命令不存在

**解决：**
```bash
npm install -g clawhub
```

### 问题 2: 权限错误

**解决：**
```bash
# 确保目录权限正确
chmod -R 755 ~/.openclaw/workspace/skills/evolution-engine-v2
```

### 问题 3: tsx 安装失败

**解决：**
```bash
# 手动安装 tsx
npm install -g tsx

# 然后重试
cd ~/.openclaw/workspace/skills/evolution-engine-v2
npm install
```

### 问题 4: 数据目录创建失败

**解决：**
```bash
# 手动创建
mkdir -p ~/.openclaw/workspace/memory/evolution

# 初始化配置
cd ~/.openclaw/workspace/skills/evolution-engine-v2
npx tsx src/openclaw-integration.ts init
```

### 问题 5: OpenClaw 版本过低

**解决：**
```bash
# 升级 OpenClaw
openclaw update

# 或重新安装
npm install -g openclaw@latest
```

---

## 卸载

```bash
# 1. 禁用自动进化
cd ~/.openclaw/workspace/skills/evolution-engine-v2
npx tsx src/openclaw-integration.ts disable

# 2. 删除技能
rm -rf ~/.openclaw/workspace/skills/evolution-engine-v2

# 3. 删除数据（可选）
rm -rf ~/.openclaw/workspace/memory/evolution
rm -f ~/.openclaw/workspace/evolution-config.json
```

---

## 从 v1.x 升级

如果之前使用过 Python 版本的 v1.x：

### 1. 备份数据（可选）

```bash
cp -r ~/.openclaw/workspace/evolution-data \
      ~/.openclaw/workspace/evolution-data.backup
```

### 2. 卸载旧版本

```bash
rm -rf ~/.openclaw/workspace/skills/evolution-engine
rm -rf ~/.openclaw/workspace/skills/evolution-engine-v1
```

### 3. 安装 v2.0

```bash
clawhub install evolution-engine-v2
```

### 4. 重新初始化

```bash
cd ~/.openclaw/workspace/skills/evolution-engine-v2
npx tsx src/openclaw-integration.ts init
npx tsx src/openclaw-integration.ts enable
```

---

## 帮助

遇到问题？

- **文档**: 查看 [README.md](README.md)
- **技能说明**: 查看 [SKILL.md](SKILL.md)
- **GitHub Issues**: https://github.com/openclaw/skill-evolution-engine-v2/issues
- **Discord**: https://discord.gg/clawd

---

**版本**: 2.0.0  
**最后更新**: 2026-03-17
