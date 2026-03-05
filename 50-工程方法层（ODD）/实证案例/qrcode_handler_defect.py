import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
import cv2
import numpy as np


class QRCodeHandler:
    """二维码处理类"""
    
    def generate(self, data, filename='qrcode.png', size=10, border=2):
        """
        生成二维码
        
        Args:
            data: 要编码的数据
            filename: 保存文件名
            size: 二维码大小
            border: 边框大小
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        return filename
    
    def read(self, image_path):
        """
        读取二维码
        
        Args:
            image_path: 图片路径
            
        Returns:
            解码后的数据列表
        """
        img = cv2.imread(image_path)
        decoded_objects = decode(img)
        
        results = []
        for obj in decoded_objects:
            results.append({
                'type': obj.type,
                'data': obj.data.decode('utf-8'),
                'rect': obj.rect
            })
        
        return results
    
    def read_from_array(self, img_array):
        """
        从numpy数组读取二维码
        
        Args:
            img_array: 图片数组
            
        Returns:
            解码后的数据列表
        """
        decoded_objects = decode(img_array)
        
        results = []
        for obj in decoded_objects:
            results.append({
                'type': obj.type,
                'data': obj.data.decode('utf-8'),
                'rect': obj.rect
            })
        
        return results


# 使用示例
if __name__ == '__main__':
    handler = QRCodeHandler()
    
    # 生成二维码
    handler.generate('https://example.com', 'test_qr.png')
    
    # 读取二维码
    results = handler.read('test_qr.png')
    for result in results:
        print(f"类型: {result['type']}, 数据: {result['data']}")