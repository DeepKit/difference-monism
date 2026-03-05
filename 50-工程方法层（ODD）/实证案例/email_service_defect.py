
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Union
from pathlib import Path
from dataclasses import dataclass


@dataclass
class EmailConfig:
    """SMTP服务器配置"""
    smtp_server: str
    smtp_port: int
    username: str
    password: str
    use_tls: bool = True
    use_ssl: bool = False
    timeout: int = 30


class EmailService:
    """邮件发送服务"""
    
    def __init__(self, config: EmailConfig):
        self.config = config
        
    def send_email(
        self,
        to_addresses: Union[str, List[str]],
        subject: str,
        body: str,
        from_address: Optional[str] = None,
        cc_addresses: Optional[Union[str, List[str]]] = None,
        bcc_addresses: Optional[Union[str, List[str]]] = None,
        html: bool = False,
        attachments: Optional[List[Union[str, Path]]] = None,
        reply_to: Optional[str] = None
    ) -> bool:
        """
        发送邮件
        
        Args:
            to_addresses: 收件人地址
            subject: 邮件主题
            body: 邮件正文
            from_address: 发件人地址（默认使用配置中的username）
            cc_addresses: 抄送地址
            bcc_addresses: 密送地址
            html: 是否为HTML格式
            attachments: 附件路径列表
            reply_to: 回复地址
            
        Returns:
            发送是否成功
        """
        try:
            # 创建邮件对象
            message = MIMEMultipart()
            message['From'] = from_address or self.config.username
            message['Subject'] = subject
            
            # 处理收件人
            to_list = self._normalize_addresses(to_addresses)
            message['To'] = ', '.join(to_list)
            
            # 处理抄送
            cc_list = []
            if cc_addresses:
                cc_list = self._normalize_addresses(cc_addresses)
                message['Cc'] = ', '.join(cc_list)
            
            # 处理密送
            bcc_list = []
            if bcc_addresses:
                bcc_list = self._normalize_addresses(bcc_addresses)
            
            # 设置回复地址
            if reply_to:
                message['Reply-To'] = reply_to
            
            # 添加邮件正文
            content_type = 'html' if html else 'plain'
            message.attach(MIMEText(body, content_type, 'utf-8'))
            
            # 添加附件
            if attachments:
                self._attach_files(message, attachments)
            
            # 所有收件人列表
            all_recipients = to_list + cc_list + bcc_list
            
            # 发送邮件
            self._send_message(message, all_recipients)
            
            return True
            
        except Exception as e:
            raise EmailSendError(f"邮件发送失败: {str(e)}") from e
    
    def _normalize_addresses(self, addresses: Union[str, List[str]]) -> List[str]:
        """标准化邮件地址"""
        if isinstance(addresses, str):
            return [addr.strip() for addr in addresses.split(',')]
        return [addr.strip() for addr in addresses]
    
    def _attach_files(self, message: MIMEMultipart, attachments: List[Union[str, Path]]):
        """添加附件"""
        for attachment_path in attachments:
            path = Path(attachment_path)
            
            if not path.exists():
                raise FileNotFoundError(f"附件不存在: {attachment_path}")
            
            with open(path, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {path.name}'
            )
            message.attach(part)
    
    def _send_message(self, message: MIMEMultipart, recipients: List[str]):
        """发送邮件消息"""
        if self.config.use_ssl:
            # 使用SSL连接
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                self.config.smtp_server,
                self.config.smtp_port,
                context=context,
                timeout=self.config.timeout
            ) as server:
                server.login(self.config.username, self.config.password)
                server.send_message(message, to_addrs=recipients)
        else:
            # 使用TLS连接
            with smtplib.SMTP(
                self.config.smtp_server,
                self.config.smtp_port,
                timeout=self.config.timeout
            ) as server:
                if self.config.use_tls:
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                server.login(self.config.username, self.config.password)
                server.send_message(message, to_addrs=recipients)
    
    def send_bulk_emails(
        self,
        emails: List[dict],
        from_address: Optional[str] = None
    ) -> dict:
        """
        批量发送邮件
        
        Args:
            emails: 邮件列表，每个元素为包含邮件参数的字典
            from_address: 统一发件人地址
            
        Returns:
            发送结果统计
        """
        results = {
            'success': 0,
            'failed': 0,
            'errors': []
        }
        
        for idx, email_data in enumerate(emails):
            try:
                if from_address:
                    email_data['from_address'] = from_address
                self.send_email(**email_data)
                results['success'] += 1
            except Exception as e:
                results['failed'] += 1
                results['errors'].append({
                    'index': idx,
                    'email': email_data.get('to_addresses'),
                    'error': str(e)
                })
        
        return results


class EmailSendError(Exception):
    """邮件发送异常"""
    pass


# 使用示例
if __name__ == '__main__':
    # 配置SMTP服务器
    config = EmailConfig(
        smtp_server='smtp.gmail.com',
        smtp_port=587,
        username='your_email@gmail.com',
        password='your_password',
        use_tls=True
    )
    
    # 创建邮件服务
    email_service = EmailService(config)
    
    # 发送简单文本邮件
    email_service.send_email(
        to_addresses='recipient@example.com',
        subject='测试邮件',
        body='这是一封测试邮件'
    )
    
    # 发送HTML邮件带附件
    email_service.send_email(
        to_addresses=['user1@example.com', 'user2@example.com'],
        subject='HTML邮件',
        body='<h1>标题</h1><p>这是HTML内容</p>',
        html=True,
        cc_addresses='cc@example.com',
        attachments=['document.pdf', 'image.png']
    )
    
    # 批量发送
    bulk_emails = [
        {
            'to_addresses': 'user1@example.com',
            'subject': '邮件1',
            'body': '内容1'
        },
        {
            'to_addresses': 'user2@example.com',
            'subject': '邮件2',
            'body': '内容2'
        }
    ]
    results = email_service.send_bulk_emails(bulk_emails)
    print(f"成功: {results['success']}, 失败: {results['failed']}")
