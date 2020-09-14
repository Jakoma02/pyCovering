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
    def __init__(self, model):
        self.model = model
        self._states = [(None, None)]

        self.end1 = None
        self.end2 = None

    def _load_last_state(self):
        self.end1, self.end2 = self._states[-1]

    def check_position(self, pos):
        self._load_last_state()

        if self.end1 is None:
            self.end1 = pos
            self.end2 = pos
            return True

        e1_neighbors = self.model._neighbors(self.end1)
        if pos in e1_neighbors:
            self.end1 = pos

            if self.end2 is None:
                self.end2 = self.end1

            return True

        e2_neighbors = self.model._neighbors(self.end2)
        if pos in e2_neighbors:
            self.end2 = pos

            if self.end1 is None:
                self.end1 = self.end2

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
