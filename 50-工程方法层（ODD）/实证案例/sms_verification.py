import random
import time
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class VerificationRecord:
    code: str
    created_at: float
    attempts: int = 0
    locked_until: Optional[float] = None
    last_sent_at: float = 0


class SMSVerification:
    CODE_LENGTH = 6
    CODE_EXPIRY = 300
    SEND_INTERVAL = 60
    MAX_ATTEMPTS = 3
    LOCK_DURATION = 1800
    
    def __init__(self):
        self.records: Dict[str, VerificationRecord] = {}
    
    def generate_code(self) -> str:
        return ''.join([str(random.randint(0, 9)) for _ in range(self.CODE_LENGTH)])
    
    def send_code(self, phone: str) -> Tuple[bool, str]:
        current_time = time.time()
        
        if phone in self.records:
            record = self.records[phone]
            
            if record.locked_until and current_time < record.locked_until:
                remaining = int(record.locked_until - current_time)
                return False, f"账号已锁定，请在{remaining}秒后重试"
            
            if current_time - record.last_sent_at < self.SEND_INTERVAL:
                remaining = int(self.SEND_INTERVAL - (current_time - record.last_sent_at))
                return False, f"发送过于频繁，请在{remaining}秒后重试"
        
        code = self.generate_code()
        
        self.records[phone] = VerificationRecord(code=code, created_at=current_time, attempts=0, locked_until=None, last_sent_at=current_time)
        
        return True, f"验证码已发送: {code}"
    
    def verify_code(self, phone: str, code: str) -> Tuple[bool, str]:
        current_time = time.time()
        
        if phone not in self.records:
            return False, "请先获取验证码"
        
        record = self.records[phone]
        
        if record.locked_until and current_time < record.locked_until:
            remaining = int(record.locked_until - current_time)
            return False, f"账号已锁定，请在{remaining}秒后重试"
        
        if current_time - record.created_at > self.CODE_EXPIRY:
            return False, "验证码已过期，请重新获取"
        
        if record.code == code:
            del self.records[phone]
            return True, "验证成功"
        else:
            record.attempts += 1
            
            if record.attempts >= self.MAX_ATTEMPTS:
                record.locked_until = current_time + self.LOCK_DURATION
                return False, f"验证失败次数过多，账号已锁定{self.LOCK_DURATION // 60}分钟"
            else:
                remaining_attempts = self.MAX_ATTEMPTS - record.attempts
                return False, f"验证码错误，还有{remaining_attempts}次机会"
