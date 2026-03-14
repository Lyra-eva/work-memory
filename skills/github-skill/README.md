# GitHub Skill

使用 GitHub API 和 git 命令进行仓库管理。

## 快速开始

### 1. 获取 GitHub Token

1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 选择权限：
   - ✅ `repo` - 完整仓库权限
   - ✅ `workflow` - CI/CD
   - ✅ `user` - 用户信息
4. 生成并复制 token

### 2. 配置 Token

**方法 1: 环境变量**
```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

**方法 2: openclaw.json**
```json
{
  "env": {
    "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxx"
  }
}
```

### 3. 测试配置

```bash
# 测试 token 是否有效
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

## 使用示例

### Python 示例

#### 克隆仓库

```python
import subprocess
import os

def clone_repo(repo_url, target_dir=None):
    """克隆 GitHub 仓库"""
    token = os.getenv('GITHUB_TOKEN')
    
    if token and 'github.com' in repo_url:
        # 私有仓库
        repo_url = repo_url.replace(
            'https://github.com/',
            f'https://{token}@github.com/'
        )
    
    cmd = ['git', 'clone', repo_url]
    if target_dir:
        cmd.append(target_dir)
    
    subprocess.run(cmd)
    print(f"✅ 克隆完成：{repo_url}")

# 使用
clone_repo('https://github.com/openclaw/openclaw')
```

#### 创建分支

```python
import subprocess

def create_branch(branch_name):
    """创建并切换分支"""
    subprocess.run(['git', 'checkout', '-b', branch_name])
    subprocess.run(['git', 'push', '-u', 'origin', branch_name])
    print(f"✅ 分支已创建：{branch_name}")

# 使用
create_branch('feature/new-feature')
```

#### 提交更改

```python
import subprocess

def commit_changes(message):
    """提交并推送更改"""
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', message])
    subprocess.run(['git', 'push'])
    print(f"✅ 提交完成：{message}")

# 使用
commit_changes('feat: add new feature')
```

#### 创建 Pull Request

```python
import requests
import os

def create_pull_request(repo, title, body, head, base='main'):
    """创建 Pull Request"""
    token = os.getenv('GITHUB_TOKEN')
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'title': title,
        'body': body,
        'head': head,
        'base': base
    }
    
    url = f'https://api.github.com/repos/{repo}/pulls'
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        pr = response.json()
        print(f"✅ PR 已创建：{pr['html_url']}")
        return pr
    else:
        print(f"❌ 创建失败：{response.json()}")
        return None

# 使用
create_pull_request(
    repo='user/repo',
    title='feat: add new feature',
    body='Description of changes',
    head='feature/new-feature',
    base='main'
)
```

### Shell 示例

#### 克隆仓库

```bash
# 公开仓库
git clone https://github.com/user/repo.git

# 私有仓库 (使用 token)
git clone https://$GITHUB_TOKEN@github.com/user/repo.git
```

#### 创建 PR

```bash
# 使用 gh CLI
gh pr create \
  --title "feat: new feature" \
  --body "Description" \
  --base main \
  --head feature-branch
```

## 常用 GitHub API

### 用户信息

```bash
# 获取当前用户
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

### 仓库管理

```bash
# 获取用户仓库
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos

# 创建仓库
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"name":"my-repo","private":false}' \
  https://api.github.com/user/repos
```

### Issue 管理

```bash
# 创建 Issue
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"title":"Bug report","body":"Description"}' \
  https://api.github.com/repos/user/repo/issues

# 获取 Issue 列表
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/user/repo/issues
```

### Pull Request

```bash
# 创建 PR
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -d '{"title":"Fix bug","body":"Description","head":"fix-bug","base":"main"}' \
  https://api.github.com/repos/user/repo/pulls

# 获取 PR 列表
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/user/repo/pulls
```

## 工具推荐

### 1. GitHub CLI (gh)

```bash
# 安装
brew install gh
# 或
sudo apt install gh

# 登录
gh auth login

# 使用
gh repo clone user/repo
gh pr create
gh issue create
```

### 2. Git 配置

```bash
# 配置用户信息
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 配置 credential helper
git config --global credential.helper store
```

## 安全提示

- ⚠️ 不要将 token 提交到代码仓库
- ⚠️ 使用 `.gitignore` 忽略敏感文件
- ⚠️ 定期更换 token
- ⚠️ 限制 token 权限范围
- ⚠️ 使用环境变量存储 token

## 故障排除

### Token 无效

```bash
# 测试 token
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user

# 如果返回 401，token 无效或已过期
```

### 权限不足

确保 token 有所需权限：
- `repo` - 仓库操作
- `workflow` - Actions
- `user` - 用户信息

### Git 认证失败

```bash
# 清除缓存
git credential-cache exit

# 重新配置
git config --global credential.helper store
```

---

**配置完成后记得测试！** ✅
