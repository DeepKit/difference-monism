from PIL import Image
from typing import Tuple, Optional
from pathlib import Path


class ImageResizer:
    def __init__(self, image_path: str):
        self.image_path = Path(image_path)
        self.image = Image.open(image_path)
        self.original_size = self.image.size
    
    def resize(self, width: int, height: int, maintain_aspect: bool = True) -> 'ImageResizer':
        """调整图片大小"""
        if maintain_aspect:
            self.image.thumbnail((width, height), Image.Resampling.LANCZOS)
        else:
            self.image = self.image.resize((width, height), Image.Resampling.LANCZOS)
        return self
    
    def resize_by_width(self, width: int) -> 'ImageResizer':
        """按宽度等比缩放"""
        ratio = width / self.image.width
        height = int(self.image.height * ratio)
        self.image = self.image.resize((width, height), Image.Resampling.LANCZOS)
        return self
    
    def resize_by_height(self, height: int) -> 'ImageResizer':
        """按高度等比缩放"""
        ratio = height / self.image.height
        width = int(self.image.width * ratio)
        self.image = self.image.resize((width, height), Image.Resampling.LANCZOS)
        return self
    
    def resize_by_percentage(self, percentage: float) -> 'ImageResizer':
        """按百分比缩放"""
        width = int(self.image.width * percentage)
        height = int(self.image.height * percentage)
        self.image = self.image.resize((width, height), Image.Resampling.LANCZOS)
        return self
    
    def crop_center(self, width: int, height: int) -> 'ImageResizer':
        """居中裁剪"""
        left = (self.image.width - width) // 2
        top = (self.image.height - height) // 2
        right = left + width
        bottom = top + height
        self.image = self.image.crop((left, top, right, bottom))
        return self
    
    def fit(self, width: int, height: int, background_color: Tuple[int, int, int] = (255, 255, 255)) -> 'ImageResizer':
        """适应尺寸（保持比例，填充背景）"""
        self.image.thumbnail((width, height), Image.Resampling.LANCZOS)
        new_image = Image.new('RGB', (width, height), background_color)
        offset = ((width - self.image.width) // 2, (height - self.image.height) // 2)
        new_image.paste(self.image, offset)
        self.image = new_image
        return self
    
    def save(self, output_path: str, quality: int = 95) -> None:
        """保存图片"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.image.save(output_path, quality=quality, optimize=True)
    
    def get_size(self) -> Tuple[int, int]:
        """获取当前尺寸"""
        return self.image.size
    
    def reset(self) -> 'ImageResizer':
        """重置为原始图片"""
        self.image = Image.open(self.image_path)
        return self


# 使用示例
if __name__ == "__main__":
    # 基本缩放
    resizer = ImageResizer("input.jpg")
    resizer.resize(800, 600).save("output1.jpg")
    
    # 按宽度缩放
    resizer.reset().resize_by_width(1000).save("output2.jpg")
    
    # 按百分比缩放
    resizer.reset().resize_by_percentage(0.5).save("output3.jpg")
    
    # 居中裁剪
    resizer.reset().crop_center(500, 500).save("output4.jpg")
    
    # 适应尺寸（带背景）
    resizer.reset().fit(1920, 1080, (0, 0, 0)).save("output5.jpg")