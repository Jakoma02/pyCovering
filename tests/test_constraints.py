"""
Unittest for the constraints module
"""

# pylint: disable=missing-function-docstring

import unittest

from parameterized import parameterized

from pycovering.models import TwoDCoveringModel, PyramidCoveringModel, Block
from pycovering.constraints import PathConstraintWatcher, \
                                   PlanarConstraintWatcher


class ConstraintWatcherTest(unittest.TestCase):
    """
    A common superclass for testing constraint watchers
    """
    # Subclasses will set the members before using these functions
    # pylint: disable=no-member
    def _insert_while_checking(self, position, expected):
        check_res = self.watcher.check_position(position)
        self.assertEqual(check_res, expected)

        if check_res is True:
            self.model.state[position] = Block.PLACEHOLDER
            self.watcher.commit()

    def _insert_initial(self, positions):
        for pos in positions:
            self._insert_while_checking(pos, True)


class TestPathConstraintWatcher(ConstraintWatcherTest):
    """
    Tests for the PathConstraintWatcher class
    """
    INITIAL_POS = (0, 0)

    def setUp(self):
        self.model = TwoDCoveringModel(4, 4, 4, 4)
        self.watcher = PathConstraintWatcher(self.model, self.INITIAL_POS)
        self.model.state[self.INITIAL_POS] = Block.PLACEHOLDER

    @parameterized.expand([
        ("Good", (0, 3), True),
        ("Bad", (1, 1), False)
    ])
    def test_check_position(self, _, adding, expected):
        added_positions = [
            (0, 1),
            (0, 2)
        ]

        self._insert_initial(added_positions)
        self._insert_while_checking(adding, expected)

    def test_rollback_state(self):
        added_positions = [
            (0, 1),
            (0, 2),
            (0, 3)
        ]

        self._insert_initial(added_positions)
        self.watcher.rollback_state()
        self.watcher.rollback_state()
        self._insert_while_checking((1, 1), True)


class TestPlanarConstraintWatcher(ConstraintWatcherTest):
    """
    Tests for the PlanarConstraintWatcher class
    """
    INITIAL_POS = (0, 0, 0)

    def setUp(self):
        self.model = PyramidCoveringModel(3, 5, 5)
        self.watcher = PlanarConstraintWatcher(self.model, self.INITIAL_POS)
        self.model.state[self.INITIAL_POS] = Block.PLACEHOLDER

    @parameterized.expand([
        ("Good", (2, 0, 0), True),
        ("Bad", (0, 0, 1), False)
    ])
    def test_check_position(self, _, adding, expected):
        added_positions = [
            (1, 0, 0),
            (0, 1, 0)
        ]

        self._insert_initial(added_positions)
        self._insert_while_checking(adding, expected)

    def test_rollback_state(self):
        added_positions = [
            (1, 0, 0),
            (0, 1, 0)
        ]

        self._insert_initial(added_positions)
        self.watcher.rollback_state()
        self._insert_while_checking((0, 0, 1), True)
