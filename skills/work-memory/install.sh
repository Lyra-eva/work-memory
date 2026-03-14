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

# 步骤 1: 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误：未找到 Python3${NC}"
    echo "请先安装 Python3"
    exit 1
fi

# 步骤 2: 安装核心库
echo -e "${YELLOW}📦 安装 Work Memory 核心库...${NC}"

# 尝试从 PyPI 安装
if pip3 install -q work-memory 2>/dev/null; then
    echo -e "${GREEN}✅ 核心库安装成功（PyPI）${NC}"
else
    # 如果 PyPI 失败，尝试本地开发模式
    WORK_MEMORY_PROJECT="$HOME/.openclaw/workspace/work-memory-project"
    if [ -d "$WORK_MEMORY_PROJECT" ]; then
        echo -e "${YELLOW}⚠️  PyPI 安装失败，使用本地开发模式...${NC}"
        cd "$WORK_MEMORY_PROJECT" && pip3 install -q -e .
        echo -e "${GREEN}✅ 核心库安装成功（本地开发模式）${NC}"
    else
        echo -e "${RED}❌ 安装失败${NC}"
        echo "请手动执行：pip install work-memory"
        exit 1
    fi
fi

# 步骤 3: 验证安装
echo -e "${YELLOW}🧪 验证安装...${NC}"
if python3 -c "from work_memory import WorkMemory" 2>/dev/null; then
    echo -e "${GREEN}✅ 核心库验证成功${NC}"
else
    echo -e "${RED}❌ 核心库验证失败${NC}"
    exit 1
fi

# 步骤 4: 更新 TOOLS.md（如果不存在 Work Memory 配置）
TOOLS_MD="$HOME/.openclaw/workspace/TOOLS.md"
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
echo "  命令：/wm project create \"项目名称\""
echo "  文档：cat ~/.openclaw/workspace/skills/work-memory/README.md"
echo ""
echo "💡 快速测试："
echo "  /wm stats"
echo ""
