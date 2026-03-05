import uuid
from typing import Dict, Tuple, Optional
from pathlib import Path

class FileUploader:
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    def __init__(self, upload_dir: str = './uploads'):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.uploaded_files: Dict[str, Dict] = {}
        self.file_index: Dict[Tuple[str, int], str] = {}
    
    def _get_file_extension(self, filename: str) -> str:
        return Path(filename).suffix.lower().lstrip('.')
    
    def _validate_file_type(self, filename: str) -> Tuple[bool, Optional[str]]:
        extension = self._get_file_extension(filename)
        if extension not in self.ALLOWED_EXTENSIONS:
            return False, f"不支持的文件类型：{extension}"
        return True, None
    
    def _validate_file_size(self, file_size: int) -> Tuple[bool, Optional[str]]:
        if file_size > self.MAX_FILE_SIZE:
            return False, f"文件过大，最大允许：{self.MAX_FILE_SIZE // (1024*1024)}MB"
        return True, None
    
    def _check_duplicate(self, filename: str, file_size: int) -> Optional[str]:
        key = (filename, file_size)
        return self.file_index.get(key)
    
    def upload(self, filename: str, file_size: int, file_data: bytes = None) -> Dict:
        is_valid_type, type_error = self._validate_file_type(filename)
        if not is_valid_type:
            return {'success': False, 'message': type_error, 'error': 'INVALID_FILE_TYPE'}
        
        is_valid_size, size_error = self._validate_file_size(file_size)
        if not is_valid_size:
            return {'success': False, 'message': size_error, 'error': 'FILE_TOO_LARGE'}
        
        existing_file_id = self._check_duplicate(filename, file_size)
        if existing_file_id:
            return {'success': False, 'message': f"文件已存在", 'error': 'DUPLICATE_FILE', 'existing_file_id': existing_file_id}
        
        file_id = str(uuid.uuid4())
        file_type = self._get_file_extension(filename)
        
        self.uploaded_files[file_id] = {'name': filename, 'size': file_size, 'type': file_type}
        self.file_index[(filename, file_size)] = file_id
        
        if file_data:
            file_path = self.upload_dir / f"{file_id}.{file_type}"
            file_path.write_bytes(file_data)
        
        return {'success': True, 'message': '文件上传成功', 'file_id': file_id, 'filename': filename, 'size': file_size, 'type': file_type}
    
    def get_file_info(self, file_id: str) -> Optional[Dict]:
        return self.uploaded_files.get(file_id)
