#!/bin/bash
# GitHub Release 快速发布脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  GitHub Release 发布脚本              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# 进入脚本目录
cd "$(dirname "$0")"

# 步骤 1: 检查 Git 状态
echo -e "${YELLOW}[1/5] 检查 Git 状态...${NC}"
git status --short
echo ""

# 步骤 2: 设置远程仓库
echo -e "${YELLOW}[2/5] 设置远程仓库...${NC}"
read -p "请输入 GitHub 用户名: " GITHUB_USER
REMOTE_URL="https://github.com/${GITHUB_USER}/skill-evolution-engine-v2.git"

git remote set-url origin "$REMOTE_URL" 2>/dev/null || \
  git remote add origin "$REMOTE_URL"

echo -e "${GREEN}✓ 远程仓库已设置：$REMOTE_URL${NC}"
echo ""

# 步骤 3: 推送代码
echo -e "${YELLOW}[3/5] 推送代码到 GitHub...${NC}"
read -p "是否推送代码？(y/n): " confirm
if [ "$confirm" = "y" ]; then
  git push -u origin master
  echo -e "${GREEN}✓ 代码已推送${NC}"
else
  echo -e "${YELLOW}跳过推送${NC}"
fi
echo ""

# 步骤 4: 推送标签
echo -e "${YELLOW}[4/5] 推送标签到 GitHub...${NC}"
read -p "是否推送标签 v2.0.0？(y/n): " confirm
if [ "$confirm" = "y" ]; then
  git push origin v2.0.0
  echo -e "${GREEN}✓ 标签已推送${NC}"
else
  echo -e "${YELLOW}跳过标签推送${NC}"
fi
echo ""

# 步骤 5: 创建 Release 指引
echo -e "${YELLOW}[5/5] 创建 GitHub Release 指引...${NC}"
echo ""
echo -e "${BLUE}请按以下步骤创建 GitHub Release:${NC}"
echo ""
echo "1. 访问：https://github.com/${GITHUB_USER}/skill-evolution-engine-v2/releases/new"
echo "2. 标签选择：v2.0.0"
echo "3. 标题：Evolution Engine v2 2.0.0"
echo "4. 描述：复制 GITHUB_RELEASE.md 中的 Release Notes"
echo "5. 点击 'Publish release'"
echo ""
echo -e "${BLUE}Release Notes 已保存在：GITHUB_RELEASE.md${NC}"
echo ""

# 完成
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  发布指引完成！                      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}下一步:${NC}"
echo "  1. 在 GitHub 上创建 Release"
echo "  2. 验证 Release 页面"
echo "  3. 分享仓库链接给用户"
echo ""
