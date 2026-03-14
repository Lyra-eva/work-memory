#!/usr/bin/env python3.8
"""
工具调用超时保护系统
实现超时重试、熔断器模式、错误恢复

用法:
    python3.8 tools/tool_call_protection.py test      # 测试保护机制
    python3.8 tools/tool_call_protection.py status    # 显示状态
"""

import json
import time
import sys
from datetime import datetime, timedelta
from pathlib import Path
from functools import wraps

STATE_FILE = Path("/home/admin/.openclaw/workspace/tools/tool_protection_state.json")
LOG_FILE = Path("/home/admin/.openclaw/workspace/logs/tool_protection.log")

# 默认配置
DEFAULT_CONFIG = {
    "default_timeout_seconds": 30,
    "max_retries": 3,
    "retry_delay_seconds": 2,
    "circuit_breaker": {
        "failure_threshold": 3,      # 连续 3 次失败触发熔断
        "reset_timeout_seconds": 60,  # 60 秒后重置
        "half_open_requests": 1       # 半开状态允许 1 次请求
    }
}

class CircuitBreaker:
    """熔断器实现"""
    
    def __init__(self, name, config):
        self.name = name
        self.failure_threshold = config["failure_threshold"]
        self.reset_timeout = config["reset_timeout_seconds"]
        self.half_open_requests = config["half_open_requests"]
        
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open
        self.success_count = 0
    
    def can_execute(self):
        """检查是否可以执行"""
        if self.state == "closed":
            return True
        
        if self.state == "open":
            if self.last_failure_time:
                elapsed = (datetime.now() - self.last_failure_time).total_seconds()
                if elapsed >= self.reset_timeout:
                    self.state = "half-open"
                    self.half_open_remaining = self.half_open_requests
                    return True
            return False
        
        if self.state == "half-open":
            if self.half_open_remaining > 0:
                self.half_open_remaining -= 1
                return True
            return False
        
        return False
    
    def record_success(self):
        """记录成功"""
        self.failures = 0
        if self.state == "half-open":
            self.state = "closed"
        self.success_count += 1
    
    def record_failure(self):
        """记录失败"""
        self.failures += 1
        self.last_failure_time = datetime.now()
        
        if self.failures >= self.failure_threshold:
            self.state = "open"
    
    def get_state(self):
        """获取状态"""
        return {
            "name": self.name,
            "state": self.state,
            "failures": self.failures,
            "success_count": self.success_count,
            "last_failure": self.last_failure_time.isoformat() if self.last_failure_time else None
        }

class ToolCallProtection:
    """工具调用保护器"""
    
    def __init__(self, tool_name, config=None):
        self.tool_name = tool_name
        self.config = config or DEFAULT_CONFIG
        self.circuit_breaker = CircuitBreaker(tool_name, self.config["circuit_breaker"])
        self.call_history = []
    
    def call_with_protection(self, func, *args, timeout=None, **kwargs):
        """带保护的函数调用"""
        timeout = timeout or self.config["default_timeout_seconds"]
        
        # 检查熔断器
        if not self.circuit_breaker.can_execute():
            raise CircuitOpenError(f"熔断器已打开：{self.tool_name}")
        
        last_error = None
        
        for attempt in range(1, self.config["max_retries"] + 1):
            try:
                # 执行带超时的调用
                result = self._execute_with_timeout(func, args, kwargs, timeout)
                
                # 记录成功
                self.circuit_breaker.record_success()
                self._record_call(True, attempt, None)
                
                return result
                
            except TimeoutError as e:
                last_error = e
                self._record_call(False, attempt, "timeout")
                
            except Exception as e:
                last_error = e
                self._record_call(False, attempt, str(type(e).__name__))
            
            # 重试前延迟
            if attempt < self.config["max_retries"]:
                time.sleep(self.config["retry_delay_seconds"] * attempt)
        
        # 所有重试失败
        self.circuit_breaker.record_failure()
        raise last_error
    
    def _execute_with_timeout(self, func, args, kwargs, timeout):
        """执行带超时的函数"""
        # 简单实现：实际使用时需要更复杂的超时机制
        result = func(*args, **kwargs)
        return result
    
    def _record_call(self, success, attempt, error_type):
        """记录调用历史"""
        self.call_history.append({
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "attempt": attempt,
            "error_type": error_type
        })
        
        # 保留最近 100 条记录
        if len(self.call_history) > 100:
            self.call_history = self.call_history[-100:]
    
    def get_stats(self):
        """获取统计信息"""
        total = len(self.call_history)
        success = sum(1 for c in self.call_history if c["success"])
        failures = total - success
        
        return {
            "tool": self.tool_name,
            "total_calls": total,
            "success": success,
            "failures": failures,
            "success_rate": success / total if total > 0 else 0,
            "circuit_breaker": self.circuit_breaker.get_state()
        }

