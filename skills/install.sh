#!/bin/bash
# Work Memory 一键安装脚本
# 使用方式：./skills/install.sh

set -e

echo "🚀 正在安装 Work Memory..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 步骤 1: 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误：未找到 Python3${NC}"
    echo "请先安装 Python3"
    exit 1
fi

# 步骤 2: 安装核心库
echo -e "${YELLOW}📦 安装工作记忆核心库...${NC}"
cd "$PROJECT_ROOT"

# 尝试使用 --break-system-packages（适用于系统 Python）
if pip3 install -e . 2>/dev/null; then
    echo -e "${GREEN}✅ 核心库安装成功${NC}"
elif pip3 install --break-system-packages -e . 2>/dev/null; then
    echo -e "${GREEN}✅ 核心库安装成功（使用 --break-system-packages）${NC}"
else
    echo -e "${RED}❌ 核心库安装失败${NC}"
    echo "建议：创建虚拟环境后安装"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -e ."
    exit 1
fi

# 步骤 3: 验证安装
echo -e "${YELLOW}🧪 验证安装...${NC}"
if python3 -c "from work_memory import WorkMemory" 2>/dev/null; then
    echo -e "${GREEN}✅ 工作记忆系统验证成功${NC}"
else
    echo -e "${RED}❌ 验证失败${NC}"
    exit 1
fi

# 步骤 4: 创建数据目录
echo -e "${YELLOW}📁 创建工作目录...${NC}"
WM_DATA="$HOME/.openclaw/workspace/work-memory-data"
mkdir -p "$WM_DATA"
echo -e "${GREEN}✅ 工作目录已创建：$WM_DATA${NC}"

# 完成
echo -e "\n${GREEN}=========================================="
echo "✅ Work Memory 安装完成！"
echo "==========================================${NC}"

echo -e "\n📚 使用方式："
echo "  Python: from work_memory import WorkMemory"
echo "  初始化：wm = WorkMemory()"
echo ""
echo "💡 快速测试："
echo "  python3 -c 'from work_memory import WorkMemory; wm = WorkMemory(); print(wm.get_stats())'"
echo ""
echo "📖 文档："
echo "  cat $PROJECT_ROOT/README.md"
echo ""
