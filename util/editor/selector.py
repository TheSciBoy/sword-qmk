import scene

import elements

from pyray import *


class Selector(scene.Scene):
    def __init__(self, name: str, items: list, page_height: int):
        super().__init__(name)
        self.selected = 0
        self.font_size = 20
        self.selected_color = RED
        self.unselected_color = BLACK
        self.y = 0
        self.result = None
        self._page_size = page_height // self.font_size
        for item in items:
            row = elements.Text(
                0,
                self.y,
                item,
                self.font_size,
                self.unselected_color
            )
            self.contents.append(row)
            self.y += row.height

    def draw(self):
        self.contents[self.selected].color = self.selected_color
        super().draw()
        self.contents[self.selected].color = self.unselected_color

    def on_key_press(self, key):
        if key == KEY_DOWN:
            self.selected = self.selected + 1
        elif key == KEY_UP:
            self.selected = self.selected - 1
        elif key == KEY_PAGE_UP:
            if (self.selected - self._page_size) >= 0:
                self.selected = self.selected - self._page_size
            else:
                self.selected = 0
        elif key == KEY_PAGE_DOWN:
            if (self.selected + self._page_size) < len(self.contents):
                self.selected = self.selected + self._page_size
            else:
                self.selected = len(self.contents) - 1
        elif key == KEY_ENTER:
            self.result = self.contents[self.selected].text
        elif key == KEY_END:
            self.selected = len(self.contents) - 1
        elif key == KEY_HOME:
            self.selected = 0

        while self.selected >= len(self.contents):
            self.selected = self.selected - len(self.contents)
        while self.selected < 0:
            self.selected = self.selected + len(self.contents)
        if (self.contents[self.selected].y + self.offset[1]) > (get_screen_height() - self.font_size):
            self.offset = (0, -self.contents[self.selected].y)
            if (-self.offset[1]) // self.font_size > len(self.contents) - self._page_size:
                self.offset = (0, -self.font_size *
                               (len(self.contents) - self._page_size))
        elif self.contents[self.selected].y + self.offset[1] < 0:
            self.offset = (0, -self.contents[self.selected].y)
