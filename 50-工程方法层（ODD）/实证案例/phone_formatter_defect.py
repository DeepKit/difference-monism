class PhoneFormatter:
    def __init__(self, country_code='+1'):
        self.country_code = country_code
    
    def clean(self, phone):
        """移除所有非数字字符"""
        return ''.join(filter(str.isdigit, phone))
    
    def format(self, phone, style='standard'):
        """格式化电话号码"""
        digits = self.clean(phone)
        
        if len(digits) == 10:
            if style == 'standard':
                return f'({digits[:3]}) {digits[3:6]}-{digits[6:]}'
            elif style == 'dots':
                return f'{digits[:3]}.{digits[3:6]}.{digits[6:]}'
            elif style == 'dashes':
                return f'{digits[:3]}-{digits[3:6]}-{digits[6:]}'
            elif style == 'international':
                return f'{self.country_code} {digits[:3]} {digits[3:6]} {digits[6:]}'
        elif len(digits) == 11 and digits[0] == '1':
            return self.format(digits[1:], style)
        
        return digits
    
    def validate(self, phone):
        """验证电话号码"""
        digits = self.clean(phone)
        return len(digits) in [10, 11]