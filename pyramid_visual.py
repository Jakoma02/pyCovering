from vpython import sphere, vec, rate, scene
from math import sqrt
from time import sleep
from random import random
from covering import PyramidCoveringModel, ImpossibleToFinishException

RADIUS = 1

spheres = []

colors = dict()


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


model = PyramidCoveringModel(10, 4)
model.reset()

try:
    while True:
        model.add_random_tile()
        pyramid(10, model.state._state)
        scene.waitfor("keyup")
except ImpossibleToFinishException:
    pass
