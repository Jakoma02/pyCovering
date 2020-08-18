#!/usr/bin/env python

import itertools as it

from PIL import Image, ImageDraw, ImageFont
from random import randint


WIDTH = 3
HEIGHT = 3
TILES = 3

SIZE = 30

colors = {}


def random_color():
    # Only light colors
    return tuple((randint(50, 255) for _ in range(3)))


def draw_covering(covering, filename):
    global colors

    im = Image.new("RGB", (WIDTH * SIZE, HEIGHT * SIZE), "white")
    draw = ImageDraw.Draw(im)
   
    for y, row in enumerate(covering):
        for x, val in enumerate(row):
            if val is None:
                continue

            if val not in colors:
                colors[val] = random_color()
            color = colors[val]

            left = x * SIZE
            top = y * SIZE

            draw.rectangle(
                xy=[(left, top), (left + SIZE), (top + SIZE)],
                outline="black",
                fill=color,
                width=1
            )

            font = ImageFont.truetype("ArialCE.ttf", 18)

            text = str(val)
            width, height = draw.textsize(text, font=font)

            text_x = left + (SIZE - width) / 2
            text_y = top + (SIZE - height) / 2

            draw.text(
                xy=(text_x, text_y),
                text=text,
                fill="black",
                font=font
            )

    im.save(filename)


def all_coverings():
    


filename = "drawing.png"
covering = [
    [None, None, 1],
    [2, 2, 2],
    [2, 3, 4]
]

draw_covering(covering, filename)
