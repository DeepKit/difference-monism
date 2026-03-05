
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import base64
import json


class DataEncryptor:
    def __init__(self, key=None):
        """
        初始化加密器
        :param key: 32字节的密钥，如果为None则自动生成
        """
        if key is None:
            self.key = self.generate_key()
        else:
            if len(key) != 32:
                raise ValueError("密钥必须是32字节")
            self.key = key
        self.backend = default_backend()

    @staticmethod
    def generate_key():
        """生成随机32字节密钥"""
        return os.urandom(32)

    @staticmethod
    def derive_key_from_password(password, salt=None):
        """
        从密码派生密钥
        :param password: 字符串密码
        :param salt: 盐值，如果为None则生成新的
        :return: (密钥, 盐值)
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        return key, salt

    def encrypt(self, plaintext):
        """
        加密数据
        :param plaintext: 明文字符串或字节
        :return: base64编码的加密数据（包含IV）
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode()

        # 生成随机IV
        iv = os.urandom(16)

        # 创建加密器
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()

        # PKCS7填充
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        # 加密
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # 将IV和密文组合并编码
        encrypted_data = iv + ciphertext
        return base64.b64encode(encrypted_data).decode()

    def decrypt(self, encrypted_data):
        """
        解密数据
        :param encrypted_data: base64编码的加密数据
        :return: 解密后的字符串
        """
        # 解码
        encrypted_bytes = base64.b64decode(encrypted_data)

        # 提取IV和密文
        iv = encrypted_bytes[:16]
        ciphertext = encrypted_bytes[16:]

        # 创建解密器
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=self.backend
        )
        decryptor = cipher.decryptor()

        # 解密
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        # 去除填充
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

        return plaintext.decode()

    def encrypt_file(self, input_path, output_path):
        """加密文件"""
        with open(input_path, 'rb') as f:
            plaintext = f.read()
        
        encrypted = self.encrypt(plaintext)
        
        with open(output_path, 'w') as f:
            f.write(encrypted)

    def decrypt_file(self, input_path, output_path):
        """解密文件"""
        with open(input_path, 'r') as f:
            encrypted = f.read()
        
        decrypted = self.decrypt(encrypted)
        
        with open(output_path, 'wb') as f:
            f.write(decrypted.encode() if isinstance(decrypted, str) else decrypted)

    def save_key(self, filepath):
        """保存密钥到文件"""
        key_b64 = base64.b64encode(self.key).decode()
        with open(filepath, 'w') as f:
            json.dump({'key': key_b64}, f)

    @classmethod
    def load_key(cls, filepath):
        """从文件加载密钥并创建加密器实例"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        key = base64.b64decode(data['key'])
        return cls(key=key)

    def get_key_base64(self):
        """获取base64编码的密钥"""
        return base64.b64encode(self.key).decode()

    @classmethod
    def from_key_base64(cls, key_b64):
        """从base64编码的密钥创建实例"""
        key = base64.b64decode(key_b64)
        return cls(key=key)


# 使用示例
if __name__ == "__main__":
    # 创建加密器
    encryptor = DataEncryptor()
    
    # 加密数据
    plaintext = "这是需要加密的敏感数据"
    encrypted = encryptor.encrypt(plaintext)
    print(f"加密后: {encrypted}")
    
    # 解密数据
    decrypted = encryptor.decrypt(encrypted)
    print(f"解密后: {decrypted}")
    
    # 保存密钥
    encryptor.save_key("secret.key")
    
    # 加载密钥
    encryptor2 = DataEncryptor.load_key("secret.key")
    decrypted2 = encryptor2.decrypt(encrypted)
    print(f"使用加载的密钥解密: {decrypted2}")
    
    # 从密码派生密钥
    password = "my_secure_password"
    key, salt = DataEncryptor.derive_key_from_password(password)
    encryptor3 = DataEncryptor(key=key)
    encrypted3 = encryptor3.encrypt("使用密码派生的密钥加密")
    print(f"密码派生密钥加密: {encrypted3}")
