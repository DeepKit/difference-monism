from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import threading
import time


class BusError(Exception):
    """总线错误基类"""
    pass


class BusTimeoutError(BusError):
    """总线超时错误"""
    pass


class BusAddressError(BusError):
    """总线地址错误"""
    pass


class BusTransactionError(BusError):
    """总线事务错误"""
    pass


class BusState(Enum):
    """总线状态"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    LOCKED = "locked"


@dataclass
class BusTransaction:
    """总线事务"""
    address: int
    data: bytes
    operation: str  # 'read' or 'write'
    timestamp: float
    device_id: Optional[str] = None


class Device:
    """总线设备"""
    def __init__(self, device_id: str, base_address: int, address_range: int):
        self.device_id = device_id
        self.base_address = base_address
        self.address_range = address_range
        self.registers: Dict[int, int] = {}
        
    def is_address_valid(self, address: int) -> bool:
        """检查地址是否在设备范围内"""
        return self.base_address <= address < self.base_address + self.address_range
    
    def read_register(self, offset: int) -> int:
        """读取寄存器"""
        return self.registers.get(offset, 0)
    
    def write_register(self, offset: int, value: int):
        """写入寄存器"""
        self.registers[offset] = value


class ControlBus:
    """控制总线类"""
    
    def __init__(self, bus_width: int = 32, timeout: float = 1.0):
        self.bus_width = bus_width
        self.timeout = timeout
        self.state = BusState.IDLE
        self.devices: Dict[str, Device] = {}
        self.transaction_history: List[BusTransaction] = []
        self.lock = threading.RLock()
        self.interrupt_handlers: Dict[int, Callable] = {}
        self.max_address = (1 << bus_width) - 1
        
    def register_device(self, device: Device) -> bool:
        """注册设备到总线"""
        with self.lock:
            if device.device_id in self.devices:
                return False
            
            # 检查地址冲突
            for existing_device in self.devices.values():
                if self._address_overlap(device, existing_device):
                    raise BusAddressError(
                        f"地址冲突: {device.device_id} 与 {existing_device.device_id}"
                    )
            
            self.devices[device.device_id] = device
            return True
    
    def unregister_device(self, device_id: str) -> bool:
        """注销设备"""
        with self.lock:
            if device_id in self.devices:
                del self.devices[device_id]
                return True
            return False
    
    def read(self, address: int, size: int = 1) -> bytes:
        """从总线读取数据"""
        with self.lock:
            self._validate_address(address)
            self._wait_for_bus()
            
            try:
                self.state = BusState.BUSY
                device = self._find_device_by_address(address)
                
                if not device:
                    raise BusAddressError(f"地址 0x{address:X} 未映射到任何设备")
                
                offset = address - device.base_address
                data = bytearray()
                
                for i in range(size):
                    value = device.read_register(offset + i)
                    data.append(value & 0xFF)
                
                transaction = BusTransaction(
                    address=address,
                    data=bytes(data),
                    operation='read',
                    timestamp=time.time(),
                    device_id=device.device_id
                )
                self.transaction_history.append(transaction)
                
                return bytes(data)
                
            finally:
                self.state = BusState.IDLE
    
    def write(self, address: int, data: bytes) -> bool:
        """向总线写入数据"""
        with self.lock:
            self._validate_address(address)
            self._wait_for_bus()
            
            try:
                self.state = BusState.BUSY
                device = self._find_device_by_address(address)
                
                if not device:
                    raise BusAddressError(f"地址 0x{address:X} 未映射到任何设备")
                
                offset = address - device.base_address
                
                for i, byte in enumerate(data):
                    device.write_register(offset + i, byte)
                
                transaction = BusTransaction(
                    address=address,
                    data=data,
                    operation='write',
                    timestamp=time.time(),
                    device_id=device.device_id
                )
                self.transaction_history.append(transaction)
                
                return True
                
            finally:
                self.state = BusState.IDLE
    
    def read_word(self, address: int) -> int:
        """读取字（32位）"""
        data = self.read(address, 4)
        return int.from_bytes(data, byteorder='little')
    
    def write_word(self, address: int, value: int):
        """写入字（32位）"""
        data = value.to_bytes(4, byteorder='little')
        self.write(address, data)
    
    def read_halfword(self, address: int) -> int:
        """读取半字（16位）"""
        data = self.read(address, 2)
        return int.from_bytes(data, byteorder='little')
    
    def write_halfword(self, address: int, value: int):
        """写入半字（16位）"""
        data = value.to_bytes(2, byteorder='little')
        self.write(address, data)
    
    def read_byte(self, address: int) -> int:
        """读取字节（8位）"""
        data = self.read(address, 1)
        return data[0]
    
    def write_byte(self, address: int, value: int):
        """写入字节（8位）"""
        self.write(address, bytes([value & 0xFF]))
    
    def register_interrupt(self, interrupt_id: int, handler: Callable):
        """注册中断处理函数"""
        with self.lock:
            self.interrupt_handlers[interrupt_id] = handler
    
    def trigger_interrupt(self, interrupt_id: int, *args, **kwargs):
        """触发中断"""
        handler = self.interrupt_handlers.get(interrupt_id)
        if handler:
            handler(*args, **kwargs)
    
    def reset(self):
        """重置总线"""
        with self.lock:
            self.state = BusState.IDLE
            for device in self.devices.values():
                device.registers.clear()
            self.transaction_history.clear()
    
    def get_transaction_history(self, device_id: Optional[str] = None) -> List[BusTransaction]:
        """获取事务历史"""
        if device_id:
            return [t for t in self.transaction_history if t.device_id == device_id]
        return self.transaction_history.copy()
    
    def _validate_address(self, address: int):
        """验证地址有效性"""
        if address < 0 or address > self.max_address:
            raise BusAddressError(f"地址 0x{address:X} 超出范围")
    
    def _wait_for_bus(self):
        """等待总线空闲"""
        start_time = time.time()
        while self.state == BusState.BUSY:
            if time.time() - start_time > self.timeout:
                raise BusTimeoutError("总线超时")
            time.sleep(0.001)
    
    def _find_device_by_address(self, address: int) -> Optional[Device]:
        """根据地址查找设备"""
        for device in self.devices.values():
            if device.is_address_valid(address):
                return device
        return None
    
    def _address_overlap(self, device1: Device, device2: Device) -> bool:
        """检查两个设备地址是否重叠"""
        range1_start = device1.base_address
        range1_end = device1.base_address + device1.address_range - 1
        range2_start = device2.base_address
        range2_end = device2.base_address + device2.address_range - 1
        
        return not (range1_end < range2_start or range2_end < range1_start)


# 使用示例
if __name__ == "__main__":
    # 创建总线
    bus = ControlBus(bus_width=32, timeout=2.0)
    
    # 创建设备
    device1 = Device("UART", base_address=0x1000, address_range=0x100)
    device2 = Device("GPIO", base_address=0x2000, address_range=0x100)
    
    # 注册设备
    bus.register_device(device1)
    bus.register_device(device2)
    
    # 写入数据
    bus.write_byte(0x1000, 0x42)
    bus.write_word(0x2000, 0xDEADBEEF)
    
    # 读取数据
    value1 = bus.read_byte(0x1000)
    value2 = bus.read_word(0x2000)
    
    print(f"读取字节: 0x{value1:X}")
    print(f"读取字: 0x{value2:X}")
    
    # 查看事务历史
    for transaction in bus.get_transaction_history():
        print(f"{transaction.operation} @ 0x{transaction.address:X}: {transaction.data.hex()}")