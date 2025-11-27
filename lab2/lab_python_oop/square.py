from lab_python_oop.rectangle import Rectangle

class Square(Rectangle):
    def __init__(self, length, color):
        super().__init__(length, length, color)
        self._length = length
    
    def area(self):
        return self._length * self._length
    
    def __repr__(self):
        return f"{self._color} квадрат со стороной {self._length} и площадью {self.area()}"
