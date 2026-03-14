#!/usr/bin/env python3
"""
Context 监控器
监控会话 Context 使用率，提供告警和自动清理功能
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

SESSIONS_DIR = Path("/home/admin/.openclaw/workspace/sessions")
MONITOR_CONFIG = Path("/home/admin/.openclaw/workspace/memory/stability/context_monitor_config.json")
LOG_FILE = Path("/home/admin/.openclaw/workspace/memory/stability/context_monitor.log")

# 告警阈值配置
THRESHOLDS = {
    "warning": 0.5,      # 50% 告警
    "critical": 0.8,     # 80% 限流
    "emergency": 0.95    # 95% 强制清理
}

# Context 上限 (tokens)
MAX_CONTEXT_TOKENS = 100000


class ContextMonitor:
    """Context 监控器"""
    
    def __init__(self, max_tokens: int = MAX_CONTEXT_TOKENS):
        self.max_tokens = max_tokens
        self.sessions_dir = SESSIONS_DIR
        self.config_file = MONITOR_CONFIG
        self.log_file = LOG_FILE
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """确保目录存在"""
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def _log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {message}"
        print(log_line)
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_line + "\n")
    
    def _estimate_tokens(self, file_path: Path) -> int:
        """估算文件的 tokens 数 (1 token ≈ 4 字符)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return len(content) // 4
        except:
            return 0
    
    def get_session_info(self) -> List[Dict]:
        """获取所有会话的 Context 信息"""
        sessions = []
        
        if not self.sessions_dir.exists():
            return sessions
        
        for f in self.sessions_dir.glob("*.jsonl"):
            stat = f.stat()
            tokens = self._estimate_tokens(f)
            usage_rate = tokens / self.max_tokens
            
            sessions.append({
                "session_id": f.stem,
                "path": str(f),
                "size": stat.st_size,
                "tokens": tokens,
                "usage_rate": usage_rate,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
        
        # 按使用率排序
        sessions.sort(key=lambda s: s["usage_rate"], reverse=True)
        return sessions
    
    def check_usage(self) -> Dict:
        """检查 Context 使用率"""
        self._log("=" * 60)
        self._log("📊 Context 使用率检查")
        self._log("=" * 60)
        
        sessions = self.get_session_info()
        if not sessions:
            self._log("✅ 无会话")
            return {"status": "ok", "sessions": 0, "alert_level": None}
        
        # 统计
        total_tokens = sum(s["tokens"] for s in sessions)
        avg_usage = sum(s["usage_rate"] for s in sessions) / len(sessions)
        max_usage_session = sessions[0] if sessions else None
        
        # 告警级别
        alert_level = None
        if max_usage_session and max_usage_session["usage_rate"] >= THRESHOLDS["emergency"]:
            alert_level = "emergency"
        elif max_usage_session and max_usage_session["usage_rate"] >= THRESHOLDS["critical"]:
            alert_level = "critical"
        elif max_usage_session and max_usage_session["usage_rate"] >= THRESHOLDS["warning"]:
            alert_level = "warning"
        
        self._log(f"总会话数：{len(sessions)}")
        self._log(f"总 tokens: {total_tokens:,}")
        self._log(f"平均使用率：{avg_usage:.1%}")
        if max_usage_session:
            self._log(f"最高使用率：{max_usage_session['usage_rate']:.1%} ({max_usage_session['session_id']})")
        if alert_level:
            self._log(f"⚠️ 告警级别：{alert_level}")
        
        return {
            "status": "ok" if not alert_level else "alert",
            "sessions": len(sessions),
            "total_tokens": total_tokens,
            "avg_usage": avg_usage,
            "alert_level": alert_level,
            "max_usage_session": max_usage_session
        }
    
    def cleanup(self, keep_recent: int = 10) -> Dict:
        """清理旧会话"""
        self._log("🧹 开始清理会话")
        
        sessions = self.get_session_info()
        if len(sessions) <= keep_recent:
            self._log(f"✅ 无需清理 (当前 {len(sessions)} 个，保留 {keep_recent} 个)")
            return {"cleaned": 0}
        
        # 按修改时间排序，保留最近的
        sessions.sort(key=lambda s: s["modified"], reverse=True)
        to_delete = sessions[keep_recent:]
        
        cleaned = 0
        for session in to_delete:
            try:
                path = Path(session["path"])
                path.unlink()
                self._log(f"   ✅ 删除：{session['session_id']}")
                cleaned += 1
            except Exception as e:
                self._log(f"   ❌ 删除失败：{session['session_id']} - {e}")
        
        self._log(f"✅ 清理完成，删除 {cleaned}/{len(to_delete)} 个会话")
        return {"cleaned": cleaned}
    
    def get_status(self) -> Dict:
        """获取监控状态"""
        return {
            "max_tokens": self.max_tokens,
            "sessions_dir": str(self.sessions_dir),
            "config_file": str(self.config_file),
            "log_file": str(self.log_file),
            "thresholds": THRESHOLDS
        }
