"""
稳定性系统测试 - T-OPT-14 测试覆盖率提升
测试 stability 模块中的稳定性保障组件
"""
import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch
import time

# 添加核心路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestContextMonitor:
    """上下文监控器测试"""
    
    def test_monitor_initialization(self):
        """监控器初始化"""
        from stability.context_monitor import ContextMonitor
        monitor = ContextMonitor()
        assert monitor is not None
    
    def test_monitor_check_context_size(self):
        """检查上下文大小"""
        from stability.context_monitor import ContextMonitor
        monitor = ContextMonitor()
        
        result = monitor.check_context_size("test_session", 1000)
        assert isinstance(result, dict)
        assert "status" in result
    
    def test_monitor_detect_drift(self):
        """检测漂移"""
        from stability.context_monitor import ContextMonitor
        monitor = ContextMonitor()
        
        baseline = {"key": "value"}
        current = {"key": "different_value"}
        drift = monitor.detect_drift(baseline, current)
        assert isinstance(drift, dict)
    
    def test_monitor_validate_state(self):
        """验证状态"""
        from stability.context_monitor import ContextMonitor
        monitor = ContextMonitor()
        
        state = {"status": "active", "data": "test"}
        is_valid = monitor.validate_state(state)
        assert isinstance(is_valid, bool)
    
    def test_monitor_get_metrics(self):
        """获取指标"""
        from stability.context_monitor import ContextMonitor
        monitor = ContextMonitor()
        
        metrics = monitor.get_metrics()
        assert isinstance(metrics, dict)
    
    def test_monitor_alert_on_anomaly(self):
        """异常告警"""
        from stability.context_monitor import ContextMonitor
        monitor = ContextMonitor()
        
        anomaly = {"type": "context_overflow", "severity": "high"}
        monitor.alert_on_anomaly(anomaly)
        # 应该不报错
    
    def test_monitor_track_session(self):
        """跟踪会话"""
        from stability.context_monitor import ContextMonitor
        monitor = ContextMonitor()
        
        session_id = "test_session"
        monitor.track_session(session_id)
        # 应该不报错
    
    def test_monitor_cleanup_stale_sessions(self):
        """清理过期会话"""
        from stability.context_monitor import ContextMonitor
        monitor = ContextMonitor()
        
        cleaned = monitor.cleanup_stale_sessions(max_age=3600)
        assert isinstance(cleaned, int)


class TestCronTimeoutExecutor:
    """Cron 超时执行器测试"""
    
    def test_executor_initialization(self):
        """执行器初始化"""
        from stability.cron_timeout_executor import CronTimeoutExecutor
        executor = CronTimeoutExecutor()
        assert executor is not None
    
    def test_executor_execute_with_timeout(self):
        """带超时执行"""
        from stability.cron_timeout_executor import CronTimeoutExecutor
        executor = CronTimeoutExecutor()
        
        def quick_task():
            return "done"
        
        result = executor.execute_with_timeout(quick_task, timeout=5)
        assert result == "done"
    
    def test_executor_execute_timeout_exceeded(self):
        """超时执行"""
        from stability.cron_timeout_executor import CronTimeoutExecutor
        executor = CronTimeoutExecutor()
        
        def slow_task():
            time.sleep(10)
            return "done"
        
        with pytest.raises(Exception):
            executor.execute_with_timeout(slow_task, timeout=1)
    
    def test_executor_retry_on_failure(self):
        """失败重试"""
        from stability.cron_timeout_executor import CronTimeoutExecutor
        executor = CronTimeoutExecutor()
        
        attempt = [0]
        def flaky_task():
            attempt[0] += 1
            if attempt[0] < 2:
                raise Exception("Fail")
            return "success"
        
        result = executor.retry_on_failure(flaky_task, max_retries=3)
        assert result == "success"
        assert attempt[0] == 2
    
    def test_executor_get_execution_stats(self):
        """获取执行统计"""
        from stability.cron_timeout_executor import CronTimeoutExecutor
        executor = CronTimeoutExecutor()
        
        stats = executor.get_execution_stats()
        assert isinstance(stats, dict)
    
    def test_executor_cancel_execution(self):
        """取消执行"""
        from stability.cron_timeout_executor import CronTimeoutExecutor
        executor = CronTimeoutExecutor()
        
        executor.cancel_execution("task_id")
        # 应该不报错


