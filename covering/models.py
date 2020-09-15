"""
This module contains all covering models
"""

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


class CoveringStoppedException(Exception):
    """
    This exceptions is raised if the covering
    was stopped by `model.stop_covering()`
    """


class Block:
    """
    This class represents one block in the model
    """
    def __init__(self, number):
        self.number = number
        self.positions = []
        self.color = self.random_color()
        self.visible = True

    @staticmethod
    def random_color():
        """
        This generates a random color for the model as (0-255, 0-255, 0-255)
        """
        return tuple((random.randint(0, 255) for _ in range(3)))

    def add_position(self, pos):
        """
        Adds `pos` to the block
        """
        self.positions.append(pos)

    def size(self):
        """
        Returns the size of the blocks
        """
        return len(self.positions)

    @classmethod
    def setup_static_instances(cls):
        """
        As is is (probably?) impossible to create static `Block`-type members
        directly, this method needs to be called once befero they can be used
        """
        cls.EMPTY = Block(-1)
        cls.PLACEHOLDER = Block(-2)

    def __deepcopy__(self, memo):
        return self  # HACK, in this case we don't need to go THIS deep


class Coverer:
    """
    This class contains some logic for covering the model.

    It uses backtracking to be able to get out of dead-ends.  As we don't know
    the total number of possible block shapes (and it is too costly to
    calculate it), we try to generate a random block `ATTEMPTS` times and if
    none if the blocks is was that wasn't tried out yet, we claim that one
    doesn't exist.
    """
    ATTEMPTS = 100

    def __init__(self, model):
        self.model = model

        # Backtracking stack
        # [(used_blocks, last_block, start_pos), ...]
        self._stack = [(set(), None, self.model.INITIAL_POSITION)]

    def _random_unused_block(self, used_blocks, pos, check_finishable=True):
        for _ in range(self.ATTEMPTS):
            try:
                new_block = self.model.random_block(
                        pos, check_finishable=check_finishable)
            except ImpossibleToFinishException:
                # No more blocks can be generated
                return None

            sorted_block = tuple(sorted(new_block))

            if sorted_block not in used_blocks:
                # Found a good block
                return sorted_block

        # No block found, backtrack
        return None

    def try_cover(self, check_finishable=True):
        """
        Try to cover the model with blocks.

        If it is not possible, throw an exception.
        """
        while self._stack:
            used_blocks, _, pos = self._stack[-1]

            new_block = self._random_unused_block(
                    used_blocks, pos, check_finishable=check_finishable)

            if new_block is None:
                # Backtraaack
                self._stack.pop()  # This is a deadend

                if not self._stack:
                    # Nothing to continue
                    break

                prev_used, prev_last, _ = self._stack[-1]  # One but last
                prev_used.add(prev_last)
                self.model.pop_block()
                continue

            # Continue with the new found block

            self.model.add_block(new_block)

            if self.model.is_filled():
                return  # Great!

            self._stack[-1] = (used_blocks, new_block, pos)

            next_pos = self.model.next_empty(pos)
            # Create a stack entry for the next level
            self._stack.append((set(), None, next_pos))

        raise ImpossibleToFinishException


