# 进化引擎 v3.5.1

个体认知增强系统 - 知识图谱 + 记忆巩固 + 记忆关联

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/Lyra-eva/work-memory.git
cd work-memory

# 切换到进化引擎分支
git checkout release/v3.5.1

# 进入目录
cd evolution
```

## 🔧 依赖

- Python 3.6+
- SQLite3 (Python 内置)

## 📚 核心模块

| 模块 | 功能 |
|------|------|
| `knowledge_graph.py` | 知识图谱管理 |
| `concept_extractor.py` | 概念提取器 |
| `memory_consolidation.py` | 记忆巩固 |
| `memory_linking.py` | 记忆关联 |
| `exceptions.py` | 异常处理 |

## 🚀 快速开始

```python
from core.knowledge_graph import KnowledgeGraph, create_node

# 初始化知识图谱
kg = KnowledgeGraph()

# 创建节点
node = create_node("Python", "skill", "Python 编程能力", mastery=0.5)
kg.add_node(node)

# 查询
print(f"节点数：{len(kg.nodes)}")
```

## 📖 使用文档

详见：https://github.com/Lyra-eva/work-memory/wiki

## 📝 版本

- **版本**: v3.5.1
- **日期**: 2026-03-15
- **状态**: 生产就绪

## 📄 许可证

MIT License
