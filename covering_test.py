"""
Unit tests for 2D covering program
"""

import unittest
import tkinter as tk
import itertools as it

from parameterized import parameterized

from covering import App

# TODO: Update to use the new interface (CoveringModel)


class TestApp(unittest.TestCase):
    """
    Tests for the App class
    """
    HEIGHT = 3
    WIDTH = 3
    BLOCK_SIZE = 3

    full = list(it.product(range(WIDTH), range(HEIGHT)))

    def setUp(self):
        root = tk.Tk()
        self.app = App(root)

        self.app.height = self.HEIGHT
        self.app.width = self.WIDTH
        self.app.block_size = self.BLOCK_SIZE
        self.app.reset_state()

    def _fill_positions(self, full_positions):
        for pos in full_positions:
            x, y = pos
            self.app.state[y][x] = 1

    @parameterized.expand([
        ("empty", [], (0, 0)),
        ("first_full", [(0, 0)], (1, 0)),
        ("row_full", [(0, 0), (1, 0), (2, 0)], (0, 1)),
        ("last_left", full[:-1], (2, 2)),
        ("full", full, None)
    ])
    def test_next_empty(self, _, full_positions, expected):
        """
        Parameterized test for next_empty method
        """
        self._fill_positions(full_positions)

        next_empty = self.app.next_empty((0, 0))
        self.assertEqual(next_empty, expected)

    @parameterized.expand([
        ("empty_corner", [], (0, 0), [(0, 1), (1, 0)]),
        ("empty_side", [], (1, 0), [(0, 0), (1, 1), (2, 0)]),
        ("empty_center", [], (1, 1), [(0, 1), (1, 0), (1, 2), (2, 1)]),
        ("partly_blocked", [(0, 1), (1, 0)], (1, 1), [(1, 2), (2, 1)]),
        ("blocked", [(0, 1), (1, 0), (1, 2), (2, 1)], (1, 1), [])
    ])
    def test_empty_neighbors(self, _, full_positions, pos, expected):
        """
        Parameterized test for empty_neighbors method
        """
        self._fill_positions(full_positions)

        neighbors = sorted(list(self.app.empty_neighbors(pos)))
        self.assertEqual(neighbors, expected)

    @parameterized.expand([
        ("empty", [], True),
        ("full", full, True),
        ("one_full", [(0, 0)], False),
        ("one_good_component", [(0, 0), (1, 0), (2, 0)], True),
        ("two_good_components", [(0, 1), (1, 1), (2, 1)], True),
        ("one_bad_component", [(0, 0), (1, 0)], False),
        ("two_bad_components", [(0, 0), (0, 1), (1, 1),
                                (2, 0), (2, 1)], False),
        ("one_good_one_bad", [(0, 0), (0, 1), (1, 1), (2, 0)], False)

    ])
    def test_is_finishable(self, _, full_positions, expected):
        """
        Parameterized test for is_finishable method
        """
        self._fill_positions(full_positions)

        finishable = self.app.is_finishable()
        self.assertEqual(finishable, expected)

    def test_valid_step(self):
        """
        Parameterized test for valid_step method

        For now we trust that the step is actually continuous
        """
        step = self.app.valid_step((0, 0))

        self.assertIsNotNone(step)

        for pos in step:
            x, y = pos
            self.app.state[y][x] = -1

        finishable = self.app.is_finishable()
        self.assertTrue(finishable)


if __name__ == "__main__":
    unittest.main()