# I guess it is right... but I don't think it is much of an issue
# pylint: disable=too-many-instance-attributes
class GeneralCoveringModel:
    """
    Model encapsulating all bussiness logic
    """

    INITIAL_POSITION = None

    def __init__(self, min_block_size, max_block_size, verbosity=0):
        Block.setup_static_instances()

        self.min_block_size = min_block_size
        self.max_block_size = max_block_size

        self.state = self._get_state_container()

        self.verbosity = verbosity

        self.pos = None  # Implementations will change this in reset()

        self.constraint_watchers = []
        self.stopped = False  # Was covering interrupted by another thread

        self.reset()

    @classmethod
    def _get_state_container(cls):
        raise NotImplementedError

    def message(self, msg):
        """
        Print a message if `-vv` is present in arguments
        """
        if self.verbosity >= 2:
            print(msg)

    def reset(self):
        """
        Reset the model to initial (empty) state

        This method is meant to be OVERRIDEN, this is just
        a common part meant to be called as `super().reset()`
        """
        self._empty_positions = self.total_positions()
        self.blocks = []
        self.block_nu = 1
        self._coverer = Coverer(self)

    def next_block(self):
        """
        Return a new (empty) block object
        """
        block = Block(self.block_nu)
        self.block_nu += 1

        return block

    def stop_covering(self):
        """
        Stop covering the model (if covering is in progress)
        """
        self.stopped = True

    def is_filled(self):
        """
        Returns true if there are no empty places
        in the model
        """
        return self._empty_positions == 0

    def _next_position(self, pos):
        raise NotImplementedError

    def neighbors(self, pos):
        """
        Returns positions of all valid neighbors of position `pos`
        """
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

    def next_empty(self, pos):
        """
        Return the first empty position after `pos`
        """
        while True:
            if pos is None:
                return None

            if self.state[pos] is Block.EMPTY:
                return pos

            pos = self._next_position(pos)

    def set_block_size(self, min_size, max_size):
        """
        Sets size of the blocks (this resets current state)
        """
        assert min_size <= max_size

        self.min_block_size = min_size
        self.max_block_size = max_size
        self.reset()

    def add_block(self, block_positions):
        """
        Add a new block on positions from block=[pos1, pos2, pos3, ...]
        """
        block_obj = self.next_block()
        self.blocks.append(block_obj)

        for pos in block_positions:
            self.state[pos] = block_obj
            block_obj.positions.append(pos)

        self._empty_positions -= len(block_positions)

    def pop_block(self):
        """
        Remove the most recently added block from the model
        """
        last = self.blocks.pop()

        for pos in last.positions:
            self.state[pos] = Block.EMPTY

        self._empty_positions += len(last.positions)
        self.block_nu -= 1

    def random_block(self, position, check_finishable=True):
        """
        Return a random block starting at position `position`
        (that can be inserted into the model)
        """
        all_sizes = list(range(self.min_block_size, self.max_block_size + 1))
        random.shuffle(all_sizes)  # Try the sizes in a random order

        step_size = 0

        for step_size in all_sizes:
            valid = self._valid_step(position, step_size,
                                     check_finishable=check_finishable)
            if valid is not None:
                break
        else:
            # No size led to a success
            raise ImpossibleToFinishException(
                "There are no more valid steps")

        return valid

    def empty_positions(self):
        """
        Return the number of positions that are not filled yet
        """
        return self._empty_positions

    def try_cover(self, check_finishable=True):
        """
        Tries to cover the whole area with blocks, throws
        an exception if not successful
        """
        self.stopped = False
        self._coverer.try_cover(check_finishable)

    def _empty_neighbors(self, pos, state=None):
        if state is None:
            state = self.state

        result = set()

        for nbr in self.neighbors(pos):
            if state[nbr] is not Block.EMPTY:
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
        """

        self.message(f"\t\t\tLooking for a valid block/step "
                     f"of size {step_size}...")
        iterables = []
        curr_generated = [pos]

        state_copy = copy.deepcopy(self.state)

        watcher_instances = [watcher(self, pos, state_copy)
                             for watcher in self.constraint_watchers]

        if pos is None:
            return None

        state_copy[pos] = Block.PLACEHOLDER

        new_gen = iter(self._group_neighbors(curr_generated, state=state_copy))
        iterables.append(new_gen)

        while iterables:
            # Another thread interrupted the covering
            if self.stopped:
                raise CoveringStoppedException

            last_gen = iterables[-1]
            try:
                generated_pos = next(last_gen)

                if not all((watcher.check_position(generated_pos)
                            for watcher in watcher_instances)):
                    # At least one constraint failed
                    continue

                for watcher in watcher_instances:
                    # Commit the new tile to watchers
                    watcher.commit()

                curr_generated.append(generated_pos)

                state_copy[generated_pos] = Block.PLACEHOLDER

                if len(curr_generated) == step_size:
                    if not check_finishable or \
                           self._is_finishable(state=state_copy):
                        return tuple(curr_generated)
                    state_copy[generated_pos] = Block.EMPTY
                    curr_generated.pop()
                    self.message("\t\t\tThe generated position was not "
                                 "finishable, trying another one...")
                else:
                    new_gen = iter(self._group_neighbors(curr_generated,
                                                         state=state_copy))
                    iterables.append(new_gen)

            except StopIteration:
                iterables.pop()
                last_pos = curr_generated.pop()
                state_copy[last_pos] = Block.EMPTY

                for watcher in watcher_instances:
                    # Return all watchers state to the one before the last
                    # position
                    watcher.rollback_state()

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

                if state[pos] is not Block.EMPTY:
                    continue

                # HACK (EMPTY == False, PLACEHOLDER == TRUE)
                if visited[pos] is not Block.EMPTY:
                    continue

                visited[pos] = Block.PLACEHOLDER
                component_size += 1  # Me

                for nei_pos in self.neighbors(pos):
                    stack.append(nei_pos)

            return component_size

        if state is None:
            state = self.state

        # A little hack, but provides exactly the interface we need
        visited = self._get_state_container()

        for pos in self.all_positions():
            if visited[pos] is not Block.EMPTY or \
                    state[pos] is not Block.EMPTY:
                continue
            component_size = dfs(pos)

            if self.min_block_size == self.max_block_size:
                if component_size % self.min_block_size != 0:
                    return False

            # If block size is ambiguous
            elif component_size < self.min_block_size:
                return False

        return True

    def add_constraint(self, watcher_cls):
        """
        Add a new model constraint watcher.

        This resets the model.
        """

        self.constraint_watchers.append(watcher_cls)
        self.reset()

    def remove_constraint(self, watcher_cls):
        """
        Remove a model constraint watcher from the list.

        This resets the model.
        """
        self.constraint_watchers.remove(watcher_cls)

        self.reset()


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
        self._state = [[Block.EMPTY for _ in range(width)]
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

    # pylint: disable=too-many-arguments
    def __init__(self, width, height,
                 min_block_size, max_block_size, verbosity=0):
        self.width = width
        self.height = height
        super().__init__(min_block_size, max_block_size, verbosity)

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
        Removes all blocks, resets position
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

    def neighbors(self, pos):
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
        self._state = [[[Block.EMPTY for _ in range(zs)]
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

    def __init__(self, pyramid_size, min_block_size, max_block_size,
                 verbosity=0):
        self.size = pyramid_size

        super().__init__(min_block_size, max_block_size, verbosity)

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

    def neighbors(self, pos):
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

    def set_size(self, size):
        """
        Sets the pyramid size (this resets current state)
        """
        self.size = size
        self.reset()
