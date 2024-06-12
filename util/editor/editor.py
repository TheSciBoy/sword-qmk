import sys

from pathlib import Path
from pyray import *

import elements
import scene
import selector
import find_info


qmk_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".")


def get_key_setup_scene(info: find_info, layout_key: str):
    # TODO: Get all the info.json's, we need to select a keymap
    
    info.load()

    layout_data = info.info["layouts"][layout_key]["layout"]

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

print(f"Reading directory: {qmk_dir}")
root = find_info.Info("root", qmk_dir)
root.walk()
print("Done.")


def get_selector(name: str, previous_scene: scene.Scene):
    if previous_scene:
        item = previous_scene.result
        if len(item.children) == 0:
            item.load()
            
            if (not "layouts" in item.info):
                item = item.parent
                if item:
                    item.load()
            return selector.Selector(
                "LayoutSelector",
                item,
                selector.LayoutExtractor(item),
                get_screen_height(),
                "LayoutView",
                "Selector"
            )
    return selector.Selector(
        name,
        item,
        selector.DirectoryExtractor(item),
        get_screen_height(),
        "Selector",
        "Selector" if item.parent else None
    )


def get_scene(name: str, previous_scene : scene.Scene = None):
    if not name:
        return None
    item = None
    if name == "Selector":
        return get_selector(name, previous_scene)
    elif name == "LayoutView":
        return get_key_setup_scene(previous_scene.item, previous_scene.result)
    else:
        raise ValueError(f"Unknown scene type {name}")


init_window(800, 450, "Hello")
set_target_fps(60)
set_exit_key(KEY_F12)

current_scene = selector.Selector(
    "Select a keyboard layout",
    root,
    selector.DirectoryExtractor(root),
    get_screen_height(),
    "Selector",
    None
)

while current_scene and not window_should_close():
    next_scene = current_scene.execute()
    if next_scene:
        current_scene = get_scene(next_scene, current_scene)
        if not current_scene:
            break

    key = get_key_pressed()
    while key:
        next_scene = current_scene.on_key_press(key)
        if next_scene:
            current_scene = get_scene(next_scene, current_scene)
            break
        key = get_key_pressed()
    
    if current_scene:
        current_scene.draw()

close_window()
