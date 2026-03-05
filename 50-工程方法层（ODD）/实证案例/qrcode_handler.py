"""
QR码处理类 - 完整实现
支持生成、读取、验证QR码
"""

import qrcode
from qrcode.image.pure import PyPNGImage
from PIL import Image
import io
import base64
from pathlib import Path
from typing import Optional, Union, Tuple, List
from dataclasses import dataclass
from enum import Enum


class ErrorCorrectionLevel(Enum):
    """错误纠正级别"""
    LOW = qrcode.constants.ERROR_CORRECT_L  # 7%
    MEDIUM = qrcode.constants.ERROR_CORRECT_M  # 15%
    QUARTILE = qrcode.constants.ERROR_CORRECT_Q  # 25%
    HIGH = qrcode.constants.ERROR_CORRECT_H  # 30%


@dataclass
class QRCodeConfig:
    """QR码配置"""
    version: Optional[int] = None  # 1-40, None为自动
    error_correction: ErrorCorrectionLevel = ErrorCorrectionLevel.MEDIUM
    box_size: int = 10
    border: int = 4
    fill_color: str = "black"
    back_color: str = "white"


class QRCodeError(Exception):
    """QR码处理异常基类"""
    pass


class QRCodeGenerationError(QRCodeError):
    """QR码生成异常"""
    pass


class QRCodeReadError(QRCodeError):
    """QR码读取异常"""
    pass


