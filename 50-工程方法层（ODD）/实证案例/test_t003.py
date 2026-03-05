import pytest
from pathlib import Path
import tempfile
import shutil
from file_uploader import (
    FileUploader, 
    FileUploadError, 
    FileSizeError, 
    FileTypeError
)


@pytest.fixture
def temp_dir():
    """创建临时目录"""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def uploader(temp_dir):
    """创建文件上传器实例"""
    upload_dir = Path(temp_dir) / 'uploads'
    return FileUploader(str(upload_dir))


@pytest.fixture
def sample_files(temp_dir):
    """创建测试文件"""
    files = {}
    
    # 创建小图片文件（1KB）
    small_image = Path(temp_dir) / 'test.jpg'
    small_image.write_bytes(b'x' * 1024)
    files['small_image'] = small_image
    
    # 创建大文件（11MB，超过限制）
    large_file = Path(temp_dir) / 'large.jpg'
    large_file.write_bytes(b'x' * (11 * 1024 * 1024))
    files['large_file'] = large_file
    
    # 创建PDF文件
    pdf_file = Path(temp_dir) / 'document.pdf'
    pdf_file.write_bytes(b'%PDF-1.4' + b'x' * 1000)
    files['pdf_file'] = pdf_file
    
    # 创建不支持的文件类型
    txt_file = Path(temp_dir) / 'test.txt'
    txt_file.write_text('test content')
    files['txt_file'] = txt_file
    
    return files


class TestFileUploader:
    """文件上传器测试"""
    
    def test_upload_dir_creation(self, temp_dir):
        """测试上传目录自动创建"""
        upload_dir = Path(temp_dir) / 'new_uploads'
        uploader = FileUploader(str(upload_dir))
        assert upload_dir.exists()
    
    def test_upload_valid_image(self, uploader, sample_files):
        """测试上传有效图片"""
        result = uploader.upload(sample_files['small_image'])
        
        assert result['success'] is True
        assert result['filename'] == 'test.jpg'
        assert Path(result['path']).exists()
        assert result['size'] == 1024
        assert '成功' in result['message']
    
    def test_upload_valid_pdf(self, uploader, sample_files):
        """测试上传有效PDF"""
        result = uploader.upload(sample_files['pdf_file'])
        
        assert result['success'] is True
        assert result['filename'] == 'document.pdf'
        assert Path(result['path']).exists()
    
    def test_file_size_limit(self, uploader, sample_files):
        """测试文件大小限制"""
        with pytest.raises(FileSizeError) as exc_info:
            uploader.upload(sample_files['large_file'])
        
        assert '超过限制' in str(exc_info.value)
        assert '10' in str(exc_info.value)
    
    def test_file_type_validation(self, uploader, sample_files):
        """测试文件类型验证"""
        with pytest.raises(FileTypeError) as exc_info:
            uploader.upload(sample_files['txt_file'])
        
        assert '不支持的文件类型' in str(exc_info.value)
        assert '.txt' in str(exc_info.value)
    
    def test_duplicate_filename_handling(self, uploader, sample_files):
        """测试重名文件处理"""
        # 第一次上传
        result1 = uploader.upload(sample_files['small_image'])
        assert result1['filename'] == 'test.jpg'
        
        # 第二次上传同名文件
        result2 = uploader.upload(sample_files['small_image'])
        assert result2['filename'] != 'test.jpg'
        assert result2['filename'].startswith('test_')
        assert result2['filename'].endswith('.jpg')
        
        # 验证两个文件都存在
        assert Path(result1['path']).exists()
        assert Path(result2['path']).exists()
    
    def test_custom_filename(self, uploader, sample_files):
        """测试自定义文件名"""
        result = uploader.upload(
            sample_files['small_image'], 
            filename='custom_name.jpg'
        )
        
        assert result['filename'] == 'custom_name.jpg'
    
    def test_nonexistent_source_file(self, uploader, temp_dir):
        """测试源文件不存在"""
        fake_path = Path(temp_dir) / 'nonexistent.jpg'
        
        with pytest.raises(FileUploadError) as exc_info:
            uploader.upload(fake_path)
        
        assert '源文件不存在' in str(exc_info.value)
    
    def test_get_uploaded_files(self, uploader, sample_files):
        """测试获取已上传文件列表"""
        # 初始为空
        assert uploader.get_uploaded_files() == []
        
        # 上传几个文件
        uploader.upload(sample_files['small_image'])
        uploader.upload(sample_files['pdf_file'])
        
        files = uploader.get_uploaded_files()
        assert len(files) == 2
        assert 'test.jpg' in files
        assert 'document.pdf' in files
    
    def test_multiple_file_types(self, uploader, temp_dir):
        """测试多种文件类型"""
        # 测试所有支持的图片格式
        for ext in ['.jpg', '.jpeg', '.png', '.gif']:
            file_path = Path(temp_dir) / f'image{ext}'
            file_path.write_bytes(b'x' * 1024)
            result = uploader.upload(file_path)
            assert result['success'] is True
        
        # 测试所有支持的文档格式
        for ext in ['.pdf', '.doc', '.docx']:
            file_path = Path(temp_dir) / f'doc{ext}'
            file_path.write_bytes(b'x' * 1024)
            result = uploader.upload(file_path)
            assert result['success'] is True
    
    def test_case_insensitive_extension(self, uploader, temp_dir):
        """测试扩展名大小写不敏感"""
        # 创建大写扩展名的文件
        file_path = Path(temp_dir) / 'test.JPG'
        file_path.write_bytes(b'x' * 1024)
        
        result = uploader.upload(file_path)
        assert result['success'] is True
