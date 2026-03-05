from typing import Optional, List, Tuple, Union, Callable
from datetime import datetime, date
from enum import Enum
import re
from functools import total_ordering
import warnings


class VersioningScheme(Enum):
    """版本控制方案枚举"""
    SEMANTIC = "semantic"  # 语义化版本 (e.g., 1.2.3)
    DATE = "date"  # 日期版本 (e.g., 2024-01-15)
    SEQUENTIAL = "sequential"  # 序列版本 (e.g., v1, v2)


class APIVersionError(Exception):
    """API版本相关错误基类"""
    pass


class InvalidVersionError(APIVersionError):
    """无效版本错误"""
    pass


class VersionNotSupportedError(APIVersionError):
    """版本不支持错误"""
    pass


class VersionDeprecatedError(APIVersionError):
    """版本已弃用错误"""
    pass


@total_ordering
class Version:
    """版本类，支持多种版本格式"""
    
    def __init__(self, version_string: str, scheme: VersioningScheme = VersioningScheme.SEMANTIC):
        self.raw_version = version_string
        self.scheme = scheme
        self._parse_version()
    
    def _parse_version(self):
        """解析版本字符串"""
        try:
            if self.scheme == VersioningScheme.SEMANTIC:
                self._parse_semantic()
            elif self.scheme == VersioningScheme.DATE:
                self._parse_date()
            elif self.scheme == VersioningScheme.SEQUENTIAL:
                self._parse_sequential()
            else:
                raise InvalidVersionError(f"不支持的版本方案: {self.scheme}")
        except Exception as e:
            raise InvalidVersionError(f"无法解析版本 '{self.raw_version}': {str(e)}")
    
    def _parse_semantic(self):
        """解析语义化版本 (major.minor.patch[-prerelease][+build])"""
        pattern = r'^v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.-]+))?(?:\+([a-zA-Z0-9.-]+))?$'
        match = re.match(pattern, self.raw_version)
        
        if not match:
            raise InvalidVersionError(f"无效的语义化版本格式: {self.raw_version}")
        
        self.major = int(match.group(1))
        self.minor = int(match.group(2))
        self.patch = int(match.group(3))
        self.prerelease = match.group(4) or ""
        self.build = match.group(5) or ""
    
    def _parse_date(self):
        """解析日期版本 (YYYY-MM-DD)"""
        try:
            self.date_value = datetime.strptime(self.raw_version, "%Y-%m-%d").date()
        except ValueError:
            raise InvalidVersionError(f"无效的日期版本格式: {self.raw_version}")
    
    def _parse_sequential(self):
        """解析序列版本 (v1, v2, etc.)"""
        pattern = r'^v?(\d+)$'
        match = re.match(pattern, self.raw_version)
        
        if not match:
            raise InvalidVersionError(f"无效的序列版本格式: {self.raw_version}")
        
        self.sequence = int(match.group(1))
    
    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        if self.scheme != other.scheme:
            return False
        
        if self.scheme == VersioningScheme.SEMANTIC:
            return (self.major, self.minor, self.patch, self.prerelease) == \
                   (other.major, other.minor, other.patch, other.prerelease)
        elif self.scheme == VersioningScheme.DATE:
            return self.date_value == other.date_value
        elif self.scheme == VersioningScheme.SEQUENTIAL:
            return self.sequence == other.sequence
    
    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        if self.scheme != other.scheme:
            raise ValueError("无法比较不同版本方案的版本")
        
        if self.scheme == VersioningScheme.SEMANTIC:
            if (self.major, self.minor, self.patch) != (other.major, other.minor, other.patch):
                return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
            # 处理预发布版本
            if not self.prerelease and other.prerelease:
                return False
            if self.prerelease and not other.prerelease:
                return True
            return self.prerelease < other.prerelease
        elif self.scheme == VersioningScheme.DATE:
            return self.date_value < other.date_value
        elif self.scheme == VersioningScheme.SEQUENTIAL:
            return self.sequence < other.sequence
    
    def __str__(self):
        return self.raw_version
    
    def __repr__(self):
        return f"Version('{self.raw_version}', scheme={self.scheme})"


