
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional, Union
from dataclasses import dataclass


@dataclass
class EmailConfig:
    smtp_host: str
    smtp_port: int
    username: str
    password: str
    use_tls: bool = True
    use_ssl: bool = False


class EmailService:
    def __init__(self, config: EmailConfig):
        self.config = config
        self.connection: Optional[smtplib.SMTP] = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        try:
            if self.config.use_ssl:
                self.connection = smtplib.SMTP_SSL(
                    self.config.smtp_host, self.config.smtp_port
                )
            else:
                self.connection = smtplib.SMTP(
                    self.config.smtp_host, self.config.smtp_port
                )
                if self.config.use_tls:
                    self.connection.starttls()

            self.connection.login(self.config.username, self.config.password)
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SMTP server: {e}")

    def disconnect(self):
        if self.connection:
            try:
                self.connection.quit()
            except:
                pass
            self.connection = None

    def send_email(
        self,
        to_addresses: Union[str, List[str]],
        subject: str,
        body: str,
        from_address: Optional[str] = None,
        cc_addresses: Optional[Union[str, List[str]]] = None,
        bcc_addresses: Optional[Union[str, List[str]]] = None,
        is_html: bool = False,
        attachments: Optional[List[Union[str, Path]]] = None,
    ) -> bool:
        if not self.connection:
            self.connect()

        msg = MIMEMultipart()
        msg["From"] = from_address or self.config.username
        msg["Subject"] = subject

        to_list = [to_addresses] if isinstance(to_addresses, str) else to_addresses
        msg["To"] = ", ".join(to_list)

        cc_list = []
        if cc_addresses:
            cc_list = [cc_addresses] if isinstance(cc_addresses, str) else cc_addresses
            msg["Cc"] = ", ".join(cc_list)

        bcc_list = []
        if bcc_addresses:
            bcc_list = (
                [bcc_addresses] if isinstance(bcc_addresses, str) else bcc_addresses
            )

        content_type = "html" if is_html else "plain"
        msg.attach(MIMEText(body, content_type, "utf-8"))

        if attachments:
            for attachment_path in attachments:
                self._attach_file(msg, attachment_path)

        all_recipients = to_list + cc_list + bcc_list

        try:
            self.connection.sendmail(msg["From"], all_recipients, msg.as_string())
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {e}")

    def _attach_file(self, msg: MIMEMultipart, file_path: Union[str, Path]):
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Attachment not found: {file_path}")

        with open(path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={path.name}")
        msg.attach(part)

    def send_text_email(
        self,
        to_addresses: Union[str, List[str]],
        subject: str,
        body: str,
        **kwargs,
    ) -> bool:
        return self.send_email(
            to_addresses=to_addresses,
            subject=subject,
            body=body,
            is_html=False,
            **kwargs,
        )

    def send_html_email(
        self,
        to_addresses: Union[str, List[str]],
        subject: str,
        html_body: str,
        **kwargs,
    ) -> bool:
        return self.send_email(
            to_addresses=to_addresses,
            subject=subject,
            body=html_body,
            is_html=True,
            **kwargs,
        )


# 使用示例
if __name__ == "__main__":
    config = EmailConfig(
        smtp_host="smtp.gmail.com",
        smtp_port=587,
        username="your_email@gmail.com",
        password="your_password",
        use_tls=True,
    )

    with EmailService(config) as email_service:
        # 发送文本邮件
        email_service.send_text_email(
            to_addresses="recipient@example.com",
            subject="测试邮件",
            body="这是一封测试邮件",
        )

        # 发送HTML邮件
        email_service.send_html_email(
            to_addresses=["recipient1@example.com", "recipient2@example.com"],
            subject="HTML邮件",
            html_body="<h1>标题</h1><p>这是HTML内容</p>",
        )

        # 发送带附件的邮件
        email_service.send_email(
            to_addresses="recipient@example.com",
            subject="带附件的邮件",
            body="请查看附件",
            attachments=["file1.pdf", "file2.jpg"],
        )
