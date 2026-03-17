#!/bin/bash
# Evolution Engine v2 安装脚本

set -e

WORKSPACE_DIR="$HOME/.openclaw/workspace"
EVOLUTION_DIR="$WORKSPACE_DIR/memory/evolution"
SKILL_DIR="$WORKSPACE_DIR/skills/evolution-engine-v2"

echo "🧬 安装 Evolution Engine v2..."
echo ""

# 创建数据目录
echo "📁 创建数据目录..."
mkdir -p "$EVOLUTION_DIR"
mkdir -p "$SKILL_DIR/src"

# 安装依赖
echo "📦 安装依赖..."
cd "$SKILL_DIR"
if command -v pnpm &> /dev/null; then
    pnpm install
elif command -v npm &> /dev/null; then
    npm install
else
    echo "⚠️  未找到 pnpm 或 npm，请手动安装依赖"
fi

# 初始化配置
echo "⚙️  初始化配置..."
cd "$WORKSPACE_DIR"
npx tsx "$SKILL_DIR/src/openclaw-integration.ts" init

# 创建便捷别名
echo "🔧 创建便捷命令..."
ALIAS_FILE="$HOME/.bashrc"
if [ -f "$HOME/.zshrc" ]; then
    ALIAS_FILE="$HOME/.zshrc"
fi

# 检查别名是否已存在
if ! grep -q "evolve" "$ALIAS_FILE" 2>/dev/null; then
    cat >> "$ALIAS_FILE" << 'EOF'

# Evolution Engine v2 快捷命令
alias evolve='cd ~/.openclaw/workspace && npx tsx skills/evolution-engine-v2/src/event-collector.ts collect'
alias evolve-stats='cd ~/.openclaw/workspace && npx tsx skills/evolution-engine-v2/src/event-collector.ts stats'
alias evolve-reflect='cd ~/.openclaw/workspace && npx tsx skills/evolution-engine-v2/src/reflector.ts'
alias evolve-inject='cd ~/.openclaw/workspace && npx tsx skills/evolution-engine-v2/src/context-injector.ts'
EOF
    echo "✅ 已添加便捷命令到 $ALIAS_FILE"
    echo "   运行 'source $ALIAS_FILE' 或重新打开终端以生效"
else
    echo "ℹ️  便捷命令已存在"
fi

# 完成
echo ""
echo "✅ 安装完成!"
echo ""
echo "📚 使用指南:"
echo ""
echo "  快捷命令 (需要先 source ~/.bashrc 或 ~/.zshrc):"
echo "    evolve --type success --data '{\"task\":\"xxx\"}'"
echo "    evolve-stats"
echo "    evolve-reflect"
echo "    evolve-inject"
echo ""
echo "  或使用完整命令:"
echo "    cd ~/.openclaw/workspace"
echo "    npx tsx skills/evolution-engine-v2/src/event-collector.ts collect --type success --data '{\"task\":\"xxx\"}'"
echo ""
echo "  启用自动反思 (每天凌晨 3 点):"
echo "    npx tsx skills/evolution-engine-v2/src/openclaw-integration.ts enable"
echo ""
echo "🎉 开始进化之旅吧!"
