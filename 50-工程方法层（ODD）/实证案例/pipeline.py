from typing import Any, Callable, List, Optional
from functools import wraps


class Pipeline:
    """管道模式实现类"""
    
    def __init__(self, name: str = "Pipeline"):
        self.name = name
        self.stages: List[Callable] = []
    
    def add_stage(self, stage: Callable) -> 'Pipeline':
        """添加管道阶段"""
        self.stages.append(stage)
        return self
    
    def pipe(self, stage: Callable) -> 'Pipeline':
        """添加管道阶段（别名方法）"""
        return self.add_stage(stage)
    
    def execute(self, data: Any) -> Any:
        """执行管道处理"""
        result = data
        for i, stage in enumerate(self.stages):
            try:
                result = stage(result)
            except Exception as e:
                raise PipelineError(
                    f"Stage {i} ({stage.__name__}) failed: {str(e)}"
                ) from e
        return result
    
    def __call__(self, data: Any) -> Any:
        """使管道对象可调用"""
        return self.execute(data)
    
    def clear(self) -> 'Pipeline':
        """清空所有阶段"""
        self.stages.clear()
        return self
    
    def __len__(self) -> int:
        """返回管道阶段数量"""
        return len(self.stages)
    
    def __repr__(self) -> str:
        return f"Pipeline(name='{self.name}', stages={len(self.stages)})"


class PipelineError(Exception):
    """管道执行异常"""
    pass


def stage(func: Callable) -> Callable:
    """装饰器：标记函数为管道阶段"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.is_stage = True
    return wrapper


# 使用示例
if __name__ == "__main__":
    # 示例1：数据处理管道
    @stage
    def add_ten(x):
        return x + 10
    
    @stage
    def multiply_by_two(x):
        return x * 2
    
    @stage
    def to_string(x):
        return f"Result: {x}"
    
    pipeline = Pipeline("Math Pipeline")
    pipeline.add_stage(add_ten).add_stage(multiply_by_two).add_stage(to_string)
    
    result = pipeline.execute(5)
    print(result)  # Output: Result: 30
    
    # 示例2：文本处理管道
    text_pipeline = (
        Pipeline("Text Pipeline")
        .pipe(lambda s: s.strip())
        .pipe(lambda s: s.lower())
        .pipe(lambda s: s.replace(" ", "_"))
        .pipe(lambda s: f"{s}.txt")
    )
    
    filename = text_pipeline("  Hello World  ")
    print(filename)  # Output: hello_world.txt
    
    # 示例3：列表处理管道
    list_pipeline = Pipeline("List Pipeline")
    list_pipeline.pipe(lambda lst: [x * 2 for x in lst])
    list_pipeline.pipe(lambda lst: [x for x in lst if x > 10])
    list_pipeline.pipe(sorted)
    
    numbers = list_pipeline([1, 5, 8, 12, 3])
    print(numbers)  # Output: [12, 16, 24]