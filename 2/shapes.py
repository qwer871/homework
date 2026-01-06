# task3/shapes.py
import math
from abc import ABC, abstractmethod


class Shape(ABC):
    """Абстрактный базовый класс: фигура"""
    
    @abstractmethod
    def area(self) -> float:
        """Вычисляет площадь"""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Вычисляет периметр"""
        pass
    
    def area_greater_than(self, other_shape) -> bool:
        """Сравнивает, больше ли площадь другой фигуры"""
        return self.area() > other_shape.area()
    
    def area_less_than(self, other_shape) -> bool:
        """Сравнивает, меньше ли площадь другой фигуры"""
        return self.area() < other_shape.area()
    
    def perimeter_greater_than(self, other_shape) -> bool:
        """Сравнивает, больше ли периметр другой фигуры"""
        return self.perimeter() > other_shape.perimeter()
    
    def perimeter_less_than(self, other_shape) -> bool:
        """Сравнивает, меньше ли периметр другой фигуры"""
        return self.perimeter() < other_shape.perimeter()


class Square(Shape):
    """Квадрат"""
    
    def __init__(self, side: float):
        self.side = side
    
    def area(self) -> float:
        return self.side ** 2
    
    def perimeter(self) -> float:
        return 4 * self.side
    
    def __str__(self):
        return f"Square(side={self.side})"


class Rectangle(Shape):
    """Прямоугольник"""
    
    def __init__(self, length: float, width: float):
        self.length = length
        self.width = width
    
    def area(self) -> float:
        return self.length * self.width
    
    def perimeter(self) -> float:
        return 2 * (self.length + self.width)
    
    def __str__(self):
        return f"Rectangle(length={self.length}, width={self.width})"


class Triangle(Shape):
    """Треугольник (предполагается обычный треугольник, нужны длины трех сторон)"""
    
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c
    
    def area(self) -> float:
        # Используем формулу Герона
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def perimeter(self) -> float:
        return self.a + self.b + self.c
    
    def __str__(self):
        return f"Triangle(a={self.a}, b={self.b}, c={self.c})"


class Circle(Shape):
    """Круг"""
    
    def __init__(self, radius: float):
        self.radius = radius
    
    def area(self) -> float:
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * math.pi * self.radius
    
    def __str__(self):
        return f"Circle(radius={self.radius})"


# Тестовые примеры
if __name__ == "__main__":
    shapes = [
        Square(5),
        Rectangle(4, 6),
        Triangle(3, 4, 5),
        Circle(3)
    ]
    
    for shape in shapes:
        print(f"{shape}: площадь={shape.area():.2f}, периметр={shape.perimeter():.2f}")
    
    # Пример сравнения
    square = Square(5)
    circle = Circle(3)
    
    print(f"\nSquare vs Circle:")
    print(f"Площадь квадрата больше площади круга: {square.area_greater_than(circle)}")
    print(f"Периметр квадрата больше периметра круга: {square.perimeter_greater_than(circle)}")