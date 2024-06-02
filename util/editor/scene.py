from pyray import *

class Scene:
    def __init__(self, name):
        self.name = name
        self.contents = list()
    
    def draw(self):
        begin_drawing()
        clear_background(RAYWHITE)
        for item in self.contents:
            item.draw()
        end_drawing()
