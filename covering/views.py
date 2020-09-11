"""
This module contains various views for all covering models
"""

from random import random
from math import sqrt
from multiprocessing import Process, Queue

import vpython as vp

from covering.models import Block


class GeneralView:
    """
    An abstract class from which all views should inherit
    """
    def show(self, model):
        """
        Show model data using the view
        """
        raise NotImplementedError

    def close(self):
        """
        Closes the view window, if any

        Doesn't do anything by default
        """


class TwoDPrintView(GeneralView):
    """
    A view for TwoDCoveringModel, prints the resulting
    covering in console
    """
    def show(self, model):
        data = model.state.raw_data()

        vals = [x.number for row in data for x in row]
        longest = max(vals)
        max_len = len(str(longest))
        width = max_len + 1

        for row in data:
            p_row = "".join([(str(x.number) if x.visible else "")
                             .center(width) for x in row])
            print(p_row)


class PyramidPrintView(GeneralView):
    """
    A view for PyramidCoveringModel, prints the resulting
    covering in console
    """
    @staticmethod
    def _max_len(data):
        vals = [x.number for layer in data for row in layer for x in row
                if x is not Block.EMPTY]
        longest = max(vals)
        max_len = len(str(longest))
        return max_len

    def show(self, model):
        def show_layer(layer_data, offset):
            # The order is not neccessarily correct
            layer_size = len(layer_data)
            for i, row in enumerate(layer_data):
                row_data = row[:layer_size-i]
                print(i * offset * " ", end="")
                row = "".join([(str(x.number) if x.visible else "")
                              .center(width) for x in row_data])
                print(row)

        data = model.state.raw_data()
        max_len = PyramidPrintView._max_len(data)

        width = max_len + 1 if (max_len % 2 == 1) else max_len + 2
        offset = width // 2
        data_size = len(data)

        for i, layer in enumerate(data):
            print(f"\nLayer {i + 1}\n")
            layer_data = layer[:data_size-i]
            show_layer(layer_data, offset)


class PyramidVisualView(GeneralView):
    """
    A view for PyramidCoveringModel, shows the resulting
    covering in a browser window as a simple 3d visualization
    """
    RADIUS = 1

    def __init__(self):
        self.spheres = []

        self.process = None
        self.queue = Queue()

    @staticmethod
    def _to_vpython_color(color):
        """
        Converts (0-255, 0-255, 0-255) -> Vector(0-1, 0-1, 0-1)
        """
        r, g, b = color

        return vp.vec(r / 255, g / 255, b / 255)

    @staticmethod
    def _real_coords(pos):
        x, y, z = pos

        real_z = sqrt(8/3) * PyramidVisualView.RADIUS * z

        # Layer offset
        real_y_start = (sqrt(3) / 3) * PyramidVisualView.RADIUS * z
        real_y = real_y_start + sqrt(3) * PyramidVisualView.RADIUS * y

        real_x_start = PyramidVisualView.RADIUS * (y + z)
        real_x = real_x_start + 2 * x * PyramidVisualView.RADIUS

        return vp.vec(real_x, real_y, real_z)

    def reset(self):
        while self.spheres:
            sphere = self.spheres.pop()
            sphere.visible = False

    def show(self, model):
        if self.process is None:
            self.process = Process(
                target=self._show_process,
                args=(model, self.queue))
            self.process.start()

        self.queue.put(model)

    def _show_process(self, model, queue):
        try:
            while True:
                if not queue.empty():
                    last = queue.get()
                    self._update(last)
        except BrokenPipeError:
            # Vpython raises this, can be ignored
            pass

    def _update(self, model):
        self.reset()

        for pos in model.all_positions():
            block = model.state[pos]

            if block is None or not block.visible:
                continue

            vp_color = self._to_vpython_color(block.color)

            rpos = PyramidVisualView._real_coords(pos)
            self.spheres.append(vp.sphere(
                pos=rpos,
                radius=PyramidVisualView.RADIUS,
                color=vp_color,
                opacity=0.8))

    def close(self):
        if self.process is not None:
            self.process.terminate()

        self.process = None
