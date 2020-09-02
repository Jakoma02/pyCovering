"""
This module contains all covering models
"""

import signal  # Unix only!
import random
import copy


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

    INITIAL_POSITION = None

    def __init__(self, min_block_size, max_block_size):
        self.min_block_size = min_block_size
        self.max_block_size = max_block_size

        self.state = self._get_state_container()

        self.pos = None  # Implementations will change this in reset()

        # `constraints` is a list of functions [position] -> bool, that return
        # true if the group fulfils the constraint
        self.constraints = []

        # Set timeout handler
        signal.signal(signal.SIGALRM, GeneralCoveringModel._timeout_handler)

        self.reset()

    @classmethod
    def _get_state_container(cls):
        raise NotImplementedError

    def reset(self):
        """
        Reset the model to initial (empty) state

        This method is meant to be OVERRIDEN, this is just
        a common part meant to be called as `super().reset()`
        """
        self._empty_positions = self.total_positions()
        self.step_nu = 1

    def is_filled(self):
        """
        Returns true if there are no empty places
        in the model
        """
        return self._empty_positions == 0

    def _next_position(self, pos):
        raise NotImplementedError

    def _neighbors(self, pos):
        raise NotImplementedError

    def total_positions(self):
        """
        Returns the number of all positions
        within the model
        """
        raise NotImplementedError

    def all_positions(self):
        """
        Returns an iterator of all valid positions
        in the model
        """

        pos = self.INITIAL_POSITION

        while pos is not None:
            yield pos
            pos = self._next_position(pos)

    def _next_empty(self, pos):
        while True:
            if pos is None:
                return None

            if self.state[pos] is None:
                return pos

            pos = self._next_position(pos)

    def set_block_size(self, min_size, max_size):
        """
        Sets size of the tile groups (this resets current state)
        """
        self.min_block_size = min_size
        self.max_block_size = max_size
        self.reset()

    def add_tile(self, tile):
        """
        Add a new tile on positions from tile=[pos1, pos2, pos3, ...]
        """
        for pos in tile:
            self.state[pos] = self.step_nu

        self.step_nu += 1
        self._empty_positions -= len(tile)

    def add_random_tile(self, check_finishable=True):
        """
        Adds one tile (makes one step) with size in given bounds
        """

        # This may need A LOT of memory if max_block_size - min_block_size
        # is large
        all_sizes = list(range(self.min_block_size, self.max_block_size + 1))
        random.shuffle(all_sizes)  # Try the sizes in a random order

        pos = self._next_empty(self.pos)
        self.pos = pos

        step_size = 0

        for step_size in all_sizes:
            valid = self._valid_step(pos, step_size,
                                     check_finishable=check_finishable)
            if valid is not None:
                break
        else:
            # No size led to a success
            raise ImpossibleToFinishException(
                "There are no more valid steps")

        self.add_tile(valid)

    def empty_positions(self):
        """
        Return the number of positions that are not filled yet
        """
        return self._empty_positions

    def try_cover(self, check_finishable=True, timeout=0):
        """
        Tries to cover the whole area with tiles, throws
        an exception if not successful
        """
        signal.alarm(timeout)  # In seconds

        while not self.is_filled():
            self.add_random_tile(check_finishable=check_finishable)

        signal.alarm(0)  # Cancel alarm

    @staticmethod
    def _timeout_handler(sig, frame):
        raise CoveringTimeoutException("Time exceeded")

    def _empty_neighbors(self, pos, state=None):
        if state is None:
            state = self.state

        result = set()

        for nbr in self._neighbors(pos):
            if state[nbr] is not None:
                continue
            result.add(nbr)

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

    def _valid_step(self, pos, step_size, check_finishable=True):
        """
        Returns a tuple of positions of a valid step
        starting with pos

        `constraints` is a list of functions [position] -> bool, that return
        true if the group fulfils the constraint
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

                # Check that all model constraints all fulfilled
                if not all((cnstrt(curr_generated)
                            for cnstrt in self.constraints)):

                    # At least one constraint failed
                    curr_generated.pop()
                    continue

                state_copy[generated_pos] = -1  # Placeholder

                if len(curr_generated) == step_size:
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
        Do a DFS and check that all component sizes are:

        1) if min_block_size == max_block_size: divisible by block_size
        2) else:                                larger than min_block_size
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

        # A little hack, but provides exactly the interface we need
        visited = self._get_state_container()

        for pos in self.all_positions():
            if visited[pos] or state[pos] is not None:
                continue
            component_size = dfs(pos)

            if self.min_block_size == self.max_block_size:
                if component_size % self.min_block_size != 0:
                    return False

            # If block size is ambiguous
            elif component_size < self.min_block_size:
                return False

        return True


class GeneralCoveringState:
    """
    An abstract class representing the state
    of a covering model
    """
    def __init__(self):
        self._state = None  # Implementations will redefine this
        raise NotImplementedError

    def __getitem__(self, pos):
        """
        Get state of position pos

        This allows to use `model[pos]` without losing genericity,
        only this method needs to be reimplemented
        """
        raise NotImplementedError

    def __setitem__(self, pos, val):
        """
        Set state of position pos

        This allows to use `model[pos] = val` without losing genericity,
        only this method needs to be reimplemented
        """
        raise NotImplementedError

    def reset(self, *args):
        """
        Reset the covering state to initial (empty) state,
        args may contain new state size
        """
        raise NotImplementedError

    def raw_data(self):
        """
        Return the inner state object

        This technically doesn't create a copy and just passes the object,
        for now we trust that it will not be modified
        """
        return self._state


# 2D


class TwoDCoveringState(GeneralCoveringState):
    """
    The state of TwoDCoveringModel
    """
    # pylint: disable=super-init-not-called
    def __init__(self, width, height):
        self.reset(width, height)

    # pylint: disable=arguments-differ
    def reset(self, width, height):
        self._state = [[None for _ in range(width)]
                       for _ in range(height)]

    def __getitem__(self, pos):
        x, y = pos
        return self._state[y][x]

    def __setitem__(self, pos, val):
        x, y = pos
        self._state[y][x] = val


class TwoDCoveringModel(GeneralCoveringModel):
    """
    Specialized version of GeneralCoveringModel that covers the plane
    """

    INITIAL_POSITION = (0, 0)

    def __init__(self, width, height, min_block_size, max_block_size):
        self.width = width
        self.height = height
        super().__init__(min_block_size, max_block_size)

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

        super().reset()

    def total_positions(self):
        return self.width * self.height

    def _next_position(self, pos):
        if pos is None:
            return None

        x, y = pos

        if x < self.width - 1:
            return (x + 1, y)
        if y < self.height - 1:
            return (0, y + 1)

        return None

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


class ThreeDCoveringState(GeneralCoveringState):
    """
    State of a general three-dimensional covering model
    """
    # pylint: disable=super-init-not-called
    def __init__(self, xs, ys, zs):
        self.reset(xs, ys, zs)

    # pylint: disable=arguments-differ
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
    """
    Specialized version of GeneralCoveringModel that covers a 3D pyramid
    """

    INITIAL_POSITION = (0, 0, 0)

    def __init__(self, pyramid_size, min_block_size, max_block_size):
        self.size = pyramid_size

        super().__init__(min_block_size, max_block_size)

    def reset(self):
        self.state.reset(self.size, self.size, self.size)
        self.pos = (0, 0, 0)

        super().reset()

    def total_positions(self):
        # This comes from formulas for 1 + 2 + 3 + ... + n
        # and 1^2 + 2^2 + 3^2 + .. + n^2
        x = self.size

        return x * (x + 1) * (2 * x + 4) // 12

    def _get_state_container(self):
        return ThreeDCoveringState(self.size, self.size, self.size)

    def _next_position(self, pos):
        x, y, z = pos

        options = [
            (x + 1, y, z),
            (0, y + 1, z),
            (0, 0, z + 1)
        ]

        for opt in options:
            if self._is_valid_position(opt):
                return opt

        return None

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
            (x - 1, y, z + 1),
            (x, y, z + 1),

            # Below
            (x, y, z - 1),
            (x + 1, y, z - 1),
            (x, y + 1, z - 1)
        ]

        for nbr in neighbors:
            if self._is_valid_position(nbr):
                yield nbr
