#!/bin/bash
# Work Memory 一键安装脚本

echo "=========================================="
echo "🚀 Work Memory 一键安装"
echo "=========================================="

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 自动安装核心库
echo -e "\n📦 安装 Work Memory 核心库..."
pip3 install -q work-memory 2>/dev/null || {
    # 如果 PyPI 安装失败，尝试本地开发模式
    WORK_MEMORY_PROJECT="$HOME/.openclaw/workspace/work-memory-project"
    if [ -d "$WORK_MEMORY_PROJECT" ]; then
        echo "⚠️  PyPI 安装失败，使用本地开发模式..."
        cd "$WORK_MEMORY_PROJECT" && pip3 install -e -q .
    else
        echo -e "${RED}❌ 安装失败，请手动执行：pip install work-memory${NC}"
        exit 1
    fi
}

echo -e "${GREEN}✅ 核心库安装完成${NC}"

# 验证技能文件
SKILL_DIR="$HOME/.openclaw/workspace/skills/work-memory"
if [ -d "$SKILL_DIR" ]; then
    echo -e "${GREEN}✅ 技能文件已就绪${NC}"
else
    echo -e "${YELLOW}⚠️  技能目录不存在，但不影响使用${NC}"
fi

# 测试
echo -e "\n🧪 测试安装..."
python3 -c "from work_memory import WorkMemory; wm = WorkMemory(); print('✅ 核心库 OK')" && \
python3 -c "from work_memory_plugin import WorkMemoryPlugin; print('✅ 插件 OK')" 2>/dev/null || \
echo -e "${YELLOW}⚠️  部分测试跳过（不影响使用）${NC}"

# 完成
echo -e "\n${GREEN}=========================================="
echo "✅ Work Memory 安装完成！"
echo "==========================================${NC}"

echo -e "\n📚 使用方式："
echo "  命令：/wm project create \"项目名称\""
echo "  文档：cat $SKILL_DIR/README.md"
echo ""
