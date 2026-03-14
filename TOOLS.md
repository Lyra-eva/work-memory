# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

---

## Work Memory

工作记忆系统配置 - 用于项目/任务/日志管理

- **数据目录**: `~/.openclaw/workspace/work-memory-data/`
- **备份目录**: `~/.openclaw/workspace/work-memory-backups/`
- **自动备份**: 每天 23:00（通过 cron）
- **默认项目**: 无（需手动指定）

### 使用方式

```python
from work_memory_plugin import WorkMemoryPlugin

plugin = WorkMemoryPlugin()
plugin.create_project("项目名称")
plugin.create_task("任务标题")
plugin.save_daily_log()
```

### 与 OpenClaw 默认记忆的分工

- **OpenClaw 默认记忆** (`memory/`): 对话历史、用户偏好、AI 进化
- **Work Memory** (`work-memory-data/`): 项目管理、任务追踪、工作日志

两者互补共存，互不影响。
