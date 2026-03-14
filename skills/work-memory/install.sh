#!/bin/bash
# Work Memory 技能安装脚本

set -e

echo "=========================================="
echo "🚀 Work Memory 技能安装"
echo "=========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 Python
echo -e "\n${YELLOW}【1/4】检查 Python 环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误：未找到 Python3${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python 版本：$(python3 --version)${NC}"

# 安装工作记忆核心库
echo -e "\n${YELLOW}【2/4】安装 Work Memory 核心库...${NC}"
WORK_MEMORY_PROJECT="$HOME/.openclaw/workspace/work-memory-project"

if [ ! -d "$WORK_MEMORY_PROJECT" ]; then
    echo -e "${RED}❌ 错误：工作记忆项目目录不存在${NC}"
    echo "   路径：$WORK_MEMORY_PROJECT"
    echo ""
    echo "提示：请先克隆或下载工作记忆项目："
    echo "  git clone https://github.com/Lyra-eva/work-memory.git $WORK_MEMORY_PROJECT"
    exit 1
fi

cd "$WORK_MEMORY_PROJECT"
pip3 install -e . > /dev/null 2>&1
echo -e "${GREEN}✅ Work Memory 核心库已安装${NC}"

# 验证技能文件
echo -e "\n${YELLOW}【3/4】验证技能文件...${NC}"
SKILL_DIR="$HOME/.openclaw/workspace/skills/work-memory"

if [ ! -d "$SKILL_DIR" ]; then
    echo -e "${RED}❌ 错误：技能目录不存在${NC}"
    echo "   路径：$SKILL_DIR"
    exit 1
fi

required_files=("SKILL.md" "work_memory_plugin.py" "README.md")
for file in "${required_files[@]}"; do
    if [ ! -f "$SKILL_DIR/$file" ]; then
        echo -e "${RED}❌ 错误：缺少必要文件 $file${NC}"
        exit 1
    fi
done
echo -e "${GREEN}✅ 技能文件验证通过${NC}"

# 更新 TOOLS.md
echo -e "\n${YELLOW}【4/4】配置 TOOLS.md...${NC}"
TOOLS_MD="$HOME/.openclaw/workspace/TOOLS.md"

if ! grep -q "Work Memory" "$TOOLS_MD" 2>/dev/null; then
    echo -e "\n\n## Work Memory\n\n工作记忆系统配置 - 用于项目/任务/日志管理\n\n- **数据目录**: \`~/.openclaw/workspace/work-memory-data/\`\n- **备份目录**: \`~/.openclaw/workspace/work-memory-backups/\`\n- **自动备份**: 每天 23:00（通过 cron）" >> "$TOOLS_MD"
    echo -e "${GREEN}✅ 已更新 TOOLS.md${NC}"
else
    echo -e "${GREEN}✅ TOOLS.md 已包含 Work Memory 配置${NC}"
fi

# 测试安装
echo -e "\n${YELLOW}测试安装...${NC}"
cd "$SKILL_DIR"
python3 -c "from work_memory_plugin import WorkMemoryPlugin; print('✅ 插件导入成功')" 2>/dev/null || {
    echo -e "${RED}❌ 警告：插件导入失败，请检查依赖${NC}"
    echo "   尝试手动安装：cd $WORK_MEMORY_PROJECT && pip3 install -e ."
    exit 1
}

# 完成
echo -e "\n${GREEN}=========================================="
echo "✅ Work Memory 技能安装完成！"
echo "==========================================${NC}"

echo -e "\n📚 下一步："
echo "  1. 查看文档：cat $SKILL_DIR/README.md"
echo "  2. 运行示例：python3 $SKILL_DIR/example_usage.py"
echo "  3. 开始使用：在技能中导入 WorkMemoryPlugin"
echo ""
echo "💡 快速测试："
echo "  python3 -c \"from work_memory_plugin import WorkMemoryPlugin; p = WorkMemoryPlugin(); print(p.get_stats())\""
echo ""
