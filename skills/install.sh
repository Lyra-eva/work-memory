#!/bin/bash
# Work Memory 一键安装/升级脚本
# 使用方式：./skills/install.sh
# 特性：支持重复安装、版本升级、数据迁移、数据保留

set -e

echo "🚀 正在安装 Work Memory..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 读取当前版本
CURRENT_VERSION=$(cat "$PROJECT_ROOT/VERSION" 2>/dev/null || echo "1.0.0")

echo -e "${BLUE}当前版本：v$CURRENT_VERSION${NC}"

# ============================================================
# 步骤 1: 检查 Python
# ============================================================
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误：未找到 Python3${NC}"
    echo "请先安装 Python3"
    exit 1
fi

# ============================================================
# 步骤 2: 检查现有安装和数据
# ============================================================
echo -e "\n${YELLOW}📦 检查安装状态...${NC}"

WM_DATA="$HOME/.openclaw/workspace/work-memory-data"
DATA_VERSION_FILE="$WM_DATA/.version"
INSTALLED_VERSION="unknown"

# 检查是否已安装
if python3 -c "import work_memory" 2>/dev/null; then
    INSTALLED_VERSION=$(python3 -c "import work_memory; print(getattr(work_memory, '__version__', 'unknown'))" 2>/dev/null || echo "unknown")
    echo -e "${CYAN}已安装版本：v$INSTALLED_VERSION${NC}"
fi

# 检查是否有数据
DATA_EXISTS=false
if [ -d "$WM_DATA" ]; then
    DATA_EXISTS=true
    echo -e "${CYAN}发现现有数据目录：$WM_DATA${NC}"
    
    # 读取数据版本
    if [ -f "$DATA_VERSION_FILE" ]; then
        DATA_VERSION=$(cat "$DATA_VERSION_FILE")
        echo -e "${CYAN}数据版本：v$DATA_VERSION${NC}"
    else
        DATA_VERSION="unknown"
        echo -e "${YELLOW}⚠️  数据版本未知${NC}"
    fi
fi

# ============================================================
# 步骤 3: 决定安装策略
# ============================================================
NEED_MIGRATION=false
BACKUP_NEEDED=false

if [ "$DATA_EXISTS" = true ]; then
    # 检查是否需要迁移
    if [ "$DATA_VERSION" != "$CURRENT_VERSION" ]; then
        NEED_MIGRATION=true
        BACKUP_NEEDED=true
        echo -e "\n${YELLOW}📊 检测到版本差异，需要数据迁移${NC}"
        echo "   从 v$DATA_VERSION → v$CURRENT_VERSION"
    else
        echo -e "\n${GREEN}✅ 数据版本与安装版本一致，无需迁移${NC}"
    fi
fi

# ============================================================
# 步骤 4: 备份现有数据（如果需要）
# ============================================================
if [ "$BACKUP_NEEDED" = true ]; then
    echo -e "\n${YELLOW}💾 备份现有数据...${NC}"
    BACKUP_DIR="$WM_DATA.backups/backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # 复制数据目录（排除 backups 目录本身）
    if [ -d "$WM_DATA" ]; then
        rsync -a --exclude='.backups' "$WM_DATA/" "$BACKUP_DIR/" 2>/dev/null || \
        cp -r "$WM_DATA" "$BACKUP_DIR" 2>/dev/null || true
        echo -e "${GREEN}✅ 数据已备份：$BACKUP_DIR${NC}"
    fi
fi

# ============================================================
# 步骤 5: 安装核心库
# ============================================================
echo -e "\n${YELLOW}📦 安装核心库...${NC}"
cd "$PROJECT_ROOT"

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

# ============================================================
# 步骤 6: 数据迁移（如果需要）
# ============================================================
if [ "$NEED_MIGRATION" = true ]; then
    echo -e "\n${YELLOW}🔄 执行数据迁移...${NC}"
    
    # 调用迁移脚本（如果存在）
    MIGRATE_SCRIPT="$PROJECT_ROOT/scripts/migrate_data.py"
    if [ -f "$MIGRATE_SCRIPT" ]; then
        echo -e "${BLUE}运行迁移脚本：$MIGRATE_SCRIPT${NC}"
        python3 "$MIGRATE_SCRIPT" "$DATA_VERSION" "$CURRENT_VERSION" || {
            echo -e "${RED}❌ 迁移失败${NC}"
            echo -e "${YELLOW}💡 可以从备份恢复：$BACKUP_DIR${NC}"
            exit 1
        }
    else
        echo -e "${BLUE}ℹ️  无迁移脚本，假设数据格式兼容${NC}"
        echo -e "${YELLOW}⚠️  如果遇到问题，请检查数据格式是否变化${NC}"
    fi
    
    # 更新数据版本文件
    echo "$CURRENT_VERSION" > "$DATA_VERSION_FILE"
    echo -e "${GREEN}✅ 数据版本已更新：v$CURRENT_VERSION${NC}"
fi

# ============================================================
# 步骤 7: 创建数据目录（如果不存在）
# ============================================================
echo -e "\n${YELLOW}📁 检查工作目录...${NC}"
if [ -d "$WM_DATA" ]; then
    echo -e "${GREEN}✅ 工作目录已存在：$WM_DATA${NC}"
    echo -e "${BLUE}💡 历史数据已保留${NC}"
else
    mkdir -p "$WM_DATA"
    echo -e "${GREEN}✅ 工作目录已创建：$WM_DATA${NC}"
    echo "$CURRENT_VERSION" > "$DATA_VERSION_FILE"
fi

# ============================================================
# 步骤 8: 验证安装
# ============================================================
echo -e "\n${YELLOW}🧪 验证安装...${NC}"
if python3 -c "from work_memory import WorkMemory" 2>/dev/null; then
    echo -e "${GREEN}✅ 工作记忆系统验证成功${NC}"
else
    echo -e "${RED}❌ 验证失败${NC}"
    exit 1
fi

# ============================================================
# 完成
# ============================================================
echo -e "\n${GREEN}=========================================="
echo "✅ Work Memory v$CURRENT_VERSION 安装完成！"
echo "==========================================${NC}"

if [ "$NEED_MIGRATION" = true ]; then
    echo -e "\n${CYAN}📊 数据迁移完成：${NC}"
    echo "   v$DATA_VERSION → v$CURRENT_VERSION"
    echo -e "   ${BLUE}备份位置：$BACKUP_DIR${NC}"
fi

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
echo "🗑️  卸载："
echo "  $SCRIPT_DIR/uninstall.sh"
echo ""
