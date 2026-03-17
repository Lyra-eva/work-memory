#!/bin/bash
# 进化引擎卸载脚本

set -e

echo "=========================================="
echo "🗑️ 进化引擎卸载"
echo "=========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. 卸载核心库
echo -e "\n${YELLOW}【1/3】卸载核心库...${NC}"
pip3 uninstall -y evolution-engine 2>/dev/null || true
echo -e "${GREEN}✅ 核心库已卸载${NC}"

# 2. 询问是否删除数据
echo -e "\n${YELLOW}【2/3】数据处理...${NC}"
DATA_DIR="$HOME/.openclaw/workspace/evolution-data"

if [ -d "$DATA_DIR" ]; then
    read -p "是否删除进化数据？(y/N): " confirm
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        rm -rf "$DATA_DIR"
        echo -e "${GREEN}✅ 数据目录已删除${NC}"
    else
        echo -e "${YELLOW}⚠️  保留数据目录：$DATA_DIR${NC}"
    fi
fi

# 3. 清理技能
echo -e "\n${YELLOW}【3/3】清理技能文件...${NC}"
SKILL_DIR="$HOME/.openclaw/workspace/skills/evolution-engine"
if [ -d "$SKILL_DIR" ]; then
    # 保留 SKILL.md，删除其他文件
    find "$SKILL_DIR" -type f ! -name "SKILL.md" -delete 2>/dev/null || true
    echo -e "${GREEN}✅ 技能文件已清理${NC}"
fi

# 完成
echo -e "\n${GREEN}=========================================="
echo "✅ 进化引擎卸载完成！"
echo "==========================================${NC}"

if [ -d "$DATA_DIR" ]; then
    echo -e "\n💡 数据目录已保留：$DATA_DIR"
    echo "   如需删除：rm -rf $DATA_DIR"
fi
echo ""
