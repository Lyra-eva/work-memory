# 工作记忆系统 (Work Memory)

🧠 为 AI Agent 设计的短期上下文缓存与记忆管理系统

## ✨ 特性

- **短期记忆缓存**：高效的会话上下文管理
- **关系图谱**：自动构建记忆关联网络
- **OpenClaw 集成**：原生支持 OpenClaw 技能系统
- **轻量级**：零外部依赖，开箱即用

## 📦 安装

### 方式一：pip 安装（推荐）

```bash
pip install work-memory
```

### 方式二：源码安装

```bash
git clone https://github.com/Lyra-eva/work-memory.git
cd work-memory
pip install -e .
```

### 方式三：OpenClaw 技能安装

```bash
# 在 OpenClaw workspace 中
cd ~/.openclaw/workspace
git clone https://github.com/Lyra-eva/work-memory.git
cd work-memory
./skills/work-memory/install.sh
```

## 🚀 快速开始

### Python API

```python
from work_memory import WorkMemory

# 初始化
wm = WorkMemory()

# 创建工作记忆会话
wm.create_session("project_alpha", {
    "context": "项目开发",
    "participants": ["Alice", "Bob"],
    "goals": ["完成 MVP", "用户测试"]
})

# 读取会话
data = wm.read_session("project_alpha")
print(data)

# 添加记忆节点
wm.add_node("decision_001", {
    "type": "decision",
    "content": "选择 React 作为前端框架",
    "timestamp": "2026-03-16T10:00:00Z"
})

# 建立关系
wm.add_relation("project_alpha", "decision_001", "contains")

# 查询关联记忆
related = wm.get_related("project_alpha")
```

### OpenClaw 技能使用

安装后在对话中自然使用：

```
记住这个项目的需求是...
```

系统会自动记录到工作记忆中。

## 📁 目录结构

```
work-memory/
├── work_memory/              # 核心 Python 包
│   ├── __init__.py
│   ├── core.py               # 核心 API
│   ├── memory_graph.py       # 关系图谱
│   └── storage.py            # 存储后端
├── skills/
│   └── work-memory/          # OpenClaw 技能
│       ├── work_memory_skill.py
│       ├── work_memory_plugin.py
│       └── install.sh
├── examples/                 # 使用示例
├── pyproject.toml
├── setup.py
└── README.md
```

## 🔧 配置

```python
# 自定义存储路径
wm = WorkMemory(storage_path="./my_memory")

# 设置自动备份
wm = WorkMemory(auto_backup=True, backup_interval=3600)
```

## 📖 文档

- [快速开始指南](skills/work-memory/QUICKSTART.md)
- [集成指南](skills/work-memory/INTEGRATION_GUIDE.md)
- [架构说明](skills/work-memory/ARCHITECTURE.md)

## 🧪 测试

```bash
python -m pytest tests/
```

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交 Issue 和 Pull Request！

---

**版本**: v1.0.0  
**作者**: Lyra-eva  
**GitHub**: https://github.com/Lyra-eva/work-memory
