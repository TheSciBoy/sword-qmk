import time

from pyray import *


class Scene:
    def __init__(self, name):
        self.name = name
        self.contents = list()
        self.result = None
        self.offset = (0, 0)
        self.key_timer = dict()
    
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

    def on_key_press(self, key) -> str:
        self.key_timer[key] = time.perf_counter() + 0.5
        return self.trigger_key(key)

    def trigger_key(self, key) -> str:
        return None

    def execute(self):
        return_value = None
        keys_to_remove = list()
        for key, timeout in self.key_timer.items():
            if is_key_down(key):
                if timeout < time.perf_counter():
                    return_value = self.trigger_key(key)
                    self.key_timer[key] = time.perf_counter() + 0.05
            else:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            del self.key_timer[key]
        return return_value
