import json
import sys
import os

from pyray import *

import elements
import scene

qmk_dir = sys.argv[1] if len(sys.argv) > 1 else "."

def get_key_setup_scene(file_name):
    with open(file_name) as f:
        doc = json.load(f)

    layout_data = doc["layouts"]["LAYOUT"]["layout"]

    matrix = dict()

    key_width = 50
    key_height = 50

    keyboard_scene = scene.Scene("KeyboardLayout")
    for item in layout_data:
        pos = item["matrix"]
        print(pos)
        if pos[0] not in matrix:
            matrix[pos[0]] = dict()
        matrix[pos[0]][pos[1]] = (float(item["x"]), float(item["y"]))
        keyboard_scene.contents.append(
            elements.Rectangle(
                int(float(item["x"]) * key_width),
                int(float(item["y"]) * key_height),
                key_width,
                key_height,
                BLACK
            )
        )

    return keyboard_scene


def get_selector_scene(name: str, items: list):
    selector_scene = scene.Scene(name)
    y = 0
    font_size = 20
    for item in items:
        row = elements.Text(
            0,
            y,
            item,
            font_size,
            BLACK
        )
        selector_scene.contents.append(row)
        y += row.height
    return selector_scene


# current_scene = get_key_setup_scene(sys.argv[1])
current_scene = get_selector_scene("Select a keyboard layout", sorted(os.listdir(qmk_dir)))

init_window(800, 450, "Hello")
set_target_fps(60)

while not window_should_close():
    current_scene.draw()

close_window()
