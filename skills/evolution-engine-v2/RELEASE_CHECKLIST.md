# 📋 发布检查清单

## 发布前检查

### 代码质量
- [ ] 所有 TypeScript 文件通过编译检查
- [ ] 运行所有测试并通过
- [ ] 代码格式化（Prettier/ESLint）
- [ ] 无 console.log 调试语句
- [ ] 错误处理完善

### 文档完整性
- [ ] SKILL.md 包含完整使用说明
- [ ] README.md 更新到最新版本
- [ ] CHANGELOG.md 记录所有变更
- [ ] DEPLOYMENT.md 包含验证结果
- [ ] 版本号在所有文件中一致

### 功能验证
- [ ] 事件收集器工作正常
- [ ] 反思引擎能生成模式
- [ ] 上下文注入能生成 prompt
- [ ] cron 调度已设置
- [ ] MEMORY.md 能自动更新

### 配置检查
- [ ] package.json 版本号正确
- [ ] dependencies 完整
- [ ] scripts 定义正确
- [ ] repository URL 正确
- [ ] license 文件存在

## 发布步骤

### 1. 本地准备

```bash
cd ~/.openclaw/workspace/skills/evolution-engine-v2

# 运行测试
npm run test

# 检查文档
cat SKILL.md | head -20
cat README.md | head -20
```

### 2. 更新版本号

```bash
# 编辑以下文件的版本号
# - package.json
# - SKILL.md
# - README.md
# - CHANGELOG.md (添加新版本条目)
```

或使用发布脚本：

```bash
./publish.sh -v 2.0.0
```

### 3. Git 提交和标签

```bash
git add -A
git commit -m "Release v2.0.0"
git tag -a "v2.0.0" -m "Release v2.0.0"
git push origin main
git push origin v2.0.0
```

### 4. 发布到 ClawHub

```bash
# 登录（首次）
clawhub login

# 发布
clawhub publish . \
  --slug evolution-engine-v2 \
  --name "Evolution Engine v2" \
  --version 2.0.0 \
  --changelog "完整功能版本 - 事件收集、反思引擎、上下文注入" \
  --category automation \
  --tags ai,evolution,learning,memory,reflection
```

### 5. 创建 GitHub Release

1. 访问：https://github.com/openclaw/skill-evolution-engine-v2/releases/new
2. 标签：`v2.0.0`
3. 标题：`Evolution Engine v2 2.0.0`
4. 描述：从 CHANGELOG.md 复制
5. 点击 "Publish release"

### 6. 验证发布

```bash
# 测试全新安装
clawhub install evolution-engine-v2

# 验证安装
ls -la ~/.openclaw/workspace/skills/evolution-engine-v2/

# 测试功能
cd ~/.openclaw/workspace/skills/evolution-engine-v2
npx tsx src/event-collector.ts stats
```

## 发布后检查

### ClawHub 验证
- [ ] 技能在 ClawHub 上可见
- [ ] 版本号正确
- [ ] 描述和标签正确
- [ ] 安装说明完整

### GitHub 验证
- [ ] Release 已创建
- [ ] 标签已推送
- [ ] Release notes 完整
- [ ] 关联的 Issue 已关闭

### 功能验证
- [ ] 新安装能正常工作
- [ ] 所有命令可执行
- [ ] 文档链接有效
- [ ] 无破坏性变更

## 版本发布频率

### 主要版本 (X.0.0)
- 包含破坏性变更
- 重大功能更新
- 每季度发布一次

### 次要版本 (x.Y.0)
- 新功能（向后兼容）
- 重大改进
- 每月发布一次

### 补丁版本 (x.y.Z)
- Bug 修复
- 小改进
- 随时发布

## 紧急修复流程

### Hotfix 发布

```bash
# 1. 创建 hotfix 分支
git checkout -b hotfix/issue-123

# 2. 修复问题
# ... 修改代码 ...

# 3. 测试修复
npm run test

# 4. 发布补丁版本
./publish.sh -v 2.0.1

# 5. 合并回 main
git checkout main
git merge hotfix/issue-123
```

## 常见问题

### Q: 发布失败怎么办？

A: 检查以下几点：
1. 网络连接正常
2. ClawHub 登录状态：`clawhub whoami`
3. 版本号未重复
4. 所有必需文件存在

### Q: 如何撤销发布？

A: 
```bash
# 删除 ClawHub 版本
clawhub unpublish evolution-engine-v2 --version 2.0.0

# 删除 Git 标签
git tag -d v2.0.0
git push origin :refs/tags/v2.0.0

# 重置提交
git reset --hard HEAD~1
```

### Q: 版本号规则？

A: 遵循语义化版本（SemVer）：
- MAJOR.MINOR.PATCH
- 破坏性变更 → MAJOR++
- 新功能（向后兼容）→ MINOR++
- Bug 修复 → PATCH++

---

**最后更新**: 2026-03-17  
**版本**: 2.0.0
