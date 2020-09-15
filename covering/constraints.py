class GeneralConstraintWatcher:
    def __init__(self):
        self._states = []

    def rollback_state(self):
        self._states.pop()

    def commit(self):
        raise NotImplementedError

    def check_position(self, pos):
        """
        Returns True or False

        TODO: Rewrite docstring
        """
        raise NotImplementedError


class PathConstraintWatcher(GeneralConstraintWatcher):
    def __init__(self, model, pos, state):
        self.model = model
        self._state = state
        self._states = []

        self.end1 = pos
        self.end2 = pos

        self.commit()

    def _load_last_state(self):
        self.end1, self.end2 = self._states[-1]

    def check_position(self, pos):
        from covering.models import Block

        self._load_last_state()

        pos_neighbors = list(self.model._neighbors(pos))
        block_neighbors = [x for x in pos_neighbors
                           if self._state[x] is Block.PLACEHOLDER]

        # If more than one neighbors are placeholders, then this is not a path
        if len(block_neighbors) > 1:
            return False

        if self.end1 in block_neighbors:
            self.end1 = pos
            return True

        if self.end2 in block_neighbors:
            self.end2 = pos
            return True

        return False

    def commit(self):
        new_state = (self.end1, self.end2)
        self._states.append(new_state)


def string_constraint(model, group):
    """
    No four positions shall be adjecent to each other
    """

    # TODO: Fix

    # The constraint was fulfilled before adding the last position,
    # it is sufficent to check the number of neighbors for the last
    # position

    last_pos = group[-1]

    neighbors = model._neighbors(last_pos)
    in_group = [x for x in group if x in neighbors]

    # print(group)

    return len(in_group) <= 2


def path_constraint(model, group):
    """
    The positions make up a path
    """
    if len(group) == 1:
        return True

    last_pos = group[-1]

    neighbors = set(model._neighbors(last_pos))
    in_group = [x for x in group if x in neighbors]

    # The last position extends the path
    if (len(in_group) == 1) and (in_group[0] in (group[-2], group[0])):
        return True

    return False
