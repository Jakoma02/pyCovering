#!/usr/bin/env python3

import tkinter as tk
import tkinter.messagebox as mb
import random

from models import ImpossibleToFinishException, TwoDCoveringModel


def random_color():
    """
    Generates a random string in format #XXXXXX
    to be used as a color
    """
    code = random.randint(0, 0xFFFFFF)
    return "#{:06X}".format(code)


class Area(tk.Canvas):
    TILE_SIZE = 30

    def __init__(self, master, width, height):
        canvas_width = width * self.TILE_SIZE
        canvas_height = height * self.TILE_SIZE

        self.colors = {}

        super().__init__(master, width=canvas_width,
                         height=canvas_height, bg="white")

    def update(self, data):
        self.delete("all")

        for y, row in enumerate(data):
            for x, val in enumerate(row):
                if val is None:
                    continue

                s = str(val)

                if s in self.colors:
                    color = self.colors[s]
                else:
                    color = random_color()
                    self.colors[s] = color

                left = x * self.TILE_SIZE
                top = y * self.TILE_SIZE

                self.create_rectangle(left, top, left + self.TILE_SIZE,
                                      top + self.TILE_SIZE, fill=color)

                x_center = left + self.TILE_SIZE / 2
                y_center = top + self.TILE_SIZE / 2

                self.create_text(x_center, y_center, text=s)

    def set_size(self, width, height):
        real_width = width * self.TILE_SIZE
        real_height = height * self.TILE_SIZE

        self.config(width=real_width, height=real_height)


class App():
    INIT_WIDTH = 10
    INIT_HEIGHT = 10
    INIT_BLOCK_SIZE = 4

    def __init__(self, master):
        self.area = Area(master, self.INIT_WIDTH, self.INIT_WIDTH)
        self.area.pack(pady=100, padx=100)

        self.model = TwoDCoveringModel(self.INIT_WIDTH, self.INIT_HEIGHT,
                                       self.INIT_BLOCK_SIZE)

        self.width = self.INIT_WIDTH
        self.height = self.INIT_HEIGHT
        self.block_size = self.INIT_BLOCK_SIZE

        frame = tk.Frame(master)
        frame.pack()

        width_frame = tk.Frame(frame)
        width_label = tk.Label(width_frame, text="Width: ")
        width_label.pack(side=tk.LEFT)
        self.width_entry = tk.Entry(width_frame)
        self.width_entry.insert(0, str(self.width))
        self.width_entry.pack(side=tk.LEFT)
        width_frame.pack()

        height_frame = tk.Frame(frame)
        height_label = tk.Label(height_frame, text="Height: ")
        height_label.pack(side=tk.LEFT)
        self.height_entry = tk.Entry(height_frame)
        self.height_entry.insert(0, str(self.height))
        self.height_entry.pack(side=tk.LEFT)
        height_frame.pack()

        block_size_frame = tk.Frame(frame)
        block_size_label = tk.Label(block_size_frame, text="Block size: ")
        block_size_label.pack(side=tk.LEFT)
        self.block_size_entry = tk.Entry(block_size_frame)
        self.block_size_entry.insert(0, str(self.block_size))
        self.block_size_entry.pack(side=tk.LEFT)
        block_size_frame.pack()

        update_button = tk.Button(frame, text="Update settings",
                                  command=self.update_settings)
        update_button.pack(side=tk.LEFT)

        step_button = tk.Button(frame, text="Step", command=self.step)
        step_button.pack(side=tk.LEFT)

    def update_settings(self):
        width = self.width_entry.get()
        height = self.height_entry.get()
        block_size = self.block_size_entry.get()

        try:
            width = int(width)
            height = int(height)
            block_size = int(block_size)

            if width < 1 or height < 1 or block_size < 1:
                mb.showerror("Invalid sizes", "The sizes must be at least one")
                return

            self.area.set_size(width, height)

            self.width = width
            self.height = height
            self.block_size = block_size

            self.reset()

        except ValueError:
            mb.showerror("Invalid sizes", "The sizes are not integers")

    def reset(self):
        self.model.set_size(self.width, self.height)
        self.model.set_block_size(self.block_size)

        self.model.reset()
        self.area.update(self.model.state.raw_data())

    def step(self):
        try:
            self.model.add_random_tile(check_finishable=True)
        except ImpossibleToFinishException:
            mb.showerror("Impossible to finish",
                         "There are no more valid steps")

        self.area.update(self.model.state.raw_data())


if __name__ == "__main__":
    root = tk.Tk()
    root.title("2D Covering - Jakub Komárek 2020")
    app = App(root)
    root.mainloop()