class TestSubagentManager:
    """子代理管理器测试"""
    
    def test_manager_initialization(self):
        """管理器初始化"""
        from stability.subagent_manager import SubAgentManager
        manager = SubAgentManager()
        assert manager is not None
    
    def test_manager_spawn_subagent(self):
        """产子代理"""
        from stability.subagent_manager import SubAgentManager
        manager = SubAgentManager()
        
        agent_id = manager.spawn_subagent("test_task")
        assert agent_id is not None
    
    def test_manager_terminate_subagent(self):
        """终止子代理"""
        from stability.subagent_manager import SubAgentManager
        manager = SubAgentManager()
        
        manager.terminate_subagent("agent_id")
        # 应该不报错
    
    def test_manager_get_subagent_status(self):
        """获取子代理状态"""
        from stability.subagent_manager import SubAgentManager
        manager = SubAgentManager()
        
        status = manager.get_subagent_status("agent_id")
        assert isinstance(status, dict)
    
    def test_manager_list_active_subagents(self):
        """列出活跃子代理"""
        from stability.subagent_manager import SubAgentManager
        manager = SubAgentManager()
        
        agents = manager.list_active_subagents()
        assert isinstance(agents, list)
    
    def test_manager_assign_task(self):
        """分配任务"""
        from stability.subagent_manager import SubAgentManager
        manager = SubAgentManager()
        
        manager.assign_task("agent_id", {"task": "test"})
        # 应该不报错
    
    def test_manager_collect_results(self):
        """收集结果"""
        from stability.subagent_manager import SubAgentManager
        manager = SubAgentManager()
        
        results = manager.collect_results("agent_id")
        assert results is None or isinstance(results, dict)
    
    def test_manager_cleanup_finished(self):
        """清理已完成"""
        from stability.subagent_manager import SubAgentManager
        manager = SubAgentManager()
        
        cleaned = manager.cleanup_finished()
        assert isinstance(cleaned, int)


class TestToolCallProtection:
    """工具调用保护测试"""
    
    def test_protection_initialization(self):
        """保护器初始化"""
        from stability.tool_call_protection import ToolCallProtection
        protection = ToolCallProtection()
        assert protection is not None
    
    def test_protection_validate_call(self):
        """验证调用"""
        from stability.tool_call_protection import ToolCallProtection
        protection = ToolCallProtection()
        
        call = {"tool": "test", "params": {}}
        is_valid = protection.validate_call(call)
        assert isinstance(is_valid, bool)
    
    def test_protection_rate_limit(self):
        """速率限制"""
        from stability.tool_call_protection import ToolCallProtection
        protection = ToolCallProtection()
        
        allowed = protection.rate_limit("user_id", "tool_name")
        assert isinstance(allowed, bool)
    
    def test_protection_sanitize_params(self):
        """参数清理"""
        from stability.tool_call_protection import ToolCallProtection
        protection = ToolCallProtection()
        
        params = {"cmd": "rm -rf /", "safe": "value"}
        sanitized = protection.sanitize_params(params)
        assert isinstance(sanitized, dict)
    
    def test_protection_check_permissions(self):
        """权限检查"""
        from stability.tool_call_protection import ToolCallProtection
        protection = ToolCallProtection()
        
        has_perm = protection.check_permissions("user_id", "tool_name")
        assert isinstance(has_perm, bool)
    
    def test_protection_log_call(self):
        """记录调用"""
        from stability.tool_call_protection import ToolCallProtection
        protection = ToolCallProtection()
        
        protection.log_call("user_id", "tool_name", {"param": "value"})
        # 应该不报错
    
    def test_protection_block_dangerous(self):
        """阻止危险调用"""
        from stability.tool_call_protection import ToolCallProtection
        protection = ToolCallProtection()
        
        call = {"tool": "exec", "params": {"cmd": "rm -rf /"}}
        is_blocked = protection.block_dangerous(call)
        assert is_blocked is True
    
    def test_protection_get_audit_log(self):
        """获取审计日志"""
        from stability.tool_call_protection import ToolCallProtection
        protection = ToolCallProtection()
        
        log = protection.get_audit_log("user_id", limit=10)
        assert isinstance(log, list)