class QRCodeHandler:
    """QR码处理类"""
    
    def __init__(self, config: Optional[QRCodeConfig] = None):
        """
        初始化QR码处理器
        
        Args:
            config: QR码配置，默认使用标准配置
        """
        self.config = config or QRCodeConfig()
    
    def generate(
        self,
        data: str,
        output_path: Optional[Union[str, Path]] = None,
        logo_path: Optional[Union[str, Path]] = None,
        logo_size_ratio: float = 0.3
    ) -> Image.Image:
        """
        生成QR码
        
        Args:
            data: 要编码的数据
            output_path: 输出文件路径（可选）
            logo_path: 中心logo图片路径（可选）
            logo_size_ratio: logo占QR码的比例
            
        Returns:
            PIL Image对象
            
        Raises:
            QRCodeGenerationError: 生成失败时抛出
        """
        try:
            if not data:
                raise QRCodeGenerationError("数据不能为空")
            
            # 创建QR码对象
            qr = qrcode.QRCode(
                version=self.config.version,
                error_correction=self.config.error_correction.value,
                box_size=self.config.box_size,
                border=self.config.border,
            )
            
            # 添加数据
            qr.add_data(data)
            qr.make(fit=True)
            
            # 生成图像
            img = qr.make_image(
                fill_color=self.config.fill_color,
                back_color=self.config.back_color
            ).convert('RGB')
            
            # 添加logo
            if logo_path:
                img = self._add_logo(img, logo_path, logo_size_ratio)
            
            # 保存文件
            if output_path:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                img.save(output_path)
            
            return img
            
        except Exception as e:
            raise QRCodeGenerationError(f"生成QR码失败: {str(e)}") from e
    
    def _add_logo(
        self,
        qr_img: Image.Image,
        logo_path: Union[str, Path],
        size_ratio: float
    ) -> Image.Image:
        """
        在QR码中心添加logo
        
        Args:
            qr_img: QR码图像
            logo_path: logo文件路径
            size_ratio: logo大小比例
            
        Returns:
            添加logo后的图像
        """
        try:
            logo = Image.open(logo_path)
            
            # 计算logo大小
            qr_width, qr_height = qr_img.size
            logo_size = int(min(qr_width, qr_height) * size_ratio)
            
            # 调整logo大小
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # 计算logo位置（居中）
            logo_pos = (
                (qr_width - logo_size) // 2,
                (qr_height - logo_size) // 2
            )
            
            # 粘贴logo
            qr_img.paste(logo, logo_pos, logo if logo.mode == 'RGBA' else None)
            
            return qr_img
            
        except Exception as e:
            raise QRCodeGenerationError(f"添加logo失败: {str(e)}") from e
    
    def read(
        self,
        image_source: Union[str, Path, Image.Image, bytes]
    ) -> List[str]:
        """
        读取QR码内容
        
        Args:
            image_source: 图像源（文件路径、PIL Image对象或字节数据）
            
        Returns:
            解码的数据列表（可能包含多个QR码）
            
        Raises:
            QRCodeReadError: 读取失败时抛出
        """
        try:
            # 加载图像
            if isinstance(image_source, (str, Path)):
                img = Image.open(image_source)
            elif isinstance(image_source, bytes):
                img = Image.open(io.BytesIO(image_source))
            elif isinstance(image_source, Image.Image):
                img = image_source
            else:
                raise QRCodeReadError("不支持的图像源类型")
            
            # 尝试使用pyzbar解码
            try:
                from pyzbar import pyzbar
                decoded_objects = pyzbar.decode(img)
                if decoded_objects:
                    return [obj.data.decode('utf-8') for obj in decoded_objects]
            except ImportError:
                pass
            
            # 尝试使用opencv解码
            try:
                import cv2
                import numpy as np
                
                img_array = np.array(img)
                detector = cv2.QRCodeDetector()
                data, vertices, _ = detector.detectAndDecode(img_array)
                
                if data:
                    return [data]
            except ImportError:
                pass
            
            raise QRCodeReadError(
                "无法读取QR码。请安装 pyzbar 或 opencv-python: "
                "pip install pyzbar 或 pip install opencv-python"
            )
            
        except QRCodeReadError:
            raise
        except Exception as e:
            raise QRCodeReadError(f"读取QR码失败: {str(e)}") from e
    
    def to_base64(self, data: str) -> str:
        """
        生成QR码并转换为base64字符串
        
        Args:
            data: 要编码的数据
            
        Returns:
            base64编码的图像字符串
        """
        try:
            img = self.generate(data)
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/png;base64,{img_base64}"
        except Exception as e:
            raise QRCodeGenerationError(f"转换为base64失败: {str(e)}") from e
    
    def batch_generate(
        self,
        data_list: List[str],
        output_dir: Union[str, Path],
        filename_prefix: str = "qr"
    ) -> List[Path]:
        """
        批量生成QR码
        
        Args:
            data_list: 数据列表
            output_dir: 输出目录
            filename_prefix: 文件名前缀
            
        Returns:
            生成的文件路径列表
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_paths = []
        for i, data in enumerate(data_list, 1):
            try:
                output_path = output_dir / f"{filename_prefix}_{i}.png"
                self.generate(data, output_path)
                output_paths.append(output_path)
            except Exception as e:
                print(f"警告: 生成第{i}个QR码失败: {e}")
        
        return output_paths
    
    def validate(self, image_source: Union[str, Path, Image.Image]) -> bool:
        """
        验证图像是否包含有效的QR码
        
        Args:
            image_source: 图像源
            
        Returns:
            是否包含有效QR码
        """
        try:
            results = self.read(image_source)
            return len(results) > 0
        except:
            return False
    
    def get_info(self, image_source: Union[str, Path, Image.Image]) -> dict:
        """
        获取QR码信息
        
        Args:
            image_source: 图像源
            
        Returns:
            QR码信息字典
        """
        try:
            data_list = self.read(image_source)
            
            if isinstance(image_source, (str, Path)):
                img = Image.open(image_source)
            elif isinstance(image_source, Image.Image):
                img = image_source
            else:
                img = None
            
            return {
                "valid": True,
                "count": len(data_list),
                "data": data_list,
                "size": img.size if img else None,
                "format": img.format if img else None
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }


# 使用示例
if __name__ == "__main__":
    # 创建处理器
    handler = QRCodeHandler()
    
    # 生成QR码
    try:
        img = handler.generate(
            "https://github.com",
            output_path="qrcode.png"
        )
        print("✓ QR码生成成功")
    except QRCodeError as e:
        print(f"✗ 生成失败: {e}")
    
    # 读取QR码
    try:
        data = handler.read("qrcode.png")
        print(f"✓ 读取成功: {data}")
    except QRCodeError as e:
        print(f"✗ 读取失败: {e}")
    
    # 生成base64
    try:
        base64_str = handler.to_base64("Hello QR Code")
        print(f"✓ Base64生成成功 (长度: {len(base64_str)})")
    except QRCodeError as e:
        print(f"✗ Base64生成失败: {e}")
    
    # 批量生成
    try:
        urls = ["https://example1.com", "https://example2.com", "https://example3.com"]
        paths = handler.batch_generate(urls, "qrcodes")
        print(f"✓ 批量生成成功: {len(paths)}个文件")
    except Exception as e:
        print(f"✗ 批量生成失败: {e}")