#!/bin/bash
# Work Memory 一键安装脚本
# 此脚本会在 clawhub install work-memory 时自动执行

set -e

echo "🚀 正在安装 Work Memory..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

WORKSPACE="$HOME/.openclaw/workspace"

# 步骤 1: 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误：未找到 Python3${NC}"
    echo "请先安装 Python3"
    exit 1
fi

# 步骤 2: 安装工作记忆系统核心
echo -e "${YELLOW}📦 安装工作记忆系统核心...${NC}"

WM_V1="$WORKSPACE/work-memory-v1"
if [ -d "$WM_V1" ]; then
    echo -e "${GREEN}✅ 找到 work-memory-v1，安装核心库...${NC}"
    cd "$WM_V1" && pip3 install -q -e .
    echo -e "${GREEN}✅ 工作记忆系统安装成功${NC}"
else
    echo -e "${RED}❌ 未找到 work-memory-v1 目录${NC}"
    echo "请确保从 GitHub 正确克隆仓库"
    exit 1
fi

# 步骤 3: 验证工作记忆安装
echo -e "${YELLOW}🧪 验证工作记忆系统...${NC}"
if python3 -c "from work_memory import WorkMemory" 2>/dev/null; then
    echo -e "${GREEN}✅ 工作记忆系统验证成功${NC}"
else
    echo -e "${RED}❌ 工作记忆系统验证失败${NC}"
    exit 1
fi

# 步骤 4: 验证进化引擎
echo -e "${YELLOW}🧪 验证进化引擎...${NC}"
EVOLUTION="$WORKSPACE/work-memory-evolution/evolution"
if [ -d "$EVOLUTION" ]; then
    export PYTHONPATH="$EVOLUTION:$PYTHONPATH"
    if python3 -c "from core.knowledge_graph import KnowledgeGraph" 2>/dev/null; then
        echo -e "${GREEN}✅ 进化引擎验证成功${NC}"
    else
        echo -e "${RED}❌ 进化引擎验证失败${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  未找到进化引擎（可选组件）${NC}"
fi

# 步骤 5: 创建数据目录
echo -e "${YELLOW}📁 创建工作目录...${NC}"
WM_DATA="$WORKSPACE/work-memory-data"
if [ ! -d "$WM_DATA" ]; then
    mkdir -p "$WM_DATA"
    echo -e "${GREEN}✅ 工作目录已创建${NC}"
else
    echo -e "${GREEN}✅ 工作目录已存在${NC}"
fi

# 步骤 6: 更新 TOOLS.md
TOOLS_MD="$WORKSPACE/TOOLS.md"
if [ -f "$TOOLS_MD" ] && ! grep -q "Work Memory" "$TOOLS_MD" 2>/dev/null; then
    echo -e "${YELLOW}📝 更新 TOOLS.md...${NC}"
    cat >> "$TOOLS_MD" << 'EOF'

---

## Work Memory

工作记忆系统配置 - 用于项目/任务/日志管理

- **数据目录**: `~/.openclaw/workspace/work-memory-data/`
- **自动备份**: 每天 23:00
EOF
    echo -e "${GREEN}✅ TOOLS.md 已更新${NC}"
fi

# 完成
echo -e "\n${GREEN}=========================================="
echo "✅ Work Memory 安装完成！"
echo "==========================================${NC}"

echo -e "\n📚 使用方式："
echo "  导入：from work_memory import WorkMemory"
echo "  文档：cat $WORKSPACE/skills/work-memory/README.md"
echo ""
echo "💡 快速测试："
echo "  python3 -c 'from work_memory import WorkMemory; wm = WorkMemory(); print(wm.get_stats())'"
echo ""
