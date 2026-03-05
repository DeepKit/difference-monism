
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64


class AESCipher:
    def __init__(self, key=None):
        """
        初始化AES加密器
        :param key: 32字节的密钥，如果为None则自动生成
        """
        if key is None:
            self.key = os.urandom(32)  # 生成256位密钥
        else:
            self.key = key if len(key) == 32 else key.ljust(32)[:32].encode() if isinstance(key, str) else key

    def encrypt(self, plaintext):
        """
        加密数据
        :param plaintext: 明文字符串
        :return: Base64编码的密文
        """
        # 生成随机IV
        iv = os.urandom(16)
        
        # 创建加密器
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # 填充明文
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        
        # 加密
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # 将IV和密文组合并Base64编码
        return base64.b64encode(iv + ciphertext).decode()

    def decrypt(self, ciphertext):
        """
        解密数据
        :param ciphertext: Base64编码的密文
        :return: 明文字符串
        """
        # Base64解码
        data = base64.b64decode(ciphertext)
        
        # 分离IV和密文
        iv = data[:16]
        actual_ciphertext = data[16:]
        
        # 创建解密器
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # 解密
        padded_plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
        
        # 去除填充
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        
        return plaintext.decode()

    def get_key(self):
        """获取密钥的Base64编码"""
        return base64.b64encode(self.key).decode()

    @staticmethod
    def from_key_string(key_string):
        """从Base64编码的密钥字符串创建加密器"""
        key = base64.b64decode(key_string)
        return AESCipher(key)


# 使用示例
if __name__ == "__main__":
    # 创建加密器
    cipher = AESCipher()
    
    # 加密
    plaintext = "这是需要加密的敏感数据"
    encrypted = cipher.encrypt(plaintext)
    print(f"加密后: {encrypted}")
    
    # 解密
    decrypted = cipher.decrypt(encrypted)
    print(f"解密后: {decrypted}")
    
    # 保存密钥以便后续使用
    key_string = cipher.get_key()
    print(f"密钥: {key_string}")
    
    # 使用已有密钥创建新的加密器
    cipher2 = AESCipher.from_key_string(key_string)
    decrypted2 = cipher2.decrypt(encrypted)
    print(f"使用保存的密钥解密: {decrypted2}")
