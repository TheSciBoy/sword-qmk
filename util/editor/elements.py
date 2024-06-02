from pyray import *

class Element:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self):
        pass


class Rectangle(Element):
    def __init__(self, x: int, y: int, width: int, height: int, color: Color):
        super().__init__(x, y, width, height)
        self.color = color
    
    def draw(self):
        draw_rectangle(self.x, self.y, self.width, self.height, self.color)


class Text(Element):
    def __init__(self, x: int, y: int, text: str, size: int, color: Color):
        super().__init__(x, y, 0, 0)
        self.text = text
        self.size = size
        self.color = color
        self.width = measure_text(text, size)
        self.height = size


    def draw(self):
        draw_text(self.text, self.x, self.y, self.size, self.color)

