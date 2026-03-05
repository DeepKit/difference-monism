from abc import ABC, abstractmethod
from typing import Any, Callable, Optional
from queue import Queue
from threading import Thread
import time


class Message:
    """消息封装类"""
    def __init__(self, payload: Any, headers: Optional[dict] = None):
        self.payload = payload
        self.headers = headers or {}
        self.timestamp = time.time()


class Channel:
    """通道类"""
    def __init__(self, name: str):
        self.name = name
        self.queue = Queue()
    
    def send(self, message: Message):
        self.queue.put(message)
    
    def receive(self, timeout: Optional[float] = None) -> Optional[Message]:
        try:
            return self.queue.get(timeout=timeout)
        except:
            return None


class ChannelAdapter(ABC):
    """通道适配器基类"""
    def __init__(self, channel: Channel):
        self.channel = channel
        self.running = False
    
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass


class InboundChannelAdapter(ChannelAdapter):
    """入站通道适配器"""
    def __init__(self, channel: Channel, source: Callable[[], Any], interval: float = 1.0):
        super().__init__(channel)
        self.source = source
        self.interval = interval
        self.thread = None
    
    def start(self):
        self.running = True
        self.thread = Thread(target=self._poll)
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _poll(self):
        while self.running:
            try:
                data = self.source()
                if data is not None:
                    message = Message(data)
                    self.channel.send(message)
            except Exception as e:
                print(f"入站适配器错误: {e}")
            time.sleep(self.interval)


class OutboundChannelAdapter(ChannelAdapter):
    """出站通道适配器"""
    def __init__(self, channel: Channel, handler: Callable[[Any], None]):
        super().__init__(channel)
        self.handler = handler
        self.thread = None
    
    def start(self):
        self.running = True
        self.thread = Thread(target=self._consume)
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _consume(self):
        while self.running:
            message = self.channel.receive(timeout=0.5)
            if message:
                try:
                    self.handler(message.payload)
                except Exception as e:
                    print(f"出站适配器错误: {e}")


class TransformingChannelAdapter(ChannelAdapter):
    """转换通道适配器"""
    def __init__(self, input_channel: Channel, output_channel: Channel, 
                 transformer: Callable[[Any], Any]):
        super().__init__(input_channel)
        self.output_channel = output_channel
        self.transformer = transformer
        self.thread = None
    
    def start(self):
        self.running = True
        self.thread = Thread(target=self._transform)
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
    
    def _transform(self):
        while self.running:
            message = self.channel.receive(timeout=0.5)
            if message:
                try:
                    transformed = self.transformer(message.payload)
                    new_message = Message(transformed, message.headers)
                    self.output_channel.send(new_message)
                except Exception as e:
                    print(f"转换适配器错误: {e}")


# 使用示例
if __name__ == "__main__":
    # 创建通道
    input_channel = Channel("input")
    output_channel = Channel("output")
    
    # 数据源函数
    counter = [0]
    def data_source():
        counter[0] += 1
        return f"数据-{counter[0]}"
    
    # 数据处理函数
    def data_handler(data):
        print(f"处理: {data}")
    
    # 转换函数
    def transformer(data):
        return data.upper()
    
    # 创建适配器
    inbound = InboundChannelAdapter(input_channel, data_source, interval=2.0)
    transform = TransformingChannelAdapter(input_channel, output_channel, transformer)
    outbound = OutboundChannelAdapter(output_channel, data_handler)
    
    # 启动
    inbound.start()
    transform.start()
    outbound.start()
    
    # 运行10秒
    time.sleep(10)
    
    # 停止
    inbound.stop()
    transform.stop()
    outbound.stop()