---
name: github-skill
description: GitHub 操作技能。支持仓库克隆、文件上传、PR 创建等 GitHub 操作。
author: OpenClaw Community
version: 1.0.0
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["git"] },
        "config": {
          "env": {
            "GITHUB_TOKEN": {
              "description": "GitHub Personal Access Token",
              "required": false
            }
          }
        }
      }
  }
---

# GitHub Skill

使用 GitHub API 和 git 命令进行仓库管理。

## 配置

### 1. 获取 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token**
3. 选择权限：
   - ✅ repo (完整仓库权限)
   - ✅ workflow (CI/CD)
   - ✅ user (用户信息)
4. 生成并复制 token

### 2. 设置环境变量

```bash
export GITHUB_TOKEN="your_token_here"
```

或在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "env": {
    "GITHUB_TOKEN": "your_token_here"
  }
}
```

## 使用示例

### 克隆仓库

```python
import subprocess

# 克隆公开仓库
subprocess.run(["git", "clone", "https://github.com/user/repo.git"])

# 克隆私有仓库 (使用 token)
subprocess.run(["git", "clone", "https://YOUR_TOKEN@github.com/user/repo.git"])
```

### 创建分支

```python
import subprocess

subprocess.run(["git", "checkout", "-b", "feature/new-feature"])
subprocess.run(["git", "push", "-u", "origin", "feature/new-feature"])
```

### 提交更改

```python
import subprocess

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "feat: add new feature"])
subprocess.run(["git", "push"])
```

### 创建 Pull Request

```python
import requests
import os

token = os.getenv('GITHUB_TOKEN')
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

data = {
    'title': 'feat: add new feature',
    'body': 'Description of changes',
    'head': 'feature/new-feature',
    'base': 'main'
}

response = requests.post(
    'https://api.github.com/repos/user/repo/pulls',
    headers=headers,
    json=data
)

print(response.json())
```

## 常用命令

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
curl -H "Authorization: token TOKEN" https://api.github.com/user

# 获取仓库列表
curl -H "Authorization: token TOKEN" https://api.github.com/user/repos

# 创建 Issue
curl -X POST \
  -H "Authorization: token TOKEN" \
  -d '{"title":"Issue title","body":"Description"}' \
  https://api.github.com/repos/user/repo/issues
```

## 注意事项

- ⚠️ 不要将 token 提交到代码仓库
- ⚠️ 使用 `.gitignore` 忽略敏感文件
- ⚠️ 定期更换 token
- ⚠️ 限制 token 权限范围

---

**配置完成后记得测试！** ✅
