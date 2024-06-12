import scene
import elements
from find_info import Info

from pyray import *


class DirectoryExtractor:
    def __init__(self, item: Info):
        self.item = item
        
    def get_menu_item_texts(self):
        for child in self.item.children.keys():
            yield child
    
    def get_result(self, text: str):
        return self.item.children[text]


class LayoutExtractor:
    def __init__(self, item: Info):
        self.item = item
        
    def get_menu_item_texts(self):
        if "layouts" not in self.item.info:
            self.item = self.item.parent
        if "layouts" in self.item.info:
            for name in self.item.info["layouts"]:
                if len(name) > 7 and name.startswith("LAYOUT_"):
                    yield name[7:]
    
    def get_result(self, text: str):
        return f"LAYOUT_{text}"


class Selector(scene.Scene):
    
    def __init__(
            self,
            name: str,
            item : Info,
            extractor,
            page_height: int,
            select_scene: str,
            cancel_scene: str
        ):
        super().__init__(name)
        self.selected = 0
        self.font_size = 20
        self.selected_color = RED
        self.unselected_color = BLACK
        self.y = 0
        self.result = None
        self._page_size = page_height // self.font_size
        self.select_scene = select_scene
        self.cancel_scene = cancel_scene
        self.item = item
        self.extractor = extractor
        for name in sorted([x for x in self.extractor.get_menu_item_texts()]):
            row = elements.Text(
                0,
                self.y,
                name,
                self.font_size,
                self.unselected_color
            )
            self.contents.append(row)
            self.y += row.height

    def draw(self):
        self.contents[self.selected].color = self.selected_color
        super().draw()
        self.contents[self.selected].color = self.unselected_color

    def trigger_key(self, key) -> str:
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
            name = self.contents[self.selected].text
            self.result = self.extractor.get_result(name)
            return self.select_scene
        elif key == KEY_END:
            self.selected = len(self.contents) - 1
        elif key == KEY_HOME:
            self.selected = 0
        elif key == KEY_ESCAPE:
            self.result = self.item.parent
            return self.cancel_scene
        elif key >= KEY_A and key <= KEY_Z:
            if self.contents[self.selected].text.lower().startswith(chr(key).lower()):
                self.selected = self.selected + 1
            else:
                for i, item in enumerate(self.contents):
                    if item.text.lower().startswith(chr(key).lower()):
                        self.selected = i
                        break

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
        return None
