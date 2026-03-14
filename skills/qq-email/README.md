# QQ 邮箱配置指南

## 📧 QQ 邮箱 SMTP/IMAP 配置

### 1. 开启 QQ 邮箱 SMTP/IMAP 服务

1. 登录 QQ 邮箱网页版 (https://mail.qq.com)
2. 点击 **设置** → **账户**
3. 找到 **POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV 服务**
4. 开启 **IMAP/SMTP 服务**
5. 生成 **授权码**（重要！不是 QQ 密码）

### 2. 配置参数

```yaml
# QQ 邮箱配置
email:
  provider: qq
  smtp_server: smtp.qq.com
  smtp_port: 465  # SSL
  imap_server: imap.qq.com
  imap_port: 993   # SSL
  ssl: true
```

### 3. 环境变量配置

在 `~/.openclaw/openclaw.json` 或环境变量中添加：

```json
{
  "email": {
    "qq": {
      "address": "your_qq_number@qq.com",
      "smtp_server": "smtp.qq.com",
      "smtp_port": 465,
      "imap_server": "imap.qq.com",
      "imap_port": 993,
      "use_ssl": true,
      "auth_code": "your_auth_code_here"
    }
  }
}
```

### 4. 使用示例

```python
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# QQ 邮箱配置
qq_email = "123456789@qq.com"  # 你的 QQ 号
auth_code = "xxxxxxxxxxxxxxx"   # 授权码（不是 QQ 密码！）

# 创建邮件
msg = MIMEText('测试邮件内容', 'plain', 'utf-8')
msg['From'] = Header(f"发件人 <{qq_email}>")
msg['To'] = Header("收件人 <recipient@example.com>")
msg['Subject'] = Header('测试邮件', 'utf-8')

# 发送邮件
server = smtplib.SMTP_SSL("smtp.qq.com", 465)
server.login(qq_email, auth_code)
server.sendmail(qq_email, ["recipient@example.com"], msg.as_string())
server.quit()

print("✅ 邮件发送成功！")
```

### 5. 常见问题

#### Q: 授权码在哪里获取？
A: QQ 邮箱 → 设置 → 账户 → 开启 SMTP 服务 → 生成授权码

#### Q: 授权码忘记了怎么办？
A: 重新生成即可，旧的授权码会失效

#### Q: 发送邮件失败？
A: 检查以下几点：
- 确认已开启 SMTP 服务
- 使用授权码，不是 QQ 密码
- 端口 465（SSL）或 587（TLS）
- 检查防火墙设置

#### Q: 接收邮件失败？
A: 检查：
- IMAP 服务是否开启
- 端口 993（SSL）
- 授权码是否正确

### 6. 安全建议

- ✅ 使用授权码，不要使用 QQ 密码
- ✅ 不要在代码中硬编码授权码
- ✅ 使用环境变量或配置文件
- ✅ 定期更换授权码
- ✅ 限制授权码的访问权限

### 7. 完整配置示例

```python
# config/email_config.py
import os
from dataclasses import dataclass

@dataclass
class QQEmailConfig:
    """QQ 邮箱配置"""
    address: str = os.getenv('QQ_EMAIL_ADDRESS', '')
    auth_code: str = os.getenv('QQ_EMAIL_AUTH_CODE', '')
    smtp_server: str = 'smtp.qq.com'
    smtp_port: int = 465
    imap_server: str = 'imap.qq.com'
    imap_port: int = 993
    use_ssl: bool = True
    
    def validate(self) -> bool:
        """验证配置是否完整"""
        return bool(self.address and self.auth_code)

# 使用
config = QQEmailConfig()
if not config.validate():
    print("❌ 请配置 QQ_EMAIL_ADDRESS 和 QQ_EMAIL_AUTH_CODE")
```

### 8. 环境变量设置

```bash
# Linux/macOS
export QQ_EMAIL_ADDRESS="123456789@qq.com"
export QQ_EMAIL_AUTH_CODE="your_auth_code"

# Windows
set QQ_EMAIL_ADDRESS=123456789@qq.com
set QQ_EMAIL_AUTH_CODE=your_auth_code
```

---

## 📖 参考链接

- [QQ 邮箱帮助](https://service.mail.qq.com/)
- [SMTP 协议文档](https://tools.ietf.org/html/rfc5321)

---

**配置完成后，记得测试一下！** ✅
