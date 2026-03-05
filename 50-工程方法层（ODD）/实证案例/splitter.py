class MessageSplitter:
    """消息分割类，用于将长消息分割成多个较小的片段"""
    
    def __init__(self, max_length=2000, separator="\n"):
        """
        初始化消息分割器
        
        Args:
            max_length: 每个片段的最大长度
            separator: 分割符，默认为换行符
        """
        self.max_length = max_length
        self.separator = separator
    
    def split(self, message):
        """
        分割消息
        
        Args:
            message: 要分割的消息字符串
            
        Returns:
            list: 分割后的消息片段列表
        """
        if len(message) <= self.max_length:
            return [message]
        
        chunks = []
        lines = message.split(self.separator)
        current_chunk = ""
        
        for line in lines:
            # 如果单行就超过最大长度，强制分割
            if len(line) > self.max_length:
                if current_chunk:
                    chunks.append(current_chunk.rstrip())
                    current_chunk = ""
                chunks.extend(self._force_split(line))
                continue
            
            # 检查添加这行后是否超过限制
            test_chunk = current_chunk + line + self.separator
            if len(test_chunk) > self.max_length:
                if current_chunk:
                    chunks.append(current_chunk.rstrip())
                current_chunk = line + self.separator
            else:
                current_chunk = test_chunk
        
        if current_chunk:
            chunks.append(current_chunk.rstrip())
        
        return chunks
    
    def _force_split(self, text):
        """
        强制分割超长文本
        
        Args:
            text: 要分割的文本
            
        Returns:
            list: 分割后的片段列表
        """
        chunks = []
        for i in range(0, len(text), self.max_length):
            chunks.append(text[i:i + self.max_length])
        return chunks
    
    def split_by_bytes(self, message, encoding='utf-8'):
        """
        按字节数分割消息
        
        Args:
            message: 要分割的消息字符串
            encoding: 字符编码
            
        Returns:
            list: 分割后的消息片段列表
        """
        chunks = []
        current_chunk = ""
        
        for char in message:
            test_chunk = current_chunk + char
            if len(test_chunk.encode(encoding)) > self.max_length:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = char
            else:
                current_chunk = test_chunk
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def split_smart(self, message, preserve_words=True):
        """
        智能分割，尽量保持单词完整
        
        Args:
            message: 要分割的消息字符串
            preserve_words: 是否保持单词完整
            
        Returns:
            list: 分割后的消息片段列表
        """
        if len(message) <= self.max_length:
            return [message]
        
        chunks = []
        current_chunk = ""
        words = message.split(' ') if preserve_words else [message]
        
        for word in words:
            if len(word) > self.max_length:
                if current_chunk:
                    chunks.append(current_chunk.rstrip())
                    current_chunk = ""
                chunks.extend(self._force_split(word))
                continue
            
            test_chunk = current_chunk + word + ' '
            if len(test_chunk) > self.max_length:
                if current_chunk:
                    chunks.append(current_chunk.rstrip())
                current_chunk = word + ' '
            else:
                current_chunk = test_chunk
        
        if current_chunk:
            chunks.append(current_chunk.rstrip())
        
        return chunks


# 使用示例
if __name__ == "__main__":
    splitter = MessageSplitter(max_length=50)
    
    # 测试基本分割
    long_message = "这是一条很长的消息\n" * 10
    chunks = splitter.split(long_message)
    print(f"分割成 {len(chunks)} 个片段")
    
    # 测试智能分割
    text = "This is a very long message that needs to be split into smaller chunks"
    smart_chunks = splitter.split_smart(text)
    print(f"智能分割成 {len(smart_chunks)} 个片段")
    
    # 测试字节分割
    byte_chunks = splitter.split_by_bytes("中文测试消息" * 10)
    print(f"按字节分割成 {len(byte_chunks)} 个片段")