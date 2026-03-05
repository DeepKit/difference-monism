from abc import ABC, abstractmethod


# Implementation interface
class DrawingAPI(ABC):
    @abstractmethod
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        pass
    
    @abstractmethod
    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> None:
        pass


# Concrete Implementations
class DrawingAPI1(DrawingAPI):
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        print(f"API1.circle at ({x}, {y}) with radius {radius}")
    
    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> None:
        print(f"API1.rectangle at ({x}, {y}) with width {width} and height {height}")


class DrawingAPI2(DrawingAPI):
    def draw_circle(self, x: float, y: float, radius: float) -> None:
        print(f"API2.circle at ({x}:{y}) radius={radius}")
    
    def draw_rectangle(self, x: float, y: float, width: float, height: float) -> None:
        print(f"API2.rectangle at ({x}:{y}) size={width}x{height}")


# Abstraction
class Shape(ABC):
    def __init__(self, drawing_api: DrawingAPI):
        self._drawing_api = drawing_api
    
    @abstractmethod
    def draw(self) -> None:
        pass
    
    @abstractmethod
    def resize(self, factor: float) -> None:
        pass


# Refined Abstractions
class Circle(Shape):
    def __init__(self, x: float, y: float, radius: float, drawing_api: DrawingAPI):
        super().__init__(drawing_api)
        self._x = x
        self._y = y
        self._radius = radius
    
    def draw(self) -> None:
        self._drawing_api.draw_circle(self._x, self._y, self._radius)
    
    def resize(self, factor: float) -> None:
        self._radius *= factor


class Rectangle(Shape):
    def __init__(self, x: float, y: float, width: float, height: float, drawing_api: DrawingAPI):
        super().__init__(drawing_api)
        self._x = x
        self._y = y
        self._width = width
        self._height = height
    
    def draw(self) -> None:
        self._drawing_api.draw_rectangle(self._x, self._y, self._width, self._height)
    
    def resize(self, factor: float) -> None:
        self._width *= factor
        self._height *= factor


# Client code
if __name__ == "__main__":
    shapes = [
        Circle(1, 2, 3, DrawingAPI1()),
        Circle(5, 7, 11, DrawingAPI2()),
        Rectangle(1, 2, 4, 5, DrawingAPI1()),
        Rectangle(3, 4, 6, 8, DrawingAPI2())
    ]
    
    for shape in shapes:
        shape.draw()
        shape.resize(2)
        shape.draw()