#!/bin/bash
# Work Memory 一键卸载脚本
# 使用方式：./skills/uninstall.sh
# 安全设计：数据可选删除，默认保留

set -e

echo "🗑️  正在卸载 Work Memory..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 步骤 1: 检查是否已安装
echo -e "\n${YELLOW}📦 检查安装状态...${NC}"
if ! python3 -c "import work_memory" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  未检测到已安装的工作记忆系统${NC}"
    echo "可能已经卸载，或者从未安装。"
    read -p "是否继续清理？[y/N]: " confirm
    if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
        echo -e "${YELLOW}⚠️  操作已取消${NC}"
        exit 0
    fi
fi

# 步骤 2: 卸载核心库
echo -e "\n${YELLOW}📦 卸载核心库...${NC}"
if pip3 uninstall -y work-memory 2>/dev/null; then
    echo -e "${GREEN}✅ 核心库已卸载${NC}"
else
    echo -e "${YELLOW}⚠️  pip 卸载失败，尝试手动清理${NC}"
fi

# 步骤 3: 询问是否删除数据
echo -e "\n${YELLOW}📁 数据处理...${NC}"
WM_DATA="$HOME/.openclaw/workspace/work-memory-data"

if [ -d "$WM_DATA" ]; then
    echo -e "${BLUE}发现数据目录：$WM_DATA${NC}"
    echo "包含：项目、任务、技能、会议记录等历史数据"
    echo ""
    read -p "是否删除工作记忆数据？(N/y - 默认保留): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        rm -rf "$WM_DATA"
        echo -e "${GREEN}✅ 数据目录已删除${NC}"
    else
        echo -e "${GREEN}✅ 数据目录已保留：$WM_DATA${NC}"
        echo -e "${BLUE}💡 重新安装时将自动使用现有数据${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  未找到数据目录${NC}"
fi

# 步骤 4: 清理技能缓存
echo -e "\n${YELLOW}🧹 清理技能缓存...${NC}"
SKILL_CACHE="$PROJECT_ROOT/skills/__pycache__"
if [ -d "$SKILL_CACHE" ]; then
    rm -rf "$SKILL_CACHE"
    echo -e "${GREEN}✅ 技能缓存已清理${NC}"
else
    echo -e "${YELLOW}⚠️  无需清理缓存${NC}"
fi

# 完成
echo -e "\n${GREEN}=========================================="
echo "✅ Work Memory 卸载完成！"
echo "==========================================${NC}"

if [ -d "$WM_DATA" ]; then
    echo -e "\n💡 数据目录已保留：$WM_DATA"
    echo "   如需删除：rm -rf $WM_DATA"
fi

echo -e "\n📚 重新安装："
echo "  $SCRIPT_DIR/install.sh"
echo ""
