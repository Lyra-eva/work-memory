#!/bin/bash
# OpenClaw Workspace 安装脚本
# 从发布仓库安装产品级组件

set -e

echo "=========================================="
echo "🚀 OpenClaw Workspace 安装"
echo "=========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RELEASE_DIR="$SCRIPT_DIR/release"
SRC_DIR="$SCRIPT_DIR/src"
OPENCLAW_SKILLS="$HOME/.openclaw/workspace/skills"

# ============================================================
# 步骤 1: 检查 Python 和 pip
# ============================================================
echo -e "\n${YELLOW}【1/5】检查 Python 和 pip...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误：未找到 Python3${NC}"
    echo "请先安装 Python3"
    exit 1
fi

if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo -e "${RED}❌ 错误：未找到 pip${NC}"
    echo ""
    echo "请安装 pip："
    echo "  Ubuntu/Debian: sudo apt-get install python3-pip"
    echo "  CentOS/RHEL:   sudo yum install python3-pip"
    echo "  macOS:         brew install python3"
    echo "  或者：         curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py"
    echo ""
    exit 1
fi

PIP_CMD="pip3"
if ! command -v pip3 &> /dev/null; then
    PIP_CMD="pip"
fi

echo -e "${GREEN}✅ Python 和 pip 检查通过${NC}"
echo -e "${BLUE}   Python: $(python3 --version)${NC}"
echo -e "${BLUE}   pip: $($PIP_CMD --version | head -1)${NC}"

# ============================================================
# 步骤 2: 检查发布仓库
# ============================================================
echo -e "\n${YELLOW}【2/6】检查发布仓库...${NC}"

if [ ! -d "$RELEASE_DIR/work-memory-release" ]; then
    echo -e "${RED}❌ 未找到工作记忆发布仓库${NC}"
    echo "   路径：$RELEASE_DIR/work-memory-release"
    exit 1
fi

if [ ! -d "$RELEASE_DIR/evolution-engine-release" ]; then
    echo -e "${RED}❌ 未找到进化引擎发布仓库${NC}"
    echo "   路径：$RELEASE_DIR/evolution-engine-release"
    exit 1
fi

echo -e "${GREEN}✅ 发布仓库检查通过${NC}"

# ============================================================
# 步骤 3: 安装工作记忆系统（Python 核心包）
# ============================================================
echo -e "\n${YELLOW}【3/6】安装工作记忆系统（Python 核心包）...${NC}"
cd "$RELEASE_DIR/work-memory-release"

if $PIP_CMD install -e . --user 2>&1 | tee /tmp/work-memory-install.log | grep -q "Successfully installed"; then
    echo -e "${GREEN}✅ 工作记忆核心包安装成功${NC}"
    echo -e "${BLUE}   安装位置：$(python3 -c "import work_memory, os; print(os.path.dirname(work_memory.__file__))")${NC}"
elif python3 -c "import work_memory" 2>/dev/null; then
    echo -e "${GREEN}✅ 工作记忆核心包已安装${NC}"
else
    echo -e "${RED}❌ 工作记忆核心包安装失败${NC}"
    echo "查看日志：/tmp/work-memory-install.log"
    exit 1
fi

# ============================================================
# 步骤 3: 安装工作记忆技能（OpenClaw 技能目录）
# ============================================================
echo -e "\n${YELLOW}【3/5】安装工作记忆技能（OpenClaw 技能目录）...${NC}"

if [ -d "$SRC_DIR/work-memory-project/skills/work-memory" ]; then
    SKILL_SRC="$SRC_DIR/work-memory-project/skills/work-memory"
elif [ -d "$OPENCLAW_SKILLS/work-memory" ]; then
    SKILL_SRC="$OPENCLAW_SKILLS/work-memory"
    echo -e "${BLUE}   技能已存在，跳过安装${NC}"
else
    echo -e "${YELLOW}⚠️  未找到工作记忆技能源文件${NC}"
    SKILL_SRC=""
fi

