import smtplib
import queue
import threading
import time
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class Email:
    """邮件数据类"""
    to: List[str]
    subject: str
    body: str
    from_addr: str
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    attachments: Optional[List[str]] = None
    html: bool = False
    retry_count: int = 0
    max_retries: int = 3
    priority: int = 5  # 1-10, 数字越小优先级越高
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def __lt__(self, other):
        """用于优先级队列排序"""
        return self.priority < other.priority


class EmailQueue:
    """线程安全的邮件队列类"""
    
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        use_tls: bool = True,
        max_workers: int = 3,
        retry_delay: int = 60,
        log_level: int = logging.INFO
    ):
        """
        初始化邮件队列
        
        Args:
            smtp_host: SMTP服务器地址
            smtp_port: SMTP端口
            username: 邮箱用户名
            password: 邮箱密码
            use_tls: 是否使用TLS
            max_workers: 最大工作线程数
            retry_delay: 重试延迟(秒)
            log_level: 日志级别
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.max_workers = max_workers
        self.retry_delay = retry_delay
        
        # 使用优先级队列
        self.email_queue = queue.PriorityQueue()
        self.failed_queue = queue.Queue()
        
        # 线程控制
        self.workers = []
        self.running = False
        self.lock = threading.Lock()
        
        # 统计信息
        self.stats = {
            'sent': 0,
            'failed': 0,
            'pending': 0,
            'retrying': 0
        }
        
        # 配置日志
        self._setup_logging(log_level)
        
    def _setup_logging(self, log_level: int):
        """配置日志"""
        self.logger = logging.getLogger('EmailQueue')
        self.logger.setLevel(log_level)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def add_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        from_addr: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None,
        html: bool = False,
        priority: int = 5
    ) -> bool:
        """
        添加邮件到队列
        
        Args:
            to: 收件人列表
            subject: 邮件主题
            body: 邮件正文
            from_addr: 发件人地址
            cc: 抄送列表
            bcc: 密送列表
            attachments: 附件路径列表
            html: 是否为HTML格式
            priority: 优先级(1-10)
            
        Returns:
            bool: 是否成功添加
        """
        try:
            if not to or not subject or not body:
                raise ValueError("收件人、主题和正文不能为空")
            
            email = Email(
                to=to,
                subject=subject,
                body=body,
                from_addr=from_addr or self.username,
                cc=cc,
                bcc=bcc,
                attachments=attachments,
                html=html,
                priority=priority
            )
            
            self.email_queue.put((priority, email))
            
            with self.lock:
                self.stats['pending'] += 1
            
            self.logger.info(f"邮件已加入队列: {subject} -> {', '.join(to)}")
            return True
            
        except Exception as e:
            self.logger.error(f"添加邮件失败: {str(e)}")
            return False
    
    def _create_message(self, email: Email) -> MIMEMultipart:
        """创建邮件消息对象"""
        msg = MIMEMultipart()
        msg['From'] = email.from_addr
        msg['To'] = ', '.join(email.to)
        msg['Subject'] = email.subject
        
        if email.cc:
            msg['Cc'] = ', '.join(email.cc)
        
        # 添加正文
        mime_type = 'html' if email.html else 'plain'
        msg.attach(MIMEText(email.body, mime_type, 'utf-8'))
        
        # 添加附件
        if email.attachments:
            for filepath in email.attachments:
                try:
                    with open(filepath, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename={filepath.split("/")[-1]}'
                        )
                        msg.attach(part)
                except Exception as e:
                    self.logger.warning(f"附件添加失败 {filepath}: {str(e)}")
        
        return msg
    
    def _send_email(self, email: Email) -> bool:
        """
        发送单封邮件
        
        Args:
            email: 邮件对象
            
        Returns:
            bool: 是否发送成功
        """
        try:
            msg = self._create_message(email)
            
            # 获取所有收件人
            recipients = email.to.copy()
            if email.cc:
                recipients.extend(email.cc)
            if email.bcc:
                recipients.extend(email.bcc)
            
            # 连接SMTP服务器
            if self.use_tls:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            
            server.login(self.username, self.password)
            server.send_message(msg, email.from_addr, recipients)
            server.quit()
            
            with self.lock:
                self.stats['sent'] += 1
                self.stats['pending'] -= 1
            
            self.logger.info(f"邮件发送成功: {email.subject}")
            return True
            
        except smtplib.SMTPException as e:
            self.logger.error(f"SMTP错误: {str(e)}")
            return False
        except Exception as e:
            self.logger.error(f"发送邮件失败: {str(e)}")
            return False
    
    def _worker(self):
        """工作线程"""
        while self.running:
            try:
                # 获取邮件，超时1秒
                priority, email = self.email_queue.get(timeout=1)
                
                # 发送邮件
                success = self._send_email(email)
                
                if not success:
                    # 发送失败，检查是否需要重试
                    email.retry_count += 1
                    
                    if email.retry_count <= email.max_retries:
                        # 重新加入队列，延迟重试
                        self.logger.info(
                            f"邮件将在{self.retry_delay}秒后重试 "
                            f"({email.retry_count}/{email.max_retries}): {email.subject}"
                        )
                        
                        with self.lock:
                            self.stats['retrying'] += 1
                        
                        threading.Timer(
                            self.retry_delay,
                            lambda: self.email_queue.put((priority, email))
                        ).start()
                    else:
                        # 超过最大重试次数，移入失败队列
                        self.failed_queue.put(email)
                        
                        with self.lock:
                            self.stats['failed'] += 1
                            self.stats['pending'] -= 1
                        
                        self.logger.error(f"邮件发送失败(已达最大重试次数): {email.subject}")
                
                self.email_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"工作线程错误: {str(e)}")
    
    def start(self):
        """启动邮件队列处理"""
        if self.running:
            self.logger.warning("邮件队列已在运行")
            return
        
        self.running = True
        
        # 启动工作线程
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)
        
        self.logger.info(f"邮件队列已启动，工作线程数: {self.max_workers}")
    
    def stop(self, wait: bool = True):
        """
        停止邮件队列处理
        
        Args:
            wait: 是否等待队列清空
        """
        if not self.running:
            self.logger.warning("邮件队列未运行")
            return
        
        self.logger.info("正在停止邮件队列...")
        
        if wait:
            self.email_queue.join()
        
        self.running = False
        
        # 等待所有工作线程结束
        for worker in self.workers:
            worker.join(timeout=5)
        
        self.workers.clear()
        self.logger.info("邮件队列已停止")
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        with self.lock:
            return {
                **self.stats,
                'queue_size': self.email_queue.qsize(),
                'failed_queue_size': self.failed_queue.qsize(),
                'running': self.running,
                'workers': len(self.workers)
            }
    
    def get_failed_emails(self) -> List[Email]:
        """获取所有失败的邮件"""
        failed = []
        while not self.failed_queue.empty():
            try:
                email = self.failed_queue.get_nowait()
                failed.append(email)
            except queue.Empty:
                break
        return failed
    
    def clear_queue(self):
        """清空队列"""
        with self.email_queue.mutex:
            self.email_queue.queue.clear()
        
        with self.lock:
            self.stats['pending'] = 0
        
        self.logger.info("队列已清空")
    
    def export_failed_emails(self, filepath: str):
        """导出失败的邮件到JSON文件"""
        failed = self.get_failed_emails()
        
        data = []
        for email in failed:
            data.append({
                'to': email.to,
                'subject': email.subject,
                'body': email.body,
                'from_addr': email.from_addr,
                'cc': email.cc,
                'bcc': email.bcc,
                'created_at': email.created_at.isoformat(),
                'retry_count': email.retry_count
            })
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"已导出{len(data)}封失败邮件到: {filepath}")


# 使用示例
if __name__ == "__main__":
    # 创建邮件队列
    queue = EmailQueue(
        smtp_host="smtp.gmail.com",
        smtp_port=587,
        username="your_email@gmail.com",
        password="your_password",
        use_tls=True,
        max_workers=3
    )
    
    # 启动队列
    queue.start()
    
    # 添加邮件
    queue.add_email(
        to=["recipient@example.com"],
        subject="测试邮件",
        body="这是一封测试邮件",
        priority=1
    )
    
    queue.add_email(
        to=["recipient2@example.com"],
        subject="HTML邮件",
        body="<h1>这是HTML邮件</h1><p>内容</p>",
        html=True,
        priority=5
    )
    
    # 等待处理完成
    time.sleep(5)
    
    # 查看统计
    print(queue.get_stats())
    
    # 停止队列
    queue.stop()