from pyray import *

class Scene:
    def __init__(self, name):
        self.name = name
        self.contents = list()
        self.result = None
        self.offset = (0, 0)
    
    def draw(self):
        begin_drawing()
        clear_background(RAYWHITE)
        for item in self.contents:
            item.draw(self.offset)
        end_drawing()
    
    def on_start(self):
        pass

    def on_end(self):
        pass

    def on_key_press(self, key):
        pass

