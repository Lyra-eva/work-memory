# 工作记忆系统 v1.0

工作记忆管理 - 短期上下文缓存系统

## 📦 安装

```bash
git clone https://github.com/Lyra-eva/work-memory.git
cd work-memory
git checkout release/v1.0
cd work-memory-project
```

## 🚀 快速开始

```python
from work_memory import WorkMemory

# 初始化
wm = WorkMemory()

# 创建工作记忆
wm.create_session("test", {"key": "value"})

# 读取
data = wm.read_session("test")
```

## 📄 许可证

MIT License
