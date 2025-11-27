from math import pi

from lab_python_oop.shape import Shape

class Circle(Shape):
    def __init__(self, radius, color):
        self._radius = radius
        self._color = color
    
    def area(self):
        return pi * self._radius * self._radius
    
    def __repr__(self):
        return f"{self._color} круг радиусом {self._radius} и площадью {self.area()}"
