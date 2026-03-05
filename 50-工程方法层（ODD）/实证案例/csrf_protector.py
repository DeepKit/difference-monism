
import secrets
import hashlib
import hmac
import time
from typing import Optional, Dict
from datetime import datetime, timedelta


class CSRFProtector:
    def __init__(self, secret_key: str, token_length: int = 32, token_expiry: int = 3600):
        """
        Initialize CSRF Protector
        
        :param secret_key: Secret key for HMAC signing
        :param token_length: Length of generated tokens
        :param token_expiry: Token expiry time in seconds
        """
        self.secret_key = secret_key.encode() if isinstance(secret_key, str) else secret_key
        self.token_length = token_length
        self.token_expiry = token_expiry
        self._tokens: Dict[str, float] = {}
    
    def generate_token(self, session_id: Optional[str] = None) -> str:
        """
        Generate a new CSRF token
        
        :param session_id: Optional session identifier
        :return: Generated CSRF token
        """
        random_token = secrets.token_urlsafe(self.token_length)
        timestamp = str(time.time())
        
        if session_id:
            data = f"{random_token}:{session_id}:{timestamp}"
        else:
            data = f"{random_token}:{timestamp}"
        
        signature = hmac.new(
            self.secret_key,
            data.encode(),
            hashlib.sha256
        ).hexdigest()
        
        token = f"{random_token}.{signature}.{timestamp}"
        self._tokens[token] = time.time()
        
        return token
    
    def validate_token(self, token: str, session_id: Optional[str] = None) -> bool:
        """
        Validate a CSRF token
        
        :param token: Token to validate
        :param session_id: Optional session identifier
        :return: True if valid, False otherwise
        """
        if not token:
            return False
        
        try:
            parts = token.split('.')
            if len(parts) != 3:
                return False
            
            random_token, signature, timestamp = parts
            
            # Check token expiry
            token_time = float(timestamp)
            if time.time() - token_time > self.token_expiry:
                self._remove_token(token)
                return False
            
            # Reconstruct data and verify signature
            if session_id:
                data = f"{random_token}:{session_id}:{timestamp}"
            else:
                data = f"{random_token}:{timestamp}"
            
            expected_signature = hmac.new(
                self.secret_key,
                data.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Timing-safe comparison
            is_valid = hmac.compare_digest(signature, expected_signature)
            
            if is_valid and token in self._tokens:
                return True
            
            return False
            
        except (ValueError, AttributeError):
            return False
    
    def validate_and_consume_token(self, token: str, session_id: Optional[str] = None) -> bool:
        """
        Validate and consume (remove) a CSRF token (one-time use)
        
        :param token: Token to validate
        :param session_id: Optional session identifier
        :return: True if valid, False otherwise
        """
        is_valid = self.validate_token(token, session_id)
        if is_valid:
            self._remove_token(token)
        return is_valid
    
    def _remove_token(self, token: str) -> None:
        """Remove token from storage"""
        self._tokens.pop(token, None)
    
    def cleanup_expired_tokens(self) -> int:
        """
        Remove expired tokens from storage
        
        :return: Number of tokens removed
        """
        current_time = time.time()
        expired_tokens = [
            token for token, created_time in self._tokens.items()
            if current_time - created_time > self.token_expiry
        ]
        
        for token in expired_tokens:
            self._remove_token(token)
        
        return len(expired_tokens)
    
    def get_token_count(self) -> int:
        """Get current number of stored tokens"""
        return len(self._tokens)
    
    def clear_all_tokens(self) -> None:
        """Clear all stored tokens"""
        self._tokens.clear()


# Usage example
if __name__ == "__main__":
    # Initialize protector
    csrf = CSRFProtector(secret_key="your-secret-key-here", token_expiry=3600)
    
    # Generate token
    token = csrf.generate_token(session_id="user123")
    print(f"Generated token: {token}")
    
    # Validate token
    is_valid = csrf.validate_token(token, session_id="user123")
    print(f"Token valid: {is_valid}")
    
    # Validate and consume (one-time use)
    is_valid = csrf.validate_and_consume_token(token, session_id="user123")
    print(f"Token consumed: {is_valid}")
    
    # Try to validate again (should fail)
    is_valid = csrf.validate_token(token, session_id="user123")
    print(f"Token valid after consumption: {is_valid}")
