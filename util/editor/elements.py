import pyray

class Element:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self):
        pass


class Rectangle(Element):
    def __init__(self, x: int, y: int, width: int, height: int, color: pyray.Color):
        super().__init__(x, y, width, height)
        self.color = color
    
    def draw(self, offset):
        pyray.draw_rectangle_lines_ex(
            pyray.Rectangle(
                self.x + offset[0],
                self.y + offset[1],
                self.width,
                self.height
            ),
            1.5,
            self.color
        )


class Text(Element):
    def __init__(self, x: int, y: int, text: str, size: int, color: pyray.Color):
        super().__init__(x, y, 0, 0)
        self.text = text
        self.size = size
        self.color = color
        self.width = pyray.measure_text(text, size)
        self.height = size

    def draw(self, offset):
        x = self.x + offset[0]
        y = self.y + offset[1]
        pyray.draw_text(self.text, x, y, self.size, self.color)