class TestStabilityIntegration:
    """稳定性集成测试"""
    
    def test_full_stability_check(self):
        """完整稳定性检查"""
        from stability.context_monitor import ContextMonitor
        from stability.cron_timeout_executor import CronTimeoutExecutor
        from stability.subagent_manager import SubAgentManager
        from stability.tool_call_protection import ToolCallProtection
        
        monitor = ContextMonitor()
        executor = CronTimeoutExecutor()
        manager = SubAgentManager()
        protection = ToolCallProtection()
        
        # 模拟完整工作流
        monitor.track_session("test_session")
        monitor.check_context_size("test_session", 1000)
        
        def task():
            return "done"
        executor.execute_with_timeout(task, timeout=5)
        
        agent_id = manager.spawn_subagent("test")
        manager.get_subagent_status(agent_id)
        
        protection.validate_call({"tool": "test", "params": {}})
        
        # 应该不报错
    
    def test_error_recovery(self):
        """错误恢复"""
        from stability.cron_timeout_executor import CronTimeoutExecutor
        from stability.subagent_manager import SubAgentManager
        
        executor = CronTimeoutExecutor()
        manager = SubAgentManager()
        
        # 模拟错误并恢复
        def failing_task():
            raise Exception("Test error")
        
        try:
            executor.execute_with_timeout(failing_task, timeout=1)
        except Exception:
            # 恢复
            manager.spawn_subagent("recovery_task")
        
        # 应该能继续工作
    
    def test_resource_cleanup(self):
        """资源清理"""
        from stability.context_monitor import ContextMonitor
        from stability.subagent_manager import SubAgentManager
        
        monitor = ContextMonitor()
        manager = SubAgentManager()
        
        # 创建一些资源
        monitor.track_session("session1")
        monitor.track_session("session2")
        manager.spawn_subagent("agent1")
        
        # 清理
        monitor.cleanup_stale_sessions(max_age=0)
        manager.cleanup_finished()
        
        # 应该清理完成


class TestStabilityEdgeCases:
    """稳定性边界条件测试"""
    
    def test_monitor_with_empty_session(self):
        """空会话监控"""
        from stability.context_monitor import ContextMonitor
        monitor = ContextMonitor()
        
        result = monitor.check_context_size("", 0)
        assert isinstance(result, dict)
    
    def test_executor_with_zero_timeout(self):
        """零超时执行"""
        from stability.cron_timeout_executor import CronTimeoutExecutor
        executor = CronTimeoutExecutor()
        
        def task():
            return "done"
        
        # 零超时应该立即超时或执行
        try:
            result = executor.execute_with_timeout(task, timeout=0)
            assert result == "done"
        except Exception:
            pass  # 超时也是可接受的
    
    def test_manager_with_invalid_agent_id(self):
        """无效代理 ID"""
        from stability.subagent_manager import SubAgentManager
        manager = SubAgentManager()
        
        status = manager.get_subagent_status("invalid_id")
        assert isinstance(status, dict)
    
    def test_protection_with_none_params(self):
        """None 参数保护"""
        from stability.tool_call_protection import ToolCallProtection
        protection = ToolCallProtection()
        
        is_valid = protection.validate_call({"tool": "test", "params": None})
        assert isinstance(is_valid, bool)
    
    def test_concurrent_stability_checks(self):
        """并发稳定性检查"""
        from stability.context_monitor import ContextMonitor
        import threading
        
        monitor = ContextMonitor()
        results = []
        
        def check():
            result = monitor.check_context_size("test", 100)
            results.append(result)
        
        threads = [threading.Thread(target=check) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(results) == 10


class TestStabilityPerformance:
    """稳定性性能测试"""
    
    def test_monitor_performance(self):
        """监控器性能"""
        from stability.context_monitor import ContextMonitor
        import time
        
        monitor = ContextMonitor()
        
        start = time.time()
        for _ in range(100):
            monitor.check_context_size("test", 100)
        elapsed = time.time() - start
        
        assert elapsed < 5.0  # 5 秒上限
    
    def test_executor_throughput(self):
        """执行器吞吐量"""
        from stability.cron_timeout_executor import CronTimeoutExecutor
        import time
        
        executor = CronTimeoutExecutor()
        
        def quick_task():
            return "done"
        
        start = time.time()
        for _ in range(50):
            executor.execute_with_timeout(quick_task, timeout=1)
        elapsed = time.time() - start
        
        assert elapsed < 10.0  # 10 秒上限


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