if [ -n "$SKILL_SRC" ] && [ ! -d "$OPENCLAW_SKILLS/work-memory" ]; then
    # 备份现有技能
    if [ -d "$OPENCLAW_SKILLS/work-memory" ]; then
        BACKUP_DIR="$OPENCLAW_SKILLS/.backups/work-memory_$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$(dirname "$BACKUP_DIR")"
        cp -r "$OPENCLAW_SKILLS/work-memory" "$BACKUP_DIR"
        echo -e "${BLUE}   已备份现有技能：$BACKUP_DIR${NC}"
    fi
    
    # 复制技能到 OpenClaw skills 目录
    cp -r "$SKILL_SRC" "$OPENCLAW_SKILLS/work-memory/"
    echo -e "${GREEN}✅ 工作记忆技能已安装${NC}"
    echo -e "${BLUE}   安装位置：$OPENCLAW_SKILLS/work-memory/${NC}"
fi

# ============================================================
# 步骤 5: 安装进化引擎系统（Python 核心包）
# ============================================================
echo -e "\n${YELLOW}【5/6】安装进化引擎系统（Python 核心包）...${NC}"
cd "$RELEASE_DIR/evolution-engine-release"

if $PIP_CMD install -e . --user 2>&1 | tee /tmp/evolution-engine-install.log | grep -q "Successfully installed"; then
    echo -e "${GREEN}✅ 进化引擎核心包安装成功${NC}"
    echo -e "${BLUE}   安装位置：$(python3 -c "import evolution_engine, os; print(os.path.dirname(evolution_engine.__file__))")${NC}"
elif python3 -c "from evolution_engine import EvolutionEngine" 2>/dev/null; then
    echo -e "${GREEN}✅ 进化引擎核心包已安装${NC}"
else
    echo -e "${RED}❌ 进化引擎核心包安装失败${NC}"
    echo "查看日志：/tmp/evolution-engine-install.log"
    exit 1
fi

# ============================================================
# 步骤 6: 安装进化引擎技能（OpenClaw 技能目录）
# ============================================================
echo -e "\n${YELLOW}【6/6】安装进化引擎技能（OpenClaw 技能目录）...${NC}"

if [ -d "$OPENCLAW_SKILLS/evolution-engine" ]; then
    echo -e "${BLUE}   技能已存在，跳过安装${NC}"
else
    if [ -d "$SRC_DIR/evolution-engine/skills" ]; then
        # 复制技能到 OpenClaw skills 目录
        cp -r "$SRC_DIR/evolution-engine/skills" "$OPENCLAW_SKILLS/evolution-engine/"
        echo -e "${GREEN}✅ 进化引擎技能已安装${NC}"
        echo -e "${BLUE}   安装位置：$OPENCLAW_SKILLS/evolution-engine/${NC}"
    else
        echo -e "${YELLOW}⚠️  未找到进化引擎技能源文件${NC}"
    fi
fi

# ============================================================
# 完成
# ============================================================
echo -e "\n${GREEN}=========================================="
echo "✅ OpenClaw Workspace 安装完成！"
echo "==========================================${NC}"

echo -e "\n${BLUE}📦 已安装产品：${NC}"
echo "  1. 工作记忆系统 (work-memory)"
echo "     - Python 核心包：site-packages/work_memory/"
echo "     - OpenClaw 技能：$OPENCLAW_SKILLS/work-memory/"
echo ""
echo "  2. 进化引擎系统 (evolution-engine)"
echo "     - Python 核心包：site-packages/evolution_engine/"
echo "     - OpenClaw 技能：$OPENCLAW_SKILLS/evolution-engine/"
echo ""
echo "📁 目录结构："
echo "  - src/       : 开发仓库（源代码）"
echo "  - release/   : 发布仓库（产品级，仅 Python 包）"
echo "  - skills/    : OpenClaw 技能（默认目录）"
echo ""
echo "🚀 快速开始："
echo "  工作记忆：python3 -c 'from work_memory import WorkMemory; wm = WorkMemory()'"
echo "  进化引擎：python3 -c 'from evolution_engine import EvolutionEngine; e = EvolutionEngine(); e.enable()'"
echo ""
echo "💡 提示：pip 命令使用：$PIP_CMD"
echo ""
