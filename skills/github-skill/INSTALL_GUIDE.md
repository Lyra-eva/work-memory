# GitHub Skill 安装指南

**安装时间**: 2026-03-12  
**状态**: ✅ 已安装

---

## 📦 安装位置

**技能目录**: `/home/admin/.openclaw/workspace/skills/github-skill/`

**文件结构**:
```
github-skill/
├── SKILL.md                 # 技能说明
├── README.md                # 使用指南
├── INSTALL_GUIDE.md         # 安装指南
├── test_github.py           # 测试脚本
└── .env.example             # 配置模板
```

---

## ✅ 安装状态

| 组件 | 状态 |
|------|------|
| Git | ✅ 已安装 (v2.43.7) |
| GitHub Skill | ✅ 已安装 |
| GitHub Token | ⚠️ 需配置 |

---

## 🔧 配置 GitHub Token

### 1. 获取 Token

1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 选择权限：
   - ✅ `repo` - 完整仓库权限
   - ✅ `workflow` - Actions
   - ✅ `user` - 用户信息
4. 生成并复制 token

### 2. 设置 Token

**方法 1: 环境变量**
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

**方法 2: 配置文件**
```bash
cd /home/admin/.openclaw/workspace/skills/github-skill
cp .env.example .env
# 编辑 .env 文件，填入 token
```

**方法 3: openclaw.json**
```json
{
  "env": {
    "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxx"
  }
}
```

### 3. 测试 Token

```bash
# 测试 token 是否有效
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

---

## 🚀 使用示例

### 克隆仓库

```python
import subprocess

# 公开仓库
subprocess.run(["git", "clone", "https://github.com/user/repo.git"])

# 私有仓库
import os
token = os.getenv('GITHUB_TOKEN')
subprocess.run(["git", "clone", f"https://{token}@github.com/user/repo.git"])
```

### 创建分支

```python
import subprocess

subprocess.run(["git", "checkout", "-b", "feature/new-feature"])
subprocess.run(["git", "push", "-u", "origin", "feature/new-feature"])
```

### 创建 Pull Request

```python
import requests
import os

token = os.getenv('GITHUB_TOKEN')
headers = {'Authorization': f'token {token}'}

data = {
    'title': 'feat: new feature',
    'body': 'Description',
    'head': 'feature-branch',
    'base': 'main'
}

response = requests.post(
    'https://api.github.com/repos/user/repo/pulls',
    headers=headers,
    json=data
)

print(response.json())
```

---

## 📋 常用命令

### Git 基础

```bash
# 克隆
git clone <url>

# 分支
git checkout -b <branch>
git branch -a

# 提交
git add .
git commit -m "message"
git push

# 同步
git pull
git fetch
```

### GitHub API

```bash
# 获取用户信息
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user

# 获取仓库列表
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos

# 创建 Issue
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"title":"Issue","body":"Description"}' \
  https://api.github.com/repos/user/repo/issues
```

---

## 🧪 测试

```bash
cd /home/admin/.openclaw/workspace/skills/github-skill
python3 test_github.py
```

---

## ⚠️ 安全提示

- ⚠️ 不要将 token 提交到代码仓库
- ⚠️ 使用 `.gitignore` 忽略敏感文件
- ⚠️ 定期更换 token
- ⚠️ 限制 token 权限范围

---

## 🔗 相关链接

- [GitHub 文档](https://docs.github.com/)
- [Git 下载](https://git-scm.com/)
- [GitHub CLI](https://cli.github.com/)
- [GitHub API](https://docs.github.com/en/rest)

---

**配置完成后记得测试！** ✅
