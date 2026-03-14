#!/usr/bin/env python3
"""
健康监控器 - 统一健康检查接口
"""

class HealthMonitor:
    """统一健康监控"""
    
    def __init__(self):
        self.health_checks = {}
    
    def register_check(self, name, check_func):
        """注册健康检查"""
        self.health_checks[name] = check_func
    
    def check_all(self):
        """检查所有系统"""
        results = {}
        for name, check in self.health_checks.items():
            try:
                results[name] = check()
            except Exception as e:
                results[name] = {'status': 'error', 'message': str(e)}
        return results
    
    def get_status(self):
        """获取整体状态"""
        results = self.check_all()
        all_healthy = all(r.get('status') == 'healthy' for r in results.values())
        return {
            'overall': 'healthy' if all_healthy else 'unhealthy',
            'systems': results
        }
