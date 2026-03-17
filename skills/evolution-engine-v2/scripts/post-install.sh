#!/bin/bash
# 安装后初始化脚本

set -e

SKILL_DIR="$HOME/.openclaw/workspace/skills/evolution-engine-v2"
DATA_DIR="$HOME/.openclaw/workspace/memory/evolution"

echo "🧬 Evolution Engine v2 - 安装后初始化"
echo ""

# 创建数据目录
echo "📁 创建数据目录..."
mkdir -p "$DATA_DIR"
echo "✅ 数据目录：$DATA_DIR"
echo ""

# 安装依赖
echo "📦 安装依赖..."
cd "$SKILL_DIR"
if command -v pnpm &> /dev/null; then
    pnpm install
elif command -v npm &> /dev/null; then
    npm install
else
    echo "⚠️  请手动安装依赖：npm install 或 pnpm install"
fi
echo ""

# 初始化配置
echo "⚙️  初始化配置..."
npx tsx src/openclaw-integration.ts init
echo ""

# 提示
echo "✅ 安装完成！"
echo ""
echo "📚 下一步:"
echo "  1. 启用自动进化："
echo "     npx tsx src/openclaw-integration.ts enable"
echo ""
echo "  2. 记录第一个事件:"
echo "     npx tsx src/event-collector.ts collect --type success --data '{\"task\":\"安装成功\"}'"
echo ""
echo "  3. 查看文档:"
echo "     cat SKILL.md"
echo ""
