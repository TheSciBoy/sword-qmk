import json
import sys

from pathlib import Path
from pyray import *

import elements
import scene
import selector

qmk_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".")


def get_key_setup_scene(file_name: Path):
    # TODO: Get all the info.json's, we need to select a keymap
    
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


def get_scene(name: str, previous_scene : scene.Scene = None):
    if name == "KeyboardSelector":
        return scene.Selector(name)
    elif name == "Layout":
        return get_key_setup_scene(qmk_dir / previous_scene.result)
    else:
        raise ValueError(f"Unknown scene type {name}")


init_window(800, 450, "Hello")
set_target_fps(60)

current_scene = selector.Selector(
    "Select a keyboard layout",
    sorted([x.name for x in qmk_dir.iterdir() if x.is_dir()]),
    get_screen_height()
)

while not window_should_close():
    next_scene = current_scene.execute()
    if next_scene:
        current_scene = get_scene(next_scene, current_scene)

    key = get_key_pressed()
    while key:
        current_scene.on_key_press(key)
        key = get_key_pressed()
    
    current_scene.draw()

close_window()
