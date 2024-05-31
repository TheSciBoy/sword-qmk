import json
import sys

from pyray import *

with open(sys.argv[1]) as f:
    doc = json.load(f)

layout_data = doc["layouts"]["LAYOUT"]["layout"]

matrix = dict()

for item in layout_data:
    pos = item["matrix"]
    print(pos)
    if pos[0] not in matrix:
        matrix[pos[0]] = dict()
    matrix[pos[0]][pos[1]] = (float(item["x"]), float(item["y"]))
    print(f"Added {pos[0]} {pos[1]} - {matrix[pos[0]][pos[1]]}")

# print(matrix)

init_window(800, 450, "Hello")

key_width = 50
key_height = 50

while not window_should_close():
    begin_drawing()
    clear_background(RAYWHITE)
    for mxpos, items in matrix.items():
        for mypos, spos in items.items():
            xstart = int(spos[0] * key_width)
            ystart = int(spos[1] * key_height)
            draw_rectangle_lines(xstart, ystart, key_width, key_height, BLACK)
    end_drawing()

close_window()
