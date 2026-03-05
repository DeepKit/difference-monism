import re
from typing import Callable, Dict, List, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class Route:
    path: str
    handler: Callable
    methods: List[str]
    pattern: re.Pattern
    param_names: List[str]


class Router:
    def __init__(self):
        self.routes: List[Route] = []
        self.middlewares: List[Callable] = []
    
    def add_route(self, path: str, handler: Callable, methods: List[str] = None):
        if methods is None:
            methods = ['GET']
        
        param_names = re.findall(r'<(\w+)>', path)
        pattern_str = re.sub(r'<\w+>', r'([^/]+)', path)
        pattern_str = f'^{pattern_str}$'
        pattern = re.compile(pattern_str)
        
        route = Route(
            path=path,
            handler=handler,
            methods=[m.upper() for m in methods],
            pattern=pattern,
            param_names=param_names
        )
        self.routes.append(route)
    
    def get(self, path: str):
        def decorator(handler: Callable):
            self.add_route(path, handler, ['GET'])
            return handler
        return decorator
    
    def post(self, path: str):
        def decorator(handler: Callable):
            self.add_route(path, handler, ['POST'])
            return handler
        return decorator
    
    def put(self, path: str):
        def decorator(handler: Callable):
            self.add_route(path, handler, ['PUT'])
            return handler
        return decorator
    
    def delete(self, path: str):
        def decorator(handler: Callable):
            self.add_route(path, handler, ['DELETE'])
            return handler
        return decorator
    
    def use(self, middleware: Callable):
        self.middlewares.append(middleware)
    
    def match(self, path: str, method: str = 'GET') -> Optional[Tuple[Callable, Dict[str, str]]]:
        method = method.upper()
        
        for route in self.routes:
            if method not in route.methods:
                continue
            
            match = route.pattern.match(path)
            if match:
                params = dict(zip(route.param_names, match.groups()))
                return route.handler, params
        
        return None
    
    def dispatch(self, path: str, method: str = 'GET', **kwargs) -> Any:
        result = self.match(path, method)
        
        if result is None:
            raise ValueError(f"No route found for {method} {path}")
        
        handler, params = result
        kwargs.update(params)
        
        # 执行中间件
        for middleware in self.middlewares:
            middleware_result = middleware(path, method, kwargs)
            if middleware_result is not None:
                return middleware_result
        
        return handler(**kwargs)


# 使用示例
if __name__ == '__main__':
    router = Router()
    
    @router.get('/users')
    def list_users():
        return {'users': ['Alice', 'Bob']}
    
    @router.get('/users/<user_id>')
    def get_user(user_id):
        return {'user_id': user_id}
    
    @router.post('/users')
    def create_user():
        return {'status': 'created'}
    
    # 中间件示例
    def auth_middleware(path, method, kwargs):
        print(f"Auth check for {method} {path}")
        return None
    
    router.use(auth_middleware)
    
    # 测试
    print(router.dispatch('/users', 'GET'))
    print(router.dispatch('/users/123', 'GET'))
    print(router.dispatch('/users', 'POST'))