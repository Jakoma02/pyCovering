"""
This module contains constraint watchers.

A constraint watcher is a class, responsible for deciding whether given
position can be added to a block without breaking the constraint -- e.g. that
the block must be planar.  It maintains its state, so that some calculations
don't have to be done over and over.

Watchers are *persistent* -- they remember all of their previous states and can
be rolled back to a previous state, which is useful while backtracking.
"""

from math import isclose


class GeneralConstraintWatcher:
    """
    This is and abstract class that all watchers should subclass.
    """
    # Implementations will use the arguments
    # pylint: disable=unused-argument
    def __init__(self, model, pos):
        # Don't save state, use the model built in one...
        # but be careful to return it as is was
        self.model = model
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
    def __init__(self, model, pos):
        super().__init__(model, pos)

        self.end1 = pos
        self.end2 = pos

        self.commit()

    def _load_last_state(self):
        self.end1, self.end2 = self._states[-1]

    def check_position(self, pos):
        # This is a bit ugly... but is needed, would introduce a circular
        # import
        # pylint: disable=import-outside-toplevel
        from pycovering.models import Block

        super().check_position(pos)

        pos_neighbors = list(self.model.neighbors(pos))
        block_neighbors = [x for x in pos_neighbors
                           if self.model.state[x] is Block.PLACEHOLDER]

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


class Vector:
    """
    A simple 3D vector implementation, used to represent points as well
    """
    def __init__(self, x, y, z):
        self.coords = (x, y, z)

    def __sub__(self, other):
        x1, y1, z1 = self.coords
        x2, y2, z2 = other.coords

        return Vector(
            x1 - x2,
            y1 - y2,
            z1 - z2
        )

    def vector_product(self, other):
        """
        Return a new vector that is the vector product self X other
        """
        x1, y1, z1 = self.coords
        x2, y2, z2 = other.coords

        prod1 = y1 * z2 - z1 * y2
        prod2 = z1 * x2 - x1 * z2
        prod3 = x1 * y2 - y1 * x2

        return Vector(prod1, prod2, prod3)

    @staticmethod
    def _are_all_close(arr):
        if len(arr) < 2:
            return True

        for i in range(1, len(arr)):
            if not isclose(arr[i - 1], arr[i]):
                return False

        return True

    def is_dependent(self, other):
        """
        Return true if self and other are linearly dependent
        """
        coeff = []

        # This is done to avoid division by zero.
        # Two vectors cannot be linearly dependent
        # if only one has zero at the same position
        # (and none is an zero vector)
        for coresp in zip(self.coords, other.coords):
            zero_count = coresp.count(0)
            if zero_count == 1:
                return False
            if zero_count == 2:
                continue  # Ignore

            coeff.append(coresp[0] / coresp[1])

        return self._are_all_close(coeff)


class Plane:
    """
    A simple plane implementation, only allows checking whether a point lies
    within the plane.
    """
    def __init__(self, point1, point2, point3):
        vector1 = point2 - point1
        vector2 = point3 - point1

        self.normal_vect = vector1.vector_product(vector2)
        self.constant_member = self.evaluate(point1)

    # The names are short, but domain-specific
    # pylint: disable=invalid-name
    def evaluate(self, point):
        """
        Calculate ax + by + cz (where a,b,c are constants specific for the
        plane and x,y,z are coordinates of the point).

        All points contained within one plane (parallel with the original one)
        will yield the same value.
        """
        x, y, z = point.coords
        a, b, c = self.normal_vect.coords

        return a * x + b * y + c * z

    def contains(self, point):
        """
        Returns True if point lies in the plane.
        """
        return self.evaluate(point) == self.constant_member


class PlanarConstraintWatcher(GeneralConstraintWatcher):
    """
    This watcher ensures that all blocks lie within one plane.
    It can ONLY be used with 3-dimensional covering models.
    """
    def __init__(self, model, pos):
        super().__init__(model, pos)

        self.plane = None

        self._points = [Vector(*pos)]
        self.commit()

    def commit(self):
        new_state = (self._points[:], self.plane)
        self._states.append(new_state)

    def _load_last_state(self):
        self._points, self.plane = self._states[-1][0][:], self._states[-1][1]

    # pylint: disable=too-many-locals
    @staticmethod
    def _on_the_same_line(pos1, pos2, pos3):
        vector1 = pos2 - pos1
        vector2 = pos3 - pos1

        return vector1.is_dependent(vector2)

    def check_position(self, pos):
        super().check_position(pos)

        x, y, z = pos
        new_point = Vector(x, y, z)

        # Two points are always OK
        if len(self._points) < 2:
            self._points.append(new_point)
            return True

        # Add third point only if it doesn't
        # lie on the same line as the other two
        if len(self._points) == 2:
            point1, point2 = self._points

            if not self._on_the_same_line(point1, point2, new_point):
                self._points.append(new_point)
                # Figure out which plane
                self.plane = Plane(point1, point2, new_point)

            return True

        # Other points must lie on the plane
        return self.plane.contains(new_point)
