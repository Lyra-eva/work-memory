#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ 邮箱配置测试脚本

测试 QQ 邮箱配置是否正确
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def test_qq_email_config():
    """测试 QQ 邮箱配置"""
    print("=" * 60)
    print("📧 QQ 邮箱配置测试")
    print("=" * 60)
    
    # 1. 检查环境变量
    print("\n[1] 检查环境变量")
    qq_email = os.getenv('QQ_EMAIL_ADDRESS')
    auth_code = os.getenv('QQ_EMAIL_AUTH_CODE')
    
    if not qq_email:
        print("   ❌ QQ_EMAIL_ADDRESS 未设置")
        print("      请设置：export QQ_EMAIL_ADDRESS='your_qq@qq.com'")
        return False
    else:
        print(f"   ✅ QQ 邮箱：{qq_email}")
    
    if not auth_code:
        print("   ❌ QQ_EMAIL_AUTH_CODE 未设置")
        print("      请设置：export QQ_EMAIL_AUTH_CODE='your_auth_code'")
        return False
    else:
        print(f"   ✅ 授权码：{'*' * len(auth_code)}")
    
    # 2. 测试 SMTP 连接
    print("\n[2] 测试 SMTP 连接")
    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=10)
        print("   ✅ SMTP 服务器连接成功 (smtp.qq.com:465)")
        
        server.login(qq_email, auth_code)
        print("   ✅ 登录成功")
        
        server.quit()
        print("   ✅ 连接已关闭")
        
    except smtplib.SMTPAuthenticationError:
        print("   ❌ 认证失败：授权码错误")
        return False
    except Exception as e:
        print(f"   ❌ 连接失败：{e}")
        return False
    
    # 3. 发送测试邮件（可选）
    print("\n[3] 发送测试邮件（可选）")
    test_email = input("   输入接收测试邮件的邮箱地址（留空跳过）: ").strip()
    
    if test_email:
        try:
            msg = MIMEText('这是一封测试邮件，用于验证 QQ 邮箱配置。', 'plain', 'utf-8')
            msg['From'] = Header(f"QQ 邮箱测试 <{qq_email}>")
            msg['To'] = Header(f"测试用户 <{test_email}>")
            msg['Subject'] = Header('QQ 邮箱配置测试', 'utf-8')
            
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login(qq_email, auth_code)
            server.sendmail(qq_email, [test_email], msg.as_string())
            server.quit()
            
            print(f"   ✅ 测试邮件已发送到：{test_email}")
            
        except Exception as e:
            print(f"   ❌ 发送失败：{e}")
    
    print("\n" + "=" * 60)
    print("✅ QQ 邮箱配置测试完成！")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_qq_email_config()
    sys.exit(0 if success else 1)
