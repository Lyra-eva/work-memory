---
name: qq-email
description: QQ 邮箱配置和使用指南。支持 SMTP 发送和 IMAP 接收邮件。
author: OpenClaw Community
version: 1.0.0
metadata:
  {
    "openclaw":
      {
        "config": {
          "env": {
            "QQ_EMAIL_ADDRESS": {
              "description": "QQ 邮箱地址（如：123456789@qq.com）",
              "required": true
            },
            "QQ_EMAIL_AUTH_CODE": {
              "description": "QQ 邮箱授权码（在 QQ 邮箱设置中获取）",
              "required": true
            }
          }
        }
      }
  }
---

# QQ 邮箱技能

使用 QQ 邮箱发送和接收邮件。

## 配置步骤

### 1. 获取授权码

1. 登录 QQ 邮箱网页版 (https://mail.qq.com)
2. 点击 **设置** → **账户**
3. 开启 **IMAP/SMTP 服务**
4. 生成 **授权码**（重要！不是 QQ 密码）

### 2. 设置环境变量

```bash
export QQ_EMAIL_ADDRESS="your_qq_number@qq.com"
export QQ_EMAIL_AUTH_CODE="your_auth_code"
```

### 3. 或在 openclaw.json 中配置

```json
{
  "env": {
    "QQ_EMAIL_ADDRESS": "123456789@qq.com",
    "QQ_EMAIL_AUTH_CODE": "your_auth_code"
  }
}
```

## 使用示例

### 发送邮件

```python
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 获取配置
qq_email = os.getenv('QQ_EMAIL_ADDRESS')
auth_code = os.getenv('QQ_EMAIL_AUTH_CODE')

# 创建邮件
msg = MIMEText('邮件内容', 'plain', 'utf-8')
msg['From'] = Header(f"发件人 <{qq_email}>")
msg['To'] = Header("收件人 <recipient@example.com>")
msg['Subject'] = Header('邮件主题', 'utf-8')

# 发送
server = smtplib.SMTP_SSL("smtp.qq.com", 465)
server.login(qq_email, auth_code)
server.sendmail(qq_email, ["recipient@example.com"], msg.as_string())
server.quit()
```

### 接收邮件

```python
import os
import imaplib
import email

# 获取配置
qq_email = os.getenv('QQ_EMAIL_ADDRESS')
auth_code = os.getenv('QQ_EMAIL_AUTH_CODE')

# 连接 IMAP
mail = imaplib.IMAP4_SSL("imap.qq.com", 993)
mail.login(qq_email, auth_code)
mail.select("INBOX")

# 搜索邮件
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()

# 获取最新邮件
if email_ids:
    latest = email_ids[-1]
    status, msg_data = mail.fetch(latest, "(RFC822)")
    email_msg = email.message_from_bytes(msg_data[0][1])
    
    print("主题:", email_msg['Subject'])
    print("发件人:", email_msg['From'])
    print("内容:", email_msg.get_payload())

mail.close()
mail.logout()
```

## 配置参数

| 参数 | 值 | 说明 |
|------|-----|------|
| SMTP 服务器 | smtp.qq.com | 发送邮件 |
| SMTP 端口 | 465 | SSL 加密 |
| IMAP 服务器 | imap.qq.com | 接收邮件 |
| IMAP 端口 | 993 | SSL 加密 |
| 授权码 | (在邮箱设置中获取) | 不是 QQ 密码！ |

## 常见问题

**Q: 授权码在哪里获取？**  
A: QQ 邮箱 → 设置 → 账户 → 开启 SMTP 服务 → 生成授权码

**Q: 发送失败？**  
A: 检查授权码是否正确，确认已开启 SMTP 服务

**Q: 如何测试配置？**  
A: 运行 `python3 test_email.py` 测试发送功能

## 安全提示

- ⚠️ 不要使用 QQ 密码，使用授权码
- ⚠️ 不要在代码中硬编码授权码
- ⚠️ 使用环境变量或配置文件
- ⚠️ 定期更换授权码

---

**配置完成后记得测试！** ✅
