from vpython import sphere, arrow, vec, rate, scene, color
from math import sqrt
from time import sleep
from random import random
from covering import PyramidCoveringModel, ImpossibleToFinishException

RADIUS = 1

spheres = []

colors = {}


def random_color():
    return vec(random(), random(), random())


def layer(size, layer_data, start_pos=vec(0, 0, 0)):
    for x, row_data in enumerate(layer_data):
        row_start = start_pos + vec(x * RADIUS, sqrt(3) * x * RADIUS, 0)
        for y, val in zip(range(size - x), row_data):
            if val is None:
                continue

            if val not in colors:
                colors[val] = random_color()

            color = colors[val]

            pos = row_start + vec(2 * y * RADIUS, 0, 0)
            spheres.append(sphere(pos=pos, radius=RADIUS, color=color))


def pyramid(size, data):
    for z, ld in enumerate(data):
        layer_start = vec(z * RADIUS, z * RADIUS, sqrt(3) * z * RADIUS)
        layer(size - z, ld, layer_start)


def clear():
    while spheres:
        s = spheres.pop()
        s.visible = False
        del s


def show_axes():
    OPACITY = 0.5

    o = vec(0, 0, 0)
    arrow(pos=o, axis=vec(10, 0, 0), color=color.red, opacity=OPACITY)
    arrow(pos=o, axis=vec(0, 10, 0), color=color.green, opacity=OPACITY)
    arrow(pos=o, axis=vec(0, 0, 10), color=color.blue, opacity=OPACITY)


def show_pyramid_axes():
    OPACITY = 0.5

    o = vec(0, 0, 0)
    arrow(pos=o, axis=vec(10, 0, 0), color=color.red, opacity=OPACITY)
    arrow(pos=o, axis=vec(5, 5 * sqrt(3), 0), color=color.green,
          opacity=OPACITY)
    arrow(pos=o, axis=vec(5, 5/3 * sqrt(3), 5 * sqrt(8/3)), color=color.blue,
          opacity=OPACITY)


def show_model(model):
    clear()
    pyramid(model.size, model.state._state)


def real_coords(pos):
    x, y, z = pos

    rz = sqrt(8/3) * RADIUS * z

    ry_start = (sqrt(3) / 3) * RADIUS * z  # Layer offset
    ry = ry_start + sqrt(3) * RADIUS * y

    rx_start = RADIUS * (y + z)
    rx = rx_start + 2 * x * RADIUS

    return vec(rx, ry, rz)


def show_model2(model):
    clear()
    for pos in model._all_positions():
        val = model.state[pos]

        if val is None:
            continue

        if val not in colors:
            colors[val] = random_color()
        color = colors[val]

        rpos = real_coords(pos)
        spheres.append(sphere(pos=rpos, radius=RADIUS, color=color,
                       opacity=0.8))


show_pyramid_axes()

model = PyramidCoveringModel(15, 4)
# model = PyramidCoveringModel(4, 4)

while not model.is_filled():
    model.add_random_tile()
    show_model2(model)
    scene.waitfor("keyup")
