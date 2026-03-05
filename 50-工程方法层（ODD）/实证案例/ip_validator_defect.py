import ipaddress

class IPValidator:
    @staticmethod
    def is_valid_ipv4(ip: str) -> bool:
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_ipv6(ip: str) -> bool:
        try:
            ipaddress.IPv6Address(ip)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False


# 使用示例
if __name__ == "__main__":
    validator = IPValidator()
    
    # IPv4
    print(validator.is_valid_ipv4("192.168.1.1"))      # True
    print(validator.is_valid_ipv4("256.1.1.1"))        # False
    
    # IPv6
    print(validator.is_valid_ipv6("2001:db8::1"))      # True
    print(validator.is_valid_ipv6("invalid"))          # False
    
    # 通用验证
    print(validator.is_valid_ip("192.168.1.1"))        # True
    print(validator.is_valid_ip("2001:db8::1"))        # True