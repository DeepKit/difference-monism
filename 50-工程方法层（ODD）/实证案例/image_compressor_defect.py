from PIL import Image
import os


class ImageCompressor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
    
    def compress(self, output_path=None, quality=85, max_size=None):
        """
        压缩图片
        
        Args:
            output_path: 输出路径，默认为原文件名_compressed
            quality: 压缩质量 (1-100)，默认85
            max_size: 最大尺寸 (width, height)，保持比例
        """
        img = self.image.copy()
        
        # 调整尺寸
        if max_size:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # 设置输出路径
        if not output_path:
            name, ext = os.path.splitext(self.image_path)
            output_path = f"{name}_compressed{ext}"
        
        # 转换RGBA为RGB
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # 保存压缩图片
        img.save(output_path, optimize=True, quality=quality)
        
        return output_path
    
    def get_size(self):
        """获取图片尺寸"""
        return self.image.size
    
    def get_file_size(self):
        """获取文件大小(KB)"""
        return os.path.getsize(self.image_path) / 1024


# 使用示例
if __name__ == "__main__":
    compressor = ImageCompressor("example.jpg")
    print(f"原始尺寸: {compressor.get_size()}")
    print(f"原始大小: {compressor.get_file_size():.2f} KB")
    
    # 压缩图片
    output = compressor.compress(quality=70, max_size=(1920, 1080))
    print(f"已保存到: {output}")