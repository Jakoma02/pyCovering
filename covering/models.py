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

    def __init__(self, block_size):
        self.block_size = block_size
        self.state = self._get_state_container()

        self.pos = None  # Implementations will change this in reset()
        self.step_nu = 1

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

    def _neighbors(self, pos):
        raise NotImplementedError

    def all_positions(self, state=None):
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

        for pos in self.all_positions():
            if visited[pos] or state[pos] is not None:
                continue
            component_size = dfs(pos)
            if component_size % self.block_size != 0:
                return False

        return True


class GeneralCoveringState:
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

    def raw_data(self):
        """
        Return the inner state object

        This technically doesn't create a copy and just passes the object,
        for now we trust that it will not be modified
        """
        return self._state


# 2D


class TwoDCoveringState(GeneralCoveringState):
    def __init__(self, width, height):
        self.reset(width, height)

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

    def all_positions(self, state=None):
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


class ThreeDCoveringState(GeneralCoveringState):
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

        self.state.reset(self.size, self.size, self.size)
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
            (x + 1, y, z),
            (0, y + 1, z),
            (0, 0, z + 1)
        ]

        for opt in options:
            if self._is_valid_position(opt):
                return opt

        return None

    def all_positions(self, state=None):
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
            (x - 1, y, z + 1),
            (x, y, z + 1),

            # Below
            (x, y, z - 1),
            (x + 1, y, z - 1),
            (x, y + 1, z - 1)
        ]

        for pos in neighbors:
            if self._is_valid_position(pos):
                yield pos
