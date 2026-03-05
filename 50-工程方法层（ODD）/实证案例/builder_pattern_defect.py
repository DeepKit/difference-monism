from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional


# Product - 要构建的复杂对象
class Computer:
    def __init__(self):
        self.cpu: Optional[str] = None
        self.ram: Optional[str] = None
        self.storage: Optional[str] = None
        self.gpu: Optional[str] = None
        self.os: Optional[str] = None
        
    def __str__(self) -> str:
        specs = []
        if self.cpu:
            specs.append(f"CPU: {self.cpu}")
        if self.ram:
            specs.append(f"RAM: {self.ram}")
        if self.storage:
            specs.append(f"Storage: {self.storage}")
        if self.gpu:
            specs.append(f"GPU: {self.gpu}")
        if self.os:
            specs.append(f"OS: {self.os}")
        return "Computer Specs:\n" + "\n".join(specs)


# Builder接口
class ComputerBuilder(ABC):
    def __init__(self):
        self.computer = Computer()
    
    @abstractmethod
    def build_cpu(self) -> ComputerBuilder:
        pass
    
    @abstractmethod
    def build_ram(self) -> ComputerBuilder:
        pass
    
    @abstractmethod
    def build_storage(self) -> ComputerBuilder:
        pass
    
    @abstractmethod
    def build_gpu(self) -> ComputerBuilder:
        pass
    
    @abstractmethod
    def build_os(self) -> ComputerBuilder:
        pass
    
    def get_computer(self) -> Computer:
        return self.computer


# 具体建造者 - 游戏电脑
class GamingComputerBuilder(ComputerBuilder):
    def build_cpu(self) -> ComputerBuilder:
        self.computer.cpu = "Intel i9-13900K"
        return self
    
    def build_ram(self) -> ComputerBuilder:
        self.computer.ram = "32GB DDR5"
        return self
    
    def build_storage(self) -> ComputerBuilder:
        self.computer.storage = "2TB NVMe SSD"
        return self
    
    def build_gpu(self) -> ComputerBuilder:
        self.computer.gpu = "NVIDIA RTX 4090"
        return self
    
    def build_os(self) -> ComputerBuilder:
        self.computer.os = "Windows 11"
        return self


# 具体建造者 - 办公电脑
class OfficeComputerBuilder(ComputerBuilder):
    def build_cpu(self) -> ComputerBuilder:
        self.computer.cpu = "Intel i5-12400"
        return self
    
    def build_ram(self) -> ComputerBuilder:
        self.computer.ram = "16GB DDR4"
        return self
    
    def build_storage(self) -> ComputerBuilder:
        self.computer.storage = "512GB SSD"
        return self
    
    def build_gpu(self) -> ComputerBuilder:
        self.computer.gpu = "Integrated Graphics"
        return self
    
    def build_os(self) -> ComputerBuilder:
        self.computer.os = "Windows 11 Pro"
        return self


# Director - 指导构建过程
class ComputerDirector:
    def __init__(self, builder: ComputerBuilder):
        self.builder = builder
    
    def build_full_computer(self) -> Computer:
        return (self.builder
                .build_cpu()
                .build_ram()
                .build_storage()
                .build_gpu()
                .build_os()
                .get_computer())
    
    def build_minimal_computer(self) -> Computer:
        return (self.builder
                .build_cpu()
                .build_ram()
                .build_storage()
                .get_computer())


# 使用示例
if __name__ == "__main__":
    # 方式1: 使用Director
    print("=== 使用Director构建 ===")
    gaming_builder = GamingComputerBuilder()
    director = ComputerDirector(gaming_builder)
    gaming_pc = director.build_full_computer()
    print(gaming_pc)
    print()
    
    # 方式2: 直接使用Builder（链式调用）
    print("=== 直接使用Builder ===")
    office_builder = OfficeComputerBuilder()
    office_pc = (office_builder
                 .build_cpu()
                 .build_ram()
                 .build_storage()
                 .build_gpu()
                 .build_os()
                 .get_computer())
    print(office_pc)
    print()
    
    # 方式3: 部分构建
    print("=== 部分构建 ===")
    custom_builder = GamingComputerBuilder()
    custom_pc = (custom_builder
                 .build_cpu()
                 .build_ram()
                 .build_gpu()
                 .get_computer())
    print(custom_pc)