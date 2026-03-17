#!/bin/bash
# 进化引擎安装脚本

set -e

echo "=========================================="
echo "🚀 进化引擎 v2.0 安装"
echo "=========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. 安装核心库
echo -e "\n${YELLOW}【1/4】安装核心库...${NC}"
ENGINE_DIR="$HOME/.openclaw/workspace/evolution-engine-v2"

if [ ! -d "$ENGINE_DIR" ]; then
    echo -e "${RED}❌ 错误：进化引擎目录不存在${NC}"
    echo "   路径：$ENGINE_DIR"
    exit 1
fi

cd "$ENGINE_DIR"
pip3 install --user -e . > /dev/null 2>&1
echo -e "${GREEN}✅ 核心库安装成功${NC}"

# 2. 创建数据目录
echo -e "\n${YELLOW}【2/4】创建数据目录...${NC}"
DATA_DIR="$HOME/.openclaw/workspace/evolution-data"
mkdir -p "$DATA_DIR"/{events,capabilities,patterns,skills,backups,logs}
echo -e "${GREEN}✅ 数据目录已创建：$DATA_DIR${NC}"

# 3. 验证安装
echo -e "\n${YELLOW}【3/4】验证安装...${NC}"
python3 -c "from evolution_engine import EvolutionEngine; e = EvolutionEngine(); print('✅ 模块导入成功')" 2>/dev/null || {
    echo -e "${RED}❌ 警告：模块导入失败${NC}"
    echo "   尝试手动安装：cd $ENGINE_DIR && pip3 install -e ."
    exit 1
}

# 4. 更新 TOOLS.md
echo -e "\n${YELLOW}【4/4】配置 TOOLS.md...${NC}"
TOOLS_MD="$HOME/.openclaw/workspace/TOOLS.md"

if ! grep -q "Evolution Engine" "$TOOLS_MD" 2>/dev/null; then
    cat >> "$TOOLS_MD" << 'EOF'

---

## Evolution Engine

进化引擎配置 - AI 自主进化系统

- **数据目录**: `~/.openclaw/workspace/evolution-data/`
- **自动启用**: true
- **OODA 循环间隔**: 30 秒
EOF
    echo -e "${GREEN}✅ TOOLS.md 已更新${NC}"
else
    echo -e "${GREEN}✅ TOOLS.md 已包含 Evolution Engine 配置${NC}"
fi

# 完成
echo -e "\n${GREEN}=========================================="
echo "✅ 进化引擎安装完成！"
echo "==========================================${NC}"

echo -e "\n📚 使用方式："
echo "  启用：python3 -c \"from evolution_engine import EvolutionEngine; e = EvolutionEngine(); e.enable()\""
echo "  查看状态：python3 -c \"from evolution_engine import get_engine_status; print(get_engine_status())\""
echo ""
