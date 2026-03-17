# 📦 GitHub Release 发布指南

## 当前状态

**版本**: 2.0.0  
**Git 提交**: `57d7e2d`  
**Git 标签**: `v2.0.0` ✅ 已创建  
**状态**: ⏳ 等待 GitHub 仓库创建  

---

## 🎯 发布步骤

### 方案 1: 手动创建 GitHub Release（推荐）

#### 步骤 1: 创建 GitHub 仓库

1. 访问：https://github.com/new
2. 仓库名：`skill-evolution-engine-v2`
3. 描述：`Evolution Engine v2 - AI 自主进化系统`
4. 可见性：Public
5. 点击 "Create repository"

#### 步骤 2: 推送代码到 GitHub

```bash
cd ~/.openclaw/workspace/skills/evolution-engine-v2

# 添加远程仓库（替换为你的 GitHub 用户名）
git remote set-url origin https://github.com/YOUR_USERNAME/skill-evolution-engine-v2.git

# 推送代码
git push -u origin master

# 推送标签
git push origin v2.0.0
```

#### 步骤 3: 创建 GitHub Release

1. 访问：https://github.com/YOUR_USERNAME/skill-evolution-engine-v2/releases/new
2. 标签选择：`v2.0.0`
3. 标题：`Evolution Engine v2 2.0.0`
4. 描述：复制下面的 Release Notes
5. 点击 "Publish release"

---

## 📝 Release Notes 模板

```markdown
## 🧬 Evolution Engine v2 2.0.0

让 AI 真正"变聪明"的完整解决方案。通过记录经验、反思模式、注入上下文，实现持续学习和改进。

### ✨ 新特性

- **事件收集器** - 自动记录成功/失败/教训事件
- **反思引擎** - AI 驱动的模式分析和建议生成
- **上下文注入** - 会话开始时自动加载历史经验
- **OpenClaw 原生集成** - TypeScript 实现，无缝集成
- **cron 自动化** - 每天凌晨 3 点自动反思

### 📦 安装

#### 方式 1: 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/skill-evolution-engine-v2.git
cd skill-evolution-engine-v2
npm install  # 或 pnpm install
npx tsx src/openclaw-integration.ts init
```

#### 方式 2: 直接下载

下载最新 Release 并解压到 `~/.openclaw/workspace/skills/evolution-engine-v2`

### 🚀 快速开始

```bash
cd ~/.openclaw/workspace/skills/evolution-engine-v2

# 启用自动进化
npx tsx src/openclaw-integration.ts enable

# 记录事件
npx tsx src/event-collector.ts collect --type success --data '{"task":"测试"}'

# 查看统计
npx tsx src/event-collector.ts stats

# 执行反思
npx tsx src/reflector.ts
```

### 📚 文档

- **SKILL.md** - OpenClaw 技能说明
- **README.md** - 完整使用文档
- **INSTALL.md** - 安装指南
- **CHANGELOG.md** - 版本更新日志

### 🔧 技术栈

- **TypeScript** (~1,260 行代码)
- **Node.js** ≥18.0.0
- **OpenClaw** ≥2026.3.0
- **tsx** (自动安装)

### 📊 核心功能

1. **事件收集** - 支持 success, failure, lesson, correction 等类型
2. **模式识别** - 自动发现成功模式、失败模式、用户习惯
3. **反思引擎** - 定期分析事件，生成改进建议
4. **上下文注入** - 会话开始加载历史经验到 prompt
5. **自动调度** - cron 定时任务，无需手动触发

### 🎯 预期效果

- **第 1 周**: 积累 20-50 个事件，发现初步模式
- **第 2 周**: MEMORY.md 包含丰富进化内容，AI 回答更准确
- **第 1 月**: 形成稳定的成功/失败模式，重复错误减少 50%+
- **第 3 月**: AI 明显"变聪明"，主动预测用户需求

### 🐛 已知问题

无

### 📦 发布包内容

```
evolution-engine-v2/
├── src/                          # 源代码
│   ├── event-collector.ts
│   ├── reflector.ts
│   ├── context-injector.ts
│   └── openclaw-integration.ts
├── scripts/                      # 安装脚本
│   ├── post-install.ts
│   └── post-install.sh
├── SKILL.md                      # OpenClaw 技能说明
├── README.md                     # 使用文档
├── INSTALL.md                    # 安装指南
├── CHANGELOG.md                  # 更新日志
├── package.json                  # NPM 配置
└── ...                           # 其他文档和配置
```

### 📄 许可

MIT License

### 🔗 链接

- **GitHub**: https://github.com/YOUR_USERNAME/skill-evolution-engine-v2
- **Issues**: https://github.com/YOUR_USERNAME/skill-evolution-engine-v2/issues
- **Discord**: https://discord.gg/clawd

---

**Full Changelog**: https://github.com/YOUR_USERNAME/skill-evolution-engine-v2/compare/v1.0.0...v2.0.0
```

---

## 🔧 自动化脚本（可选）

### 使用 GitHub CLI

如果安装了 `gh` 命令行工具：

```bash
cd ~/.openclaw/workspace/skills/evolution-engine-v2

# 创建 Release
gh release create v2.0.0 \
  --title "Evolution Engine v2 2.0.0" \
  --notes-file - \
  --generate-notes \
  --verify-tag
```

### 使用发布脚本

```bash
# 编辑 publish.sh，添加 GitHub Release 创建
# 然后执行：
./publish.sh -v 2.0.0
```

---

## ✅ 验证清单

### 推送后验证

- [ ] 代码已推送到 GitHub
- [ ] 标签已推送
- [ ] GitHub 仓库可见
- [ ] 文件完整（15 个文件）

### Release 创建后验证

- [ ] Release 页面可见
- [ ] 标签正确（v2.0.0）
- [ ] Release notes 完整
- [ ] 关联的提交正确

---

## 📞 需要帮助？

### 常见问题

**Q: 推送失败 "repository not found"**
A: 确保先创建 GitHub 仓库，并正确设置远程 URL

**Q: 权限错误**
A: 使用正确的 GitHub 用户名，或配置 SSH key

**Q: 标签不存在**
A: 运行 `git tag -a "v2.0.0" -m "Release v2.0.0"` 创建标签

---

## 🎉 完成

发布成功后：

1. 分享 GitHub 仓库链接
2. 更新文档中的 GitHub URL
3. 通知用户可以使用

```bash
git clone https://github.com/YOUR_USERNAME/skill-evolution-engine-v2.git
```

---

**最后更新**: 2026-03-17  
**版本**: 2.0.0
