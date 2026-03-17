#!/bin/bash
# Evolution Engine v2 发布脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 版本检查
VERSION=""
SKIP_TESTS=false

# 解析参数
while [[ $# -gt 0 ]]; do
  case $1 in
    -v|--version)
      VERSION="$2"
      shift 2
      ;;
    --skip-tests)
      SKIP_TESTS=true
      shift
      ;;
    -h|--help)
      echo "用法：./publish.sh -v <版本号> [--skip-tests]"
      echo ""
      echo "选项:"
      echo "  -v, --version     版本号 (必需，例如：2.0.0)"
      echo "  --skip-tests      跳过测试"
      echo "  -h, --help        显示帮助"
      exit 0
      ;;
    *)
      echo -e "${RED}未知选项：$1${NC}"
      exit 1
      ;;
  esac
done

# 验证版本号
if [ -z "$VERSION" ]; then
  echo -e "${RED}错误：必须指定版本号 (-v 2.0.0)${NC}"
  exit 1
fi

if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo -e "${RED}错误：版本号格式必须是 X.Y.Z${NC}"
  exit 1
fi

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Evolution Engine v2 - 发布脚本       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# 进入脚本目录
cd "$(dirname "$0")"

# 步骤 1: 预检查
echo -e "${YELLOW}[1/7] 预检查...${NC}"

if ! command -v git &> /dev/null; then
  echo -e "${RED}错误：需要安装 git${NC}"
  exit 1
fi

if ! command -v node &> /dev/null; then
  echo -e "${RED}错误：需要安装 Node.js${NC}"
  exit 1
fi

if ! command -v clawhub &> /dev/null; then
  echo -e "${YELLOW}警告：clawhub CLI 未安装，将尝试安装...${NC}"
  npm install -g clawhub
fi

echo -e "${GREEN}✓ 预检查通过${NC}"
echo ""

# 步骤 2: 更新版本号
echo -e "${YELLOW}[2/7] 更新版本号到 ${VERSION}...${NC}"

# 更新 package.json
if command -v jq &> /dev/null; then
  jq ".version = \"$VERSION\"" package.json > package.json.tmp && mv package.json.tmp package.json
else
  # 使用 node 更新
  node -e "const p=require('./package.json');p.version='$VERSION';require('fs').writeFileSync('package.json',JSON.stringify(p,null,2))"
fi

# 更新 SKILL.md 版本号
sed -i.bak "s/\\*\\*版本\\*\\*: [0-9.]\+/\\*\\*版本\\*\\*: $VERSION/" SKILL.md
rm -f SKILL.md.bak

# 更新 README.md 版本号
sed -i.bak "s/\\*\\*版本\\*\\*: [0-9.]\+/\\*\\*版本\\*\\*: $VERSION/" README.md
rm -f README.md.bak

echo -e "${GREEN}✓ 版本号已更新${NC}"
echo ""

# 步骤 3: 运行测试（可选）
if [ "$SKIP_TESTS" = false ]; then
  echo -e "${YELLOW}[3/7] 运行测试...${NC}"
  
  # 测试事件收集
  npx tsx src/event-collector.ts collect --type success --data '{"task":"发布测试"}' || {
    echo -e "${RED}✗ 事件收集测试失败${NC}"
    exit 1
  }
  
  # 测试统计
  npx tsx src/event-collector.ts stats || {
    echo -e "${RED}✗ 统计测试失败${NC}"
    exit 1
  }
  
  # 测试反思
  npx tsx src/reflector.ts --dry-run || {
    echo -e "${RED}✗ 反思测试失败${NC}"
    exit 1
  }
  
  # 测试上下文注入
  npx tsx src/context-injector.ts > /dev/null || {
    echo -e "${RED}✗ 上下文注入测试失败${NC}"
    exit 1
  }
  
  echo -e "${GREEN}✓ 所有测试通过${NC}"
else
  echo -e "${YELLOW}[3/7] 跳过测试 (--skip-tests)${NC}"
fi
echo ""

# 步骤 4: Git 提交
echo -e "${YELLOW}[4/7] Git 提交...${NC}"

git add -A
git commit -m "Release v$VERSION" || {
  echo -e "${YELLOW}没有需要提交的更改${NC}"
}

git tag -a "v$VERSION" -m "Release v$VERSION"

echo -e "${GREEN}✓ Git 提交和标签已创建${NC}"
echo ""

# 步骤 5: 推送到 GitHub
echo -e "${YELLOW}[5/7] 推送到 GitHub...${NC}"

read -p "是否推送到远程仓库？(y/n): " confirm
if [ "$confirm" = "y" ]; then
  git push origin main
  git push origin "v$VERSION"
  echo -e "${GREEN}✓ 已推送到 GitHub${NC}"
else
  echo -e "${YELLOW}跳过推送（可以稍后手动推送）${NC}"
fi
echo ""

# 步骤 6: 发布到 ClawHub
echo -e "${YELLOW}[6/7] 发布到 ClawHub...${NC}"

read -p "是否发布到 ClawHub？(y/n): " confirm
if [ "$confirm" = "y" ]; then
  if ! clawhub whoami &> /dev/null; then
    echo -e "${YELLOW}需要先登录 ClawHub...${NC}"
    clawhub login
  fi
  
  clawhub publish . \
    --slug evolution-engine-v2 \
    --name "Evolution Engine v2" \
    --version "$VERSION" \
    --changelog "Release $VERSION - 完整功能版本" \
    --category automation \
    --tags ai,evolution,learning,memory,reflection
  
  echo -e "${GREEN}✓ 已发布到 ClawHub${NC}"
else
  echo -e "${YELLOW}跳过 ClawHub 发布${NC}"
fi
echo ""

# 步骤 7: 创建 GitHub Release
echo -e "${YELLOW}[7/7] 创建 GitHub Release...${NC}"

echo -e "${BLUE}请在 GitHub 上创建 Release:${NC}"
echo -e "  https://github.com/openclaw/skill-evolution-engine-v2/releases/new"
echo ""
echo -e "标签：v$VERSION"
echo -e "标题：Evolution Engine v2 $VERSION"
echo ""

# 完成
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  发布完成！                          ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}下一步:${NC}"
echo "  1. 在 GitHub 上创建 Release"
echo "  2. 验证 ClawHub 安装：clawhub install evolution-engine-v2"
echo "  3. 测试安装的技能"
echo ""
