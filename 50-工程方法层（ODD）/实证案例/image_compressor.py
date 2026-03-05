from PIL import Image
import os
from pathlib import Path
from typing import Union, Tuple, Optional


class ImageCompressor:
    """图片压缩工具类"""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
    
    def __init__(self):
        self.last_compression_ratio = None
    
    def compress_by_quality(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path], 
        quality: int = 85
    ) -> dict:
        """按质量压缩图片
        
        Args:
            input_path: 输入图片路径
            output_path: 输出图片路径
            quality: 压缩质量 (1-100)
            
        Returns:
            包含压缩信息的字典
        """
        if not 1 <= quality <= 100:
            raise ValueError("质量参数必须在1-100之间")
        
        img = Image.open(input_path)
        
        # 转换RGBA为RGB
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 保存压缩后的图片
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        return self._get_compression_info(input_path, output_path)
    
    def compress_by_size(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path], 
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        quality: int = 85
    ) -> dict:
        """按尺寸压缩图片
        
        Args:
            input_path: 输入图片路径
            output_path: 输出图片路径
            max_width: 最大宽度
            max_height: 最大高度
            quality: 压缩质量
            
        Returns:
            包含压缩信息的字典
        """
        img = Image.open(input_path)
        original_size = img.size
        
        # 计算新尺寸
        width, height = img.size
        if max_width and width > max_width:
            height = int(height * max_width / width)
            width = max_width
        if max_height and height > max_height:
            width = int(width * max_height / height)
            height = max_height
        
        # 调整尺寸
        if (width, height) != original_size:
            img = img.resize((width, height), Image.Resampling.LANCZOS)
        
        # 转换颜色模式
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        img.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        return self._get_compression_info(input_path, output_path)
    
    def compress_to_target_size(
        self, 
        input_path: Union[str, Path], 
        output_path: Union[str, Path], 
        target_size_kb: int,
        max_iterations: int = 10
    ) -> dict:
        """压缩到目标文件大小
        
        Args:
            input_path: 输入图片路径
            output_path: 输出图片路径
            target_size_kb: 目标文件大小(KB)
            max_iterations: 最大尝试次数
            
        Returns:
            包含压缩信息的字典
        """
        img = Image.open(input_path)
        
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        quality = 95
        target_size_bytes = target_size_kb * 1024
        
        for i in range(max_iterations):
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            current_size = os.path.getsize(output_path)
            
            if current_size <= target_size_bytes:
                break
            
            # 根据当前大小调整质量
            ratio = target_size_bytes / current_size
            quality = int(quality * ratio * 0.9)
            quality = max(10, min(quality, 95))
        
        return self._get_compression_info(input_path, output_path)
    
    def batch_compress(
        self, 
        input_dir: Union[str, Path], 
        output_dir: Union[str, Path], 
        quality: int = 85,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None
    ) -> list:
        """批量压缩图片
        
        Args:
            input_dir: 输入目录
            output_dir: 输出目录
            quality: 压缩质量
            max_width: 最大宽度
            max_height: 最大高度
            
        Returns:
            压缩结果列表
        """
        input_dir = Path(input_dir)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        results = []
        
        for file_path in input_dir.iterdir():
            if file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                output_path = output_dir / file_path.name
                try:
                    if max_width or max_height:
                        result = self.compress_by_size(
                            file_path, output_path, max_width, max_height, quality
                        )
                    else:
                        result = self.compress_by_quality(file_path, output_path, quality)
                    results.append(result)
                except Exception as e:
                    results.append({
                        'input': str(file_path),
                        'error': str(e)
                    })
        
        return results
    
    def _get_compression_info(self, input_path: Union[str, Path], output_path: Union[str, Path]) -> dict:
        """获取压缩信息"""
        input_size = os.path.getsize(input_path)
        output_size = os.path.getsize(output_path)
        ratio = (1 - output_size / input_size) * 100
        
        self.last_compression_ratio = ratio
        
        return {
            'input': str(input_path),
            'output': str(output_path),
            'original_size': f"{input_size / 1024:.2f} KB",
            'compressed_size': f"{output_size / 1024:.2f} KB",
            'compression_ratio': f"{ratio:.2f}%"
        }


# 使用示例
if __name__ == '__main__':
    compressor = ImageCompressor()
    
    # 按质量压缩
    result = compressor.compress_by_quality('input.jpg', 'output.jpg', quality=80)
    print(result)
    
    # 按尺寸压缩
    result = compressor.compress_by_size('input.jpg', 'output.jpg', max_width=1920, quality=85)
    print(result)
    
    # 压缩到目标大小
    result = compressor.compress_to_target_size('input.jpg', 'output.jpg', target_size_kb=500)
    print(result)
    
    # 批量压缩
    results = compressor.batch_compress('input_folder', 'output_folder', quality=80)
    for r in results:
        print(r)