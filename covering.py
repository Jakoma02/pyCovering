#!/usr/bin/env python3

import tkinter as tk
import tkinter.messagebox as mb
import random
import copy
import signal  # Unix only!


def random_color():
    """
    Generates a random string in format #XXXXXX
    to be used as a color
    """
    code = random.randint(0, 0xFFFFFF)
    return "#{:06X}".format(code)


class ImpossibleToFinishException(Exception):
    """
    This exception is raised when it is not possible
    to cover the whole area
    """


class CoveringTimeoutException(Exception):
    """
    This exception is raised if covering takes
    longer than allowed
    """


class GeneralCoveringModel:
    """
    Model encapsulating all bussiness logic
    """

    def __init__(self, block_size):
        self.block_size = block_size
        self.state = self._get_state_container()

        # Set timeout handler
        signal.signal(signal.SIGALRM, self._timeout_handler)

        self.reset()

    def _get_state_container(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError

    def is_filled(self):
        raise NotImplementedError

    def _next_position(self, pos):
        raise NotImplementedError

    def _all_positions(self, state=None):
        raise NotImplementedError

    def _neighbors(self, pos):
        raise NotImplementedError

    def _next_empty(self, pos):
        while True:
            if pos is None:
                return None

            if self.state[pos] is None:
                return pos

            pos = self._next_position(pos)

    def set_block_size(self, size):
        """
        Sets size of the tile groups (this resets current state)
        """
        self.block_size = size

    def add_random_tile(self, check_finishable=True):
        """
        Adds one tile (makes one step)
        """
        pos = self._next_empty(self.pos)
        self.pos = pos

        valid = self._valid_step(pos, check_finishable=check_finishable)
        if valid is None:
            raise ImpossibleToFinishException("There are no more valid steps")

        for pos in valid:
            self.state[pos] = self.step_nu

        self.step_nu += 1

    def try_cover(self, check_finishable=True, timeout=0):
        """
        Tries to cover the whole area with tiles, throws
        an exception if not successful
        """
        signal.alarm(timeout)  # In seconds

        while not self.is_filled():
            self.add_random_tile(check_finishable=check_finishable)

        signal.alarm(0)  # Cancel alarm

    def _timeout_handler(self, sig, frame):
        raise CoveringTimeoutException("Time exceeded")

    def _empty_neighbors(self, pos, state=None):
        if state is None:
            state = self.state

        result = set()

        for pos in self._neighbors(pos):
            if state[pos] is not None:
                continue
            result.add(pos)

        return result

    def _group_neighbors(self, group, state=None):
        """
        Return a shuffled list of all empty neighbors of a group
        """

        if state is None:
            state = self.state

        result = set()

        for pos in group:
            result.update(self._empty_neighbors(pos, state=state))

        res_list = list(result)
        random.shuffle(res_list)

        return res_list

    def _valid_step(self, pos, check_finishable=True):
        """
        Returns a tuple of positions of a valid step
        starting with pos
        """
        iterables = []
        curr_generated = [pos]

        state_copy = copy.deepcopy(self.state)

        if pos is None:
            return None

        state_copy[pos] = -1

        new_gen = iter(self._group_neighbors(curr_generated, state=state_copy))
        iterables.append(new_gen)

        while iterables:
            last_gen = iterables[-1]
            try:
                generated_pos = next(last_gen)
                curr_generated.append(generated_pos)

                state_copy[generated_pos] = -1  # Placeholder

                if len(curr_generated) == self.block_size:
                    if not check_finishable or \
                           self._is_finishable(state=state_copy):
                        return tuple(curr_generated)
                    state_copy[generated_pos] = None
                    curr_generated.pop()
                else:
                    new_gen = iter(self._group_neighbors(curr_generated,
                                                         state=state_copy))
                    iterables.append(new_gen)

            except StopIteration:
                iterables.pop()
                last_pos = curr_generated.pop()
                state_copy[last_pos] = None

        return None

    def _is_finishable(self, state=None):
        """
        Do a DFS and check that all component sizes are divisible
        by block_size
        """

        def dfs(pos):
            stack = [pos]
            component_size = 0

            while stack:
                pos = stack.pop()

                if state[pos] is not None:
                    continue
                if visited[pos]:
                    continue

                visited[pos] = True
                component_size += 1  # Me

                for nei_pos in self._neighbors(pos):
                    stack.append(nei_pos)

            return component_size

        if state is None:
            state = self.state

        # A little hack, but provides exactly the API we need
        visited = self._get_state_container()

        for pos in self._all_positions():
            if visited[pos] or state[pos] is not None:
                continue
            component_size = dfs(pos)
            if component_size % self.block_size != 0:
                return False

        return True

# 2D


class TwoDCoveringState:
    def __init__(self, width, height):
        self.reset(width, height)

    def reset(self, width, height):
        self._state = [[None for _ in range(width)]
                       for _ in range(height)]

    def __getitem__(self, pos):
        """
        Get state of position pos

        This allows to use `model[pos]` without losing genericity,
        only this method needs to be reimplemented
        """
        x, y = pos
        return self._state[y][x]

    def __setitem__(self, pos, val):
        """
        Set state of position pos

        This allows to use `model[pos] = val` without losing genericity,
        only this method needs to be reimplemented
        """
        x, y = pos
        self._state[y][x] = val

    def raw_data(self):
        """
        Returns data as a list of list, as in previous versions
        """
        return self._state


class TwoDCoveringModel(GeneralCoveringModel):
    """
    Specialized version of GeneralCoveringModel that covers the plane
    """
    def __init__(self, width, height, block_size):
        self.width = width
        self.height = height
        super().__init__(block_size)

    def _get_state_container(self):
        return TwoDCoveringState(self.width, self.height)

    def set_size(self, width, height):
        """
        Sets the area width and height (this resets current state)
        """
        self.width = width
        self.height = height

        self.reset()

    def reset(self):
        """
        Removes all tiles, resets position
        """
        self.state.reset(self.width, self.height)
        self.pos = (0, 0)
        self.step_nu = 1

    def is_filled(self):
        return (self.step_nu - 1) * self.block_size == self.width * self.height

    def _next_position(self, pos):
        if pos is None:
            return None

        x, y = pos

        if x < self.width - 1:
            return (x + 1, y)
        if y < self.height - 1:
            return (0, y + 1)

        return None

    def _all_positions(self, state=None):
        if state is None:
            state = self.state

        for x in range(self.width):
            for y in range(self.height):
                yield (x, y)

    def _neighbors(self, pos):
        neighbors = [
            (pos[0] - 1, pos[1]),
            (pos[0] + 1, pos[1]),
            (pos[0], pos[1] - 1),
            (pos[0], pos[1] + 1)
        ]

        for x, y in neighbors:
            if x < 0 or y < 0 or x >= self.width or y >= self.height:
                continue
            yield (x, y)

# 3D


class ThreeDCoveringState:
    def __init__(self, xs, ys, zs):
        self.reset(xs, ys, zs)

    def reset(self, xs, ys, zs):
        self._state = [[[None for _ in range(zs)]
                        for _ in range(ys)]
                       for _ in range(xs)]

    def __getitem__(self, pos):
        x, y, z = pos

        return self._state[x][y][z]

    def __setitem__(self, pos, val):
        x, y, z = pos

        self._state[x][y][z] = val


class PyramidCoveringModel(GeneralCoveringModel):
    def __init__(self, pyramid_size, block_size):
        self.size = pyramid_size

        super().__init__(block_size)

    def reset(self):
        def layer_size(layer):
            return (1 + layer) * layer // 2

        self.state.reset(self.size)
        self.pos = (0, 0, 0)
        self.step_nu = 1

        layers = self.size

        self._total_size = sum(layer_size(x) for x in range(1, layers + 1))

    def is_filled(self):
        return (self.step_nu - 1) * self.block_size == self._total_size

    def _get_state_container(self):
        return ThreeDCoveringState(self.size, self.size, self.size)

    def _next_position(self, pos):
        x, y, z = pos

        options = [
            (x, y + 1, z),
            (x + 1, 0, z),
            (0, 0, z + 1)
        ]

        for opt in options:
            if self._is_valid_position(opt):
                return opt

        return None

    def _all_positions(self, state=None):
        if state is None:
            state = self.state

        pos = (0, 0, 0)

        while pos is not None:
            yield pos
            pos = self._next_position(pos)

    def _is_valid_position(self, pos):
        x, y, z = pos

        if x < 0 or y < 0 or z < 0:
            return False

        if z >= self.size:
            return False

        level_size = self.size - z

        if x >= level_size:
            return False

        line_size = level_size - x

        if y >= line_size:
            return False

        return True

    def _neighbors(self, pos):
        x, y, z = pos

        neighbors = [
            # Same level
            (x, y + 1, z),
            (x + 1, y, z),
            (x + 1, y - 1, z),
            (x, y - 1, z),
            (x - 1, y, z),
            (x - 1, y + 1, z),

            # Above
            (x, y - 1, z + 1),
            (x - 1, y - 1, z + 1),
            (x, y, z + 1),

            # Below
            (x, y, z - 1),
            (x + 1, y + 1, z - 1),
            (x, y + 1, z - 1)
        ]

        for pos in neighbors:
            if self._is_valid_position(pos):
                yield pos


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
