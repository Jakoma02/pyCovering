"""
This module contains constraint watchers.

A constraint watcher is a class, responsible for deciding whether given
position can be added to a block without breaking the constraint -- e.g. that
the block must be planar.  It maintains its state, so that some calculations
don't have to be done over and over.

Watchers are *persistant* -- they remember all of their previous states and can
be rolled back to a previous state, which is useful while backtracking.
"""


class GeneralConstraintWatcher:
    """
    This is and abstract class that all watchers should subclass.
    """
    # Implementations will use the arguments
    # pylint: disable=unused-argument
    def __init__(self, model, pos, state):
        self.model = model
        self._state = state  # Model state copy, this will be used
        self._states = []

    def rollback_state(self):
        """
        Return watcher state to a previous one.
        """
        self._states.pop()

    def commit(self):
        """
        Confirm adding last checked position, save current watcher state.
        """
        raise NotImplementedError

    def _load_last_state(self):
        raise NotImplementedError

    def check_position(self, pos):
        """
        Returns True if adding `pos` to the block doesn't break the constraint.
        This modifies the inner state, so that it can be saved with
        `self.commit()`
        """
        self._load_last_state()


class PathConstraintWatcher(GeneralConstraintWatcher):
    """
    This watcher ensures that all blocks forms a path. It only allows adding
    new positions to the ends of the path.
    """
    def __init__(self, model, pos, state):
        super().__init__(model, pos, state)

        self.end1 = pos
        self.end2 = pos

        self.commit()

    def _load_last_state(self):
        self.end1, self.end2 = self._states[-1]

    def check_position(self, pos):
        # This is a bit ugly... but is needed, would introduce a circular
        # import
        # pylint: disable=import-outside-toplevel
        from covering.models import Block

        super().check_position(pos)

        pos_neighbors = list(self.model.neighbors(pos))
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
