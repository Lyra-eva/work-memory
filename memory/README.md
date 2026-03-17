# Memory Directory - 记忆系统数据

这个目录包含所有记忆系统的数据。

## 目录结构

```
memory/
├── work-memory/          # Work Memory 数据
│   ├── projects/         # 项目数据
│   ├── tasks/            # 任务数据
│   ├── skills/           # 技能数据
│   ├── logs/             # 日志数据
│   └── backups/          # 备份数据
├── evolution/            # Evolution Engine 数据
│   ├── events.jsonl      # 进化事件
│   ├── patterns.json     # 发现的模式
│   └── index.json        # 索引
├── cognition/            # 认知系统数据
│   ├── graph.db          # 知识图谱
│   ├── concepts/         # 概念数据
│   └── feedback/         # 反馈数据
└── stability/            # 稳定性系统数据
    ├── health/           # 健康检查
    └── metrics/          # 性能指标
```

## 数据说明

### Work Memory
- **位置**: `memory/work-memory/`
- **用途**: 项目、任务、技能、日志管理
- **工具**: `work-memory` Python 包

### Evolution Engine
- **位置**: `memory/evolution/`
- **用途**: AI 进化数据、事件记录、模式发现
- **工具**: `evolution-engine-v2` 技能

### Cognition
- **位置**: `memory/cognition/`
- **用途**: 认知系统、知识图谱、概念提取
- **工具**: 开发中

### Stability
- **位置**: `memory/stability/`
- **用途**: 系统稳定性、健康检查、性能监控
- **工具**: 开发中

## 备份

所有数据应该定期备份：

```bash
# 备份整个 memory 目录
tar -czf memory-backup-$(date +%Y%m%d_%H%M%S).tar.gz ~/.openclaw/workspace/memory/
```

## 注意事项

1. **不要手动修改** - 使用相应的工具修改数据
2. **定期备份** - 重要数据定期备份
3. **版本控制** - 配置和代码使用 Git，数据不提交

---

**最后更新**: 2026-03-17
