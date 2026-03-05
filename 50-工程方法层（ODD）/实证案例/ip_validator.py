import re
import ipaddress


class IPValidator:
    """IP地址验证类，支持IPv4和IPv6"""
    
    @staticmethod
    def is_valid_ipv4(ip: str) -> bool:
        """验证IPv4地址"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            
            for part in parts:
                if not part.isdigit():
                    return False
                num = int(part)
                if num < 0 or num > 255:
                    return False
                # 检查前导零（除了单独的0）
                if len(part) > 1 and part[0] == '0':
                    return False
            
            return True
        except:
            return False
    
    @staticmethod
    def is_valid_ipv6(ip: str) -> bool:
        """验证IPv6地址"""
        try:
            ipaddress.IPv6Address(ip)
            return True
        except:
            return False
    
    @staticmethod
    def is_valid_ip(ip: str) -> bool:
        """验证IP地址（IPv4或IPv6）"""
        return IPValidator.is_valid_ipv4(ip) or IPValidator.is_valid_ipv6(ip)
    
    @staticmethod
    def get_ip_version(ip: str) -> int:
        """获取IP版本，返回4、6或0（无效）"""
        if IPValidator.is_valid_ipv4(ip):
            return 4
        elif IPValidator.is_valid_ipv6(ip):
            return 6
        return 0
    
    @staticmethod
    def is_private_ip(ip: str) -> bool:
        """检查是否为私有IP"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return ip_obj.is_private
        except:
            return False
    
    @staticmethod
    def is_loopback(ip: str) -> bool:
        """检查是否为回环地址"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return ip_obj.is_loopback
        except:
            return False


# 使用示例
if __name__ == "__main__":
    test_ips = [
        "192.168.1.1",
        "255.255.255.255",
        "256.1.1.1",
        "192.168.01.1",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "::1",
        "invalid.ip",
    ]
    
    for ip in test_ips:
        print(f"{ip:45} - Valid: {IPValidator.is_valid_ip(ip)}, "
              f"Version: {IPValidator.get_ip_version(ip)}, "
              f"Private: {IPValidator.is_private_ip(ip)}")