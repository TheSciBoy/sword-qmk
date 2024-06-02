import json
import sys

from pyray import *

import elements
import scene

qmk_dir = sys.argv[1] if len(sys.argv) > 1 else "."

with open(sys.argv[1]) as f:
    doc = json.load(f)

layout_data = doc["layouts"]["LAYOUT"]["layout"]

matrix = dict()

key_width = 50
key_height = 50

current_scene = scene.Scene("KeyboardLayout")
for item in layout_data:
    pos = item["matrix"]
    print(pos)
    if pos[0] not in matrix:
        matrix[pos[0]] = dict()
    matrix[pos[0]][pos[1]] = (float(item["x"]), float(item["y"]))
    current_scene.contents.append(
        elements.Rectangle(
            int(float(item["x"]) * key_width),
            int(float(item["y"]) * key_height),
            key_width,
            key_height,
            BLACK
        )
    )

# print(matrix)

init_window(800, 450, "Hello")

while not window_should_close():
    current_scene.draw()

close_window()
