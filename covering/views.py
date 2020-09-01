from random import random
from math import sqrt
import vpython as vp


class GeneralView:
    def show(self, model):
        raise NotImplementedError


class TwoDPrintView(GeneralView):
    def show(self, model):
        data = model.state.raw_data()

        vals = [x for row in data for x in row]
        longest = max(vals)
        max_len = len(str(longest))
        width = max_len + 1

        for row in data:
            p_row = "".join([str(x).center(width) for x in row])
            print(p_row)


class PyramidPrintView(GeneralView):
    @staticmethod
    def _max_len(data):
        vals = [x for layer in data for row in layer for x in row
                if x is not None]
        longest = max(vals)
        max_len = len(str(longest))
        return max_len

    def show(self, model):
        def show_layer(layer_data, offset):
            # The order is not neccessarily correct
            l = len(layer_data)
            for i, row in enumerate(layer_data):
                row_data = row[:l-i]
                print(i * offset * " ", end="")
                row = "".join([str(x).ljust(width) for x in row_data])
                print(row)

        data = model.state.raw_data()
        max_len = PyramidPrintView._max_len(data)

        width = max_len + 1 if (max_len % 2 == 1) else max_len + 2
        offset = width // 2
        l = len(data)

        for i, layer in enumerate(data):
            print(f"\nLayer {i + 1}\n")
            layer_data = layer[:l-i]
            show_layer(layer_data, offset)


class PyramidVisualView(GeneralView):
    RADIUS = 1

    def __init__(self):
        self.colors = dict()
        self.spheres = []

    @staticmethod
    def _random_color():
        return vp.vec(random(), random(), random())

    @staticmethod
    def _real_coords(pos):
        x, y, z = pos

        rz = sqrt(8/3) * PyramidVisualView.RADIUS * z

        ry_start = (sqrt(3) / 3) * PyramidVisualView.RADIUS * z  # Layer offset
        ry = ry_start + sqrt(3) * PyramidVisualView.RADIUS * y

        rx_start = PyramidVisualView.RADIUS * (y + z)
        rx = rx_start + 2 * x * PyramidVisualView.RADIUS

        return vp.vec(rx, ry, rz)

    def show(self, model):
        for pos in model.all_positions():
            val = model.state[pos]

            if val is None:
                continue

            if val not in self.colors:
                self.colors[val] = PyramidVisualView._random_color()
            color = self.colors[val]

            rpos = PyramidVisualView._real_coords(pos)
            self.spheres.append(vp.sphere(
                pos=rpos,
                radius=PyramidVisualView.RADIUS,
                color=color,
                opacity=0.8))
