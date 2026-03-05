import hashlib


class HashGenerator:
    """哈希生成器"""
    
    def __init__(self, algorithm='sha256'):
        """
        初始化哈希生成器
        :param algorithm: 哈希算法 (md5, sha1, sha256, sha512等)
        """
        self.algorithm = algorithm.lower()
    
    def hash_string(self, text):
        """对字符串生成哈希"""
        return hashlib.new(self.algorithm, text.encode('utf-8')).hexdigest()
    
    def hash_file(self, filepath):
        """对文件生成哈希"""
        h = hashlib.new(self.algorithm)
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                h.update(chunk)
        return h.hexdigest()
    
    def hash_bytes(self, data):
        """对字节数据生成哈希"""
        return hashlib.new(self.algorithm, data).hexdigest()


# 使用示例
if __name__ == '__main__':
    # SHA256
    gen = HashGenerator('sha256')
    print(gen.hash_string('Hello World'))
    
    # MD5
    gen_md5 = HashGenerator('md5')
    print(gen_md5.hash_string('Hello World'))