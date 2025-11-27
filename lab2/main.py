from lab_python_oop.circle import Circle
from lab_python_oop.rectangle import Rectangle
from lab_python_oop.square import Square

from art import text2art
print(text2art("Shapes"))

rectangle = Rectangle(12, 12, "синий")
circle = Circle(12, "зеленый")
square = Square(12, "красный")

print(rectangle)
print(circle)
print(square)