class APIVersioning:
    """API版本控制管理类"""
    
    def __init__(self, scheme: VersioningScheme = VersioningScheme.SEMANTIC):
        self.scheme = scheme
        self.supported_versions: List[Version] = []
        self.deprecated_versions: dict[Version, Optional[str]] = {}
        self.sunset_versions: dict[Version, Optional[date]] = {}
        self.default_version: Optional[Version] = None
        self.version_handlers: dict[Version, Callable] = {}
    
    def add_version(self, version_string: str, is_default: bool = False) -> Version:
        """添加支持的版本"""
        try:
            version = Version(version_string, self.scheme)
            
            if version in self.supported_versions:
                warnings.warn(f"版本 {version_string} 已存在")
                return version
            
            self.supported_versions.append(version)
            self.supported_versions.sort()
            
            if is_default or self.default_version is None:
                self.default_version = version
            
            return version
        except InvalidVersionError as e:
            raise InvalidVersionError(f"添加版本失败: {str(e)}")
    
    def remove_version(self, version_string: str):
        """移除版本"""
        version = Version(version_string, self.scheme)
        
        if version not in self.supported_versions:
            raise VersionNotSupportedError(f"版本 {version_string} 不存在")
        
        self.supported_versions.remove(version)
        
        if version in self.deprecated_versions:
            del self.deprecated_versions[version]
        if version in self.sunset_versions:
            del self.sunset_versions[version]
        if version in self.version_handlers:
            del self.version_handlers[version]
        
        if self.default_version == version:
            self.default_version = self.supported_versions[-1] if self.supported_versions else None
    
    def deprecate_version(self, version_string: str, reason: Optional[str] = None):
        """标记版本为已弃用"""
        version = Version(version_string, self.scheme)
        
        if version not in self.supported_versions:
            raise VersionNotSupportedError(f"版本 {version_string} 不存在")
        
        self.deprecated_versions[version] = reason
    
    def sunset_version(self, version_string: str, sunset_date: Optional[date] = None):
        """设置版本的日落日期（停止支持日期）"""
        version = Version(version_string, self.scheme)
        
        if version not in self.supported_versions:
            raise VersionNotSupportedError(f"版本 {version_string} 不存在")
        
        self.sunset_versions[version] = sunset_date
    
    def is_supported(self, version_string: str) -> bool:
        """检查版本是否受支持"""
        try:
            version = Version(version_string, self.scheme)
            return version in self.supported_versions
        except InvalidVersionError:
            return False
    
    def is_deprecated(self, version_string: str) -> bool:
        """检查版本是否已弃用"""
        try:
            version = Version(version_string, self.scheme)
            return version in self.deprecated_versions
        except InvalidVersionError:
            return False
    
    def is_sunset(self, version_string: str) -> bool:
        """检查版本是否已到日落日期"""
        try:
            version = Version(version_string, self.scheme)
            if version not in self.sunset_versions:
                return False
            
            sunset_date = self.sunset_versions[version]
            if sunset_date is None:
                return False
            
            return date.today() >= sunset_date
        except InvalidVersionError:
            return False
    
    def get_latest_version(self) -> Optional[Version]:
        """获取最新版本"""
        if not self.supported_versions:
            return None
        return max(self.supported_versions)
    
    def get_version_info(self, version_string: str) -> dict:
        """获取版本详细信息"""
        version = Version(version_string, self.scheme)
        
        if version not in self.supported_versions:
            raise VersionNotSupportedError(f"版本 {version_string} 不受支持")
        
        info = {
            "version": str(version),
            "scheme": self.scheme.value,
            "supported": True,
            "deprecated": version in self.deprecated_versions,
            "deprecation_reason": self.deprecated_versions.get(version),
            "sunset_date": self.sunset_versions.get(version),
            "is_sunset": self.is_sunset(version_string),
            "is_default": version == self.default_version,
            "is_latest": version == self.get_latest_version()
        }
        
        return info
    
    def negotiate_version(self, requested_version: Optional[str] = None) -> Version:
        """协商版本，返回最合适的版本"""
        if not self.supported_versions:
            raise VersionNotSupportedError("没有可用的API版本")
        
        # 如果没有请求特定版本，返回默认版本
        if requested_version is None:
            if self.default_version is None:
                raise APIVersionError("未设置默认版本")
            return self.default_version
        
        try:
            version = Version(requested_version, self.scheme)
        except InvalidVersionError as e:
            raise InvalidVersionError(f"请求的版本格式无效: {str(e)}")
        
        # 检查版本是否受支持
        if version not in self.supported_versions:
            # 尝试找到最接近的较新版本
            newer_versions = [v for v in self.supported_versions if v > version]
            if newer_versions:
                return min(newer_versions)
            raise VersionNotSupportedError(
                f"版本 {requested_version} 不受支持。"
                f"支持的版本: {', '.join(str(v) for v in self.supported_versions)}"
            )
        
        # 检查是否已日落
        if self.is_sunset(requested_version):
            raise VersionNotSupportedError(
                f"版本 {requested_version} 已停止支持（日落日期: {self.sunset_versions[version]}）"
            )
        
        # 如果版本已弃用，发出警告
        if version in self.deprecated_versions:
            reason = self.deprecated_versions[version]
            warning_msg = f"版本 {requested_version} 已弃用"
            if reason:
                warning_msg += f": {reason}"
            warnings.warn(warning_msg, DeprecationWarning)
        
        return version
    
    def register_handler(self, version_string: str, handler: Callable):
        """为特定版本注册处理器"""
        version = Version(version_string, self.scheme)
        
        if version not in self.supported_versions:
            raise VersionNotSupportedError(f"版本 {version_string} 不受支持")
        
        self.version_handlers[version] = handler
    
    def get_handler(self, version_string: str) -> Optional[Callable]:
        """获取版本对应的处理器"""
        version = Version(version_string, self.scheme)
        return self.version_handlers.get(version)
    
    def list_versions(self, include_deprecated: bool = True) -> List[dict]:
        """列出所有版本及其状态"""
        versions = []
        for version in self.supported_versions:
            if not include_deprecated and version in self.deprecated_versions:
                continue
            versions.append(self.get_version_info(str(version)))
        return versions
    
    def validate_version_range(self, min_version: str, max_version: str) -> bool:
        """验证版本范围"""
        try:
            min_v = Version(min_version, self.scheme)
            max_v = Version(max_version, self.scheme)
            return min_v <= max_v
        except InvalidVersionError:
            return False
    
    def get_versions_in_range(self, min_version: str, max_version: str) -> List[Version]:
        """获取指定范围内的所有版本"""
        min_v = Version(min_version, self.scheme)
        max_v = Version(max_version, self.scheme)
        
        if min_v > max_v:
            raise ValueError(f"最小版本 {min_version} 大于最大版本 {max_version}")
        
        return [v for v in self.supported_versions if min_v <= v <= max_v]


# 使用示例
if __name__ == "__main__":
    # 创建语义化版本控制
    api = APIVersioning(VersioningScheme.SEMANTIC)
    
    # 添加版本
    api.add_version("1.0.0")
    api.add_version("1.1.0")
    api.add_version("2.0.0", is_default=True)
    api.add_version("2.1.0")
    
    # 标记弃用
    api.deprecate_version("1.0.0", "请升级到2.x版本")
    
    # 设置日落日期
    api.sunset_version("1.0.0", date(2024, 12, 31))
    
    # 版本协商
    try:
        version = api.negotiate_version("2.0.0")
        print(f"协商版本: {version}")
        
        # 获取版本信息
        info = api.get_version_info("1.0.0")
        print(f"版本信息: {info}")
        
        # 列出所有版本
        all_versions = api.list_versions()
        print(f"所有版本: {all_versions}")
        
    except APIVersionError as e:
        print(f"错误: {e}")