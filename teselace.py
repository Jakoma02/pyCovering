#!/usr/bin/env python3

import tkinter as tk
import tkinter.messagebox as mb
import random
import copy


def random_color():
    """
    Generates a random string in format #XXXXXX
    to be used as a color
    """
    code = random.randint(0, 0xFFFFFF)
    return "#{:06X}".format(code)


class Area(tk.Canvas):
    INIT_TILES = 10
    TILE_SIZE = 30

    def __init__(self, master):
        width = self.INIT_TILES * self.TILE_SIZE
        height = self.INIT_TILES * self.TILE_SIZE

        self.colors = {}

        super().__init__(master, width=width, height=height, bg="white")

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
    def __init__(self, master):
        self.area = Area(master)
        self.area.pack(pady=100, padx=100)

        self.width = 10
        self.height = 10
        self.block_size = 4

        frame = tk.Frame(master)
        frame.pack()

        self.width_entry = tk.Entry(frame)
        self.width_entry.insert(0, str(self.width))
        self.width_entry.pack()

        self.height_entry = tk.Entry(frame)
        self.height_entry.insert(0, str(self.height))
        self.height_entry.pack()

        self.block_size_entry = tk.Entry(frame)
        self.block_size_entry.insert(0, str(self.block_size))
        self.block_size_entry.pack()

        update_button = tk.Button(frame, text="Update settings",
                                  command=self.update_settings)
        update_button.pack(side=tk.LEFT)

        step_button = tk.Button(frame, text="Step", command=self.step)
        step_button.pack(side=tk.LEFT)

        self.reset_state()

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

            self.reset_state()

        except ValueError:
            mb.showerror("Invalid sizes", "The sizes are not integers")

    def reset_state(self):
        self.state = [[None for _ in range(self.width)]
                      for _ in range(self.height)]
        self.pos = (0, 0)
        self.step_nu = 1

        self.area.update(self.state)

    def next_empty(self, pos):
        if pos is None:
            return None

        x, y = pos

        for j in range(y, self.height):
            first = x if j == y else 0
            for i in range(first, self.width):
                if self.state[j][i] is None:
                    return (i, j)

        return None

    def step(self):
        pos = self.next_empty(self.pos)
        self.pos = pos

        valid = self.valid_step(pos)
        if valid is None:
            mb.showerror("No more steps", "There are no more valid steps")
            return

        for pos in valid:
            x, y = pos
            self.state[y][x] = self.step_nu

        self.step_nu += 1

        self.area.update(self.state)

    def empty_neighbors(self, pos, state=None):
        if state is None:
            state = self.state

        neighbors = [
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1)
        ]

        result = set()

        for x, y in neighbors:
            if x < 0 or y < 0 or x >= self.width or y >= self.height:
                continue
            if state[y][x] is not None:
                continue
            result.add((x, y))

        return result

    def group_neighbors(self, group, state=None):
        """
        Return a shuffled list of all empty neighbors of a group
        """

        if state is None:
            state = self.state

        result = set()

        for pos in group:
            result.update(self.empty_neighbors(pos, state=state))

        res_list = list(result)
        random.shuffle(res_list)

        return res_list

    def valid_step(self, pos):
        """
        Returns a tuple of positions of a valid step
        starting with pos
        """
        generators = []
        curr_generated = [pos]

        state_copy = copy.deepcopy(self.state)

        if pos is None:
            return None

        x, y = pos
        state_copy[y][x] = -1

        # TODO: Rename generators to iterators

        new_gen = iter(self.group_neighbors(curr_generated, state=state_copy))
        generators.append(new_gen)

        while generators:
            last_gen = generators[-1]
            try:
                generated = next(last_gen)
                curr_generated.append(generated)

                x, y = generated
                state_copy[y][x] = -1  # Placeholder

                if len(curr_generated) == self.block_size:
                    if self.is_finishable(state=state_copy):
                        return tuple(curr_generated)
                    state_copy[y][x] = None
                    curr_generated.pop()
                else:
                    new_gen = iter(self.group_neighbors(curr_generated,
                                                        state=state_copy))
                    generators.append(new_gen)

            except StopIteration:
                generators.pop()
                x, y = curr_generated.pop()
                state_copy[y][x] = None

        return None

    def is_finishable(self, state=None):
        """
        Do a DFS and check that all component sizes are divisible
        by block_size
        """

        def dfs(x, y):
            if x < 0 or y < 0 or x >= self.width or y >= self.height:
                return 0
            if state[y][x] is not None:
                return 0
            if visited[y][x]:
                return 0

            visited[y][x] = True
            count = 1  # Me

            neighbors = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1)
            ]

            for x2, y2 in neighbors:
                count += dfs(x2, y2)

            return count

        if state is None:
            state = self.state

        visited = [[False for _ in range(self.width)]
                   for _ in range(self.height)]

        for y in range(self.width):
            for x in range(self.height):
                if visited[y][x] or state[y][x] is not None:
                    continue
                component_size = dfs(x, y)
                if component_size % self.block_size != 0:
                    return False

        return True


if __name__ == "__main__":
    root = tk.Tk()
    root.title("2D Tesselation - Jakub Komárek 2020")
    app = App(root)
    root.mainloop()
