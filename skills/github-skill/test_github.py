#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Skill - 测试脚本
"""

import subprocess
import os

def test_git_installed():
    """测试 git 是否安装"""
    print("\n[1] 测试 Git 安装")
    try:
        result = subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        print(f"   ✅ Git 已安装：{result.stdout.strip()}")
        return True
    except Exception as e:
        print(f"   ❌ Git 未安装：{e}")
        return False

def test_github_token():
    """测试 GitHub Token"""
    print("\n[2] 测试 GitHub Token")
    token = os.getenv('GITHUB_TOKEN')
    
    if not token:
        print("   ⚠️  GITHUB_TOKEN 未设置")
        print("      请设置：export GITHUB_TOKEN='your_token'")
        return False
    
    # 测试 token
    import requests
    headers = {'Authorization': f'token {token}'}
    
    try:
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            user = response.json()
            print(f"   ✅ Token 有效")
            print(f"      用户：{user.get('login', 'unknown')}")
            return True
        else:
            print(f"   ❌ Token 无效：{response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ 测试失败：{e}")
        return False

def test_git_clone():
    """测试 Git 克隆"""
    print("\n[3] 测试 Git 克隆")
    import tempfile
    import shutil
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_repo = 'https://github.com/openclaw/openclaw'
        target_dir = os.path.join(tmpdir, 'openclaw')
        
        try:
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', test_repo, target_dir],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"   ✅ 克隆成功")
                return True
            else:
                print(f"   ❌ 克隆失败：{result.stderr}")
                return False
        except Exception as e:
            print(f"   ❌ 测试失败：{e}")
            return False

def main():
    """运行所有测试"""
    print("=" * 60)
    print("🐙 GitHub Skill - 安装验证测试")
    print("=" * 60)
    
    tests = [
        test_git_installed,
        test_github_token,
        test_git_clone,
    ]
    
    passed = 0
    failed = 0
    skipped = 0
    
    for test in tests:
        try:
            result = test()
            if result:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"   ❌ 测试异常：{e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("=" * 60)
    
    if failed == 0:
        print("\n✅ 所有测试通过！")
        return 0
    else:
        print(f"\n⚠️ {failed} 个测试失败")
        print("\n📋 配置指南:")
        print("   1. 访问 https://github.com/settings/tokens")
        print("   2. 生成新 token (选择 repo 权限)")
        print("   3. 设置环境变量：export GITHUB_TOKEN='your_token'")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
