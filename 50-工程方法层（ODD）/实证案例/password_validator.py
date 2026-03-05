import re
from typing import List, Optional, Callable


class PasswordValidationError(Exception):
    pass


class PasswordValidator:
    def __init__(
        self,
        min_length: int = 8,
        max_length: int = 128,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digits: bool = True,
        require_special: bool = True,
        special_chars: str = "!@#$%^&*()_+-=[]{}|;:,.<>?",
        forbidden_passwords: Optional[List[str]] = None,
        custom_validators: Optional[List[Callable[[str], bool]]] = None
    ):
        if min_length < 1:
            raise ValueError("min_length must be at least 1")
        if max_length < min_length:
            raise ValueError("max_length must be greater than or equal to min_length")
        
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digits = require_digits
        self.require_special = require_special
        self.special_chars = special_chars
        self.forbidden_passwords = set(forbidden_passwords or [])
        self.custom_validators = custom_validators or []
        
    def validate(self, password: str) -> bool:
        errors = self.get_validation_errors(password)
        if errors:
            raise PasswordValidationError("; ".join(errors))
        return True
    
    def get_validation_errors(self, password: str) -> List[str]:
        if not isinstance(password, str):
            return ["Password must be a string"]
        
        errors = []
        
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters long")
        
        if len(password) > self.max_length:
            errors.append(f"Password must not exceed {self.max_length} characters")
        
        if self.require_uppercase and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if self.require_lowercase and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if self.require_digits and not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        
        if self.require_special:
            special_pattern = f"[{re.escape(self.special_chars)}]"
            if not re.search(special_pattern, password):
                errors.append(f"Password must contain at least one special character ({self.special_chars})")
        
        if password.lower() in self.forbidden_passwords:
            errors.append("Password is too common or forbidden")
        
        for validator in self.custom_validators:
            try:
                if not validator(password):
                    errors.append("Password failed custom validation")
            except Exception as e:
                errors.append(f"Custom validation error: {str(e)}")
        
        return errors
    
    def is_valid(self, password: str) -> bool:
        try:
            return len(self.get_validation_errors(password)) == 0
        except Exception:
            return False
    
    def add_forbidden_password(self, password: str) -> None:
        if not isinstance(password, str):
            raise ValueError("Forbidden password must be a string")
        self.forbidden_passwords.add(password.lower())
    
    def add_custom_validator(self, validator: Callable[[str], bool]) -> None:
        if not callable(validator):
            raise ValueError("Custom validator must be callable")
        self.custom_validators.append(validator)
    
    def get_strength(self, password: str) -> str:
        if not isinstance(password, str):
            return "invalid"
        
        score = 0
        
        if len(password) >= self.min_length:
            score += 1
        if len(password) >= 12:
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(f"[{re.escape(self.special_chars)}]", password):
            score += 1
        if len(password) >= 16:
            score += 1
        
        if score <= 2:
            return "weak"
        elif score <= 4:
            return "medium"
        elif score <= 6:
            return "strong"
        else:
            return "very_strong"


if __name__ == "__main__":
    validator = PasswordValidator(
        min_length=8,
        max_length=64,
        forbidden_passwords=["password", "123456", "qwerty"]
    )
    
    test_passwords = [
        "weak",
        "Password123",
        "P@ssw0rd!",
        "password",
        "VeryStr0ng!Pass"
    ]
    
    for pwd in test_passwords:
        print(f"\nTesting: {pwd}")
        print(f"Valid: {validator.is_valid(pwd)}")
        print(f"Strength: {validator.get_strength(pwd)}")
        errors = validator.get_validation_errors(pwd)
        if errors:
            print(f"Errors: {errors}")