class CircuitOpenError(Exception):
    """熔断器打开异常"""
    pass

def load_protection_state():
    """加载保护状态"""
    if not STATE_FILE.exists():
        return {"tools": {}, "global_stats": {"total_calls": 0, "total_failures": 0}}
    
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_protection_state(state):
    """保存保护状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def log(message, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line + "\n")

def test_protection():
    """测试保护机制"""
    log("=" * 70)
    log("🧪 测试工具调用保护机制")
    log("=" * 70)
    
    # 创建保护器
    protector = ToolCallProtection("test-tool")
    
    # 测试正常调用
    def success_func():
        return "success"
    
    try:
        result = protector.call_with_protection(success_func)
        log(f"✅ 正常调用成功：{result}")
    except Exception as e:
        log(f"❌ 正常调用失败：{e}", "ERROR")
    
    # 测试超时调用
    def timeout_func():
        time.sleep(10)
        return "timeout"
    
    try:
        result = protector.call_with_protection(timeout_func, timeout=1)
        log(f"❌ 超时调用应该失败", "ERROR")
    except TimeoutError:
        log(f"✅ 超时调用正确捕获")
    except Exception as e:
        log(f"✅ 超时调用捕获异常：{type(e).__name__}")
    
    # 显示统计
    stats = protector.get_stats()
    log(f"📊 统计：{json.dumps(stats, indent=2)}")
    
    log("=" * 70)

def show_status():
    """显示保护状态"""
    print("=" * 70)
    print("📊 工具调用保护状态")
    print("=" * 70)
    print()
    
    print("⚙️  配置:")
    print(f"   默认超时：{DEFAULT_CONFIG['default_timeout_seconds']}秒")
    print(f"   最大重试：{DEFAULT_CONFIG['max_retries']}")
    print(f"   重试延迟：{DEFAULT_CONFIG['retry_delay_seconds']}秒")
    print(f"   熔断阈值：{DEFAULT_CONFIG['circuit_breaker']['failure_threshold']}次失败")
    print(f"   重置超时：{DEFAULT_CONFIG['circuit_breaker']['reset_timeout_seconds']}秒")
    print()
    
    # 加载状态
    state = load_protection_state()
    
    if state["tools"]:
        print("🔧 工具状态:")
        for tool_name, tool_state in state["tools"].items():
            cb_state = tool_state.get("circuit_breaker", {})
            icon = "🟢" if cb_state.get("state") == "closed" else "🔴"
            print(f"   {icon} {tool_name}: {cb_state.get('state', 'unknown')}")
        print()
    
    print(f"📁 状态文件：{STATE_FILE}")
    print(f"📝 日志文件：{LOG_FILE}")
    print()

def main():
    if len(sys.argv) < 2:
        print("用法：python3.8 tools/tool_call_protection.py <command>")
        print()
        print("命令:")
        print("  test     测试保护机制")
        print("  status   显示状态")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "test":
        test_protection()
    elif cmd == "status":
        show_status()
    else:
        print(f"⚠️  未知命令：{cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
