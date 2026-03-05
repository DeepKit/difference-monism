from PIL import Image
from pathlib import Path
from typing import Union, Tuple

class ImageResizer:
    def __init__(self, image_path: Union[str, Path]):
        self.image = Image.open(image_path)
        self.original_size = self.image.size
    
    def resize(self, width: int = None, height: int = None, keep_aspect: bool = True) -> 'ImageResizer':
        """调整图片大小"""
        if width is None and height is None:
            return self
        
        if keep_aspect:
            if width and height:
                self.image.thumbnail((width, height), Image.Resampling.LANCZOS)
            elif width:
                ratio = width / self.image.width
                height = int(self.image.height * ratio)
                self.image = self.image.resize((width, height), Image.Resampling.LANCZOS)
            else:
                ratio = height / self.image.height
                width = int(self.image.width * ratio)
                self.image = self.image.resize((width, height), Image.Resampling.LANCZOS)
        else:
            w = width or self.image.width
            h = height or self.image.height
            self.image = self.image.resize((w, h), Image.Resampling.LANCZOS)
        
        return self
    
    def scale(self, factor: float) -> 'ImageResizer':
        """按比例缩放"""
        new_size = (int(self.image.width * factor), int(self.image.height * factor))
        self.image = self.image.resize(new_size, Image.Resampling.LANCZOS)
        return self
    
    def save(self, output_path: Union[str, Path], quality: int = 95):
        """保存图片"""
        self.image.save(output_path, quality=quality, optimize=True)
    
    def get_image(self) -> Image.Image:
        """获取PIL Image对象"""
        return self.image


# 使用示例
if __name__ == "__main__":
    # 按宽度缩放，保持比例
    ImageResizer("input.jpg").resize(width=800).save("output1.jpg")
    
    # 按比例缩放
    ImageResizer("input.jpg").scale(0.5).save("output2.jpg")
    
    # 固定尺寸，不保持比例
    ImageResizer("input.jpg").resize(width=800, height=600, keep_aspect=False).save("output3.jpg")