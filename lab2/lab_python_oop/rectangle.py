from lab_python_oop.shape import Shape
from lab_python_oop.color import Color

class Rectangle(Shape):
    def __init__(self, width, height, color):
        self._width = width
        self._height = height
        self._color = Color(color)

    def area(self):
        return self._width * self._height
    
    def __repr__(self):
        return f"{self._color} прямоугольник шириной {self._width}, высотой {self._height} и площадью {self.area()}"
    