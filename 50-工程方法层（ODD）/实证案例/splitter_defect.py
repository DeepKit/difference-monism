class MessageSplitter:
    """消息分割器类，用于将长消息分割成多个较小的片段"""
    
    def __init__(self, max_length=2000, separator="\n", preserve_words=True):
        """
        初始化消息分割器
        
        Args:
            max_length: 每个片段的最大长度
            separator: 优先分割符（默认换行符）
            preserve_words: 是否保持单词完整性
        """
        self.max_length = max_length
        self.separator = separator
        self.preserve_words = preserve_words
    
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
        current_chunk = ""
        
        # 按分隔符分割
        parts = message.split(self.separator)
        
        for i, part in enumerate(parts):
            # 如果单个部分就超过最大长度，需要强制分割
            if len(part) > self.max_length:
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""
                chunks.extend(self._force_split(part))
                continue
            
            # 尝试添加到当前块
            test_chunk = current_chunk + part
            if i < len(parts) - 1:
                test_chunk += self.separator
            
            if len(test_chunk) <= self.max_length:
                current_chunk = test_chunk
            else:
                # 当前块已满，保存并开始新块
                if current_chunk:
                    chunks.append(current_chunk.rstrip())
                current_chunk = part
                if i < len(parts) - 1:
                    current_chunk += self.separator
        
        # 添加最后一块
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
        
        if self.preserve_words:
            # 尝试按空格分割保持单词完整
            words = text.split(' ')
            current = ""
            
            for word in words:
                if len(word) > self.max_length:
                    # 单词本身太长，按字符分割
                    if current:
                        chunks.append(current.rstrip())
                        current = ""
                    chunks.extend(self._split_by_chars(word))
                elif len(current) + len(word) + 1 <= self.max_length:
                    current += word + " "
                else:
                    chunks.append(current.rstrip())
                    current = word + " "
            
            if current:
                chunks.append(current.rstrip())
        else:
            # 直接按字符分割
            chunks = self._split_by_chars(text)
        
        return chunks
    
    def _split_by_chars(self, text):
        """
        按字符分割文本
        
        Args:
            text: 要分割的文本
            
        Returns:
            list: 分割后的片段列表
        """
        return [text[i:i+self.max_length] 
                for i in range(0, len(text), self.max_length)]
    
    def split_with_prefix(self, message, prefix_template="[{current}/{total}] "):
        """
        分割消息并添加序号前缀
        
        Args:
            message: 要分割的消息
            prefix_template: 前缀模板，支持 {current} 和 {total} 占位符
            
        Returns:
            list: 带前缀的消息片段列表
        """
        chunks = self.split(message)
        total = len(chunks)
        
        if total == 1:
            return chunks
        
        prefixed_chunks = []
        for i, chunk in enumerate(chunks, 1):
            prefix = prefix_template.format(current=i, total=total)
            prefixed_chunks.append(prefix + chunk)
        
        return prefixed_chunks
    
    def split_by_bytes(self, message, max_bytes=4096, encoding='utf-8'):
        """
        按字节数分割消息（适用于有字节限制的场景）
        
        Args:
            message: 要分割的消息
            max_bytes: 最大字节数
            encoding: 字符编码
            
        Returns:
            list: 分割后的消息片段列表
        """
        chunks = []
        current_chunk = ""
        
        for char in message:
            test_chunk = current_chunk + char
            if len(test_chunk.encode(encoding)) <= max_bytes:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = char
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks


# 使用示例
if __name__ == "__main__":
    # 基本使用
    splitter = MessageSplitter(max_length=50)
    long_message = "这是一条很长的消息。" * 20
    chunks = splitter.split(long_message)
    print(f"分割成 {len(chunks)} 个片段")
    
    # 带序号前缀
    chunks_with_prefix = splitter.split_with_prefix(long_message)
    for chunk in chunks_with_prefix:
        print(chunk[:80] + "...")
    
    # 按字节分割
    chunks_bytes = splitter.split_by_bytes(long_message, max_bytes=100)
    print(f"\n按字节分割成 {len(chunks_bytes)} 个片段")