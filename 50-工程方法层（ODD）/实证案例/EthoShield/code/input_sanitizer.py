"""
ASTO MVP 1.0 - 招聘公平防火墙
输入盲化器 (Input Sanitizer)
"""

from typing import List, Dict, Any, Set, Optional


class InputSanitizer:
    """
    输入盲化器 - 删除敏感字段和代理变量
    
    这是属集空间约束的工程化表达：
    - 删除显式敏感字段
    - 删除高相关代理变量
    """
    
    def __init__(self, protected_attrs: Optional[List[str]] = None, proxy_attrs: Optional[List[str]] = None):
        """
        初始化盲化器
        
        Args:
            protected_attrs: 显式敏感属性列表
            proxy_attrs: 代理变量列表
        """
        default_protected: List[str] = [
            'gender',        # 性别
            'ethnicity',     # 民族
            'age',           # 年龄
            'religion',      # 宗教
            'birthdate',     # 出生日期
            'marital',       # 婚姻状况
            'disability',    # 残疾
        ]
        
        default_proxy: List[str] = [
            'school',        # 学校（暗示阶层)
            'birthplace',    # 籍贯
            'zipcode',       # 邮政编码
            'address',       # 地址
            'phone_prefix',  # 电话区号
        ]
        
        # 显式敏感属性
        self.protected_attrs: Set[str] = set(protected_attrs if protected_attrs else default_protected)
        # 代理变量
        self.proxy_attrs: Set[str] = set(proxy_attrs if proxy_attrs else default_proxy)
    
    def sanitize(self, resume: Dict[str, Any]) -> Dict[str, Any]:
        """
        单条简历盲化
        
        Args:
            resume: 原始简历数据
            
        Returns:
            盲化后的简历
        """
        sanitized = resume.copy()
        
        # 删除显式敏感属性
        for attr in self.protected_attrs:
            sanitized.pop(attr, None)
        
        # 删除代理变量
        for attr in self.proxy_attrs:
            sanitized.pop(attr, None)
        
        return sanitized
    
    def batch_sanitize(self, resumes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量盲化
        
        Args:
            resumes: 原始简历列表
            
        Returns:
            盲化后的简历列表
        """
        return [self.sanitize(r) for r in resumes]
    
    def add_protected(self, attr: str):
        """添加敏感属性"""
        self.protected_attrs.add(attr)
    
    def add_proxy(self, attr: str):
        """添加代理变量"""
        self.proxy_attrs.add(attr)
    
    def get_removed_fields(self) -> Dict[str, List[str]]:
        """获取被移除的字段信息"""
        return {
            'protected': list(self.protected_attrs),
            'proxies': list(self.proxy_attrs)
        }


def generate_mock_resumes(n: int = 100) -> List[Dict[str, Any]]:
    """
    生成模拟简历数据
    
    Args:
        n: 生成数量
        
    Returns:
        简历列表
    """
    import random
    
    schools = ['北大', '清华', '复旦', '浙大', '交大', '普本', '大专', '海外']
    genders = ['男', '女']
    ethnicities = ['汉族', '少数民族']
    jobs = ['工程师', '产品经理', '设计师', '运营', '销售']
    
    resumes = []
    for i in range(n):
        school = random.choice(schools)
        gender = random.choice(genders)
        ethnicity = random.choice(ethnicities)
        
        resume: Dict[str, Any] = {
            'id': i + 1,
            'name': f'候选人{i+1}',
            'gender': gender,
            'ethnicity': ethnicity,
            'age': random.randint(22, 45),
            'school': school,
            'education': random.choice(['本科', '硕士', '博士']),
            'exp': random.randint(0, 15),
            'position': random.choice(jobs),
        }
        # 模拟偏见：学校好的更容易被录用
        resume['hired'] = random.random() < (0.3 + 0.4 * (schools.index(school) / len(schools)))
        resumes.append(resume)
    
    return resumes


if __name__ == '__main__':
    # 测试
    sanitizer = InputSanitizer()
    
    # 生成测试数据
    resumes = generate_mock_resumes(10)
    
    print("=== 原始数据 (前3条) ===")
    for r in resumes[:3]:
        print(r)
    
    print("\n=== 盲化后数据 (前3条) ===")
    sanitized = sanitizer.batch_sanitize(resumes)
    for r in sanitized[:3]:
        print(r)
    
    print("\n=== 被移除的字段 ===")
    print(sanitizer.get_removed_fields())
