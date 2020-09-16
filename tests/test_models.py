"""
Unittest for the models module
"""

# pylint: disable=missing-function-docstring

import unittest
import itertools as it

from parameterized import parameterized

from pycovering.models import TwoDCoveringModel, PyramidCoveringModel, Block


class TestTwoDCoveringModel(unittest.TestCase):
    """
    Tests for the TwoDCoveringModel class
    """
    WIDTH = 4
    HEIGHT = 4

    ALL_POSITIONS = list(it.product(range(WIDTH), range(HEIGHT)))

    def setUp(self):
        self.model = TwoDCoveringModel(self.WIDTH, self.HEIGHT, 4, 4)

    def test_all_positions(self):
        positions = set(self.model.all_positions())
        expected = set(it.product(range(self.WIDTH), range(self.HEIGHT)))

        self.assertEqual(positions, expected)

    def test_reset(self):
        self.model.add_block(self.ALL_POSITIONS)
        self.model.reset()

        self.assertFalse(self.model.is_filled())

        for pos in self.model.all_positions():
            self.assertEqual(self.model.state[pos], Block.EMPTY,
                             f"Position {pos} should be empty, but is not")

    @parameterized.expand([
        ("empty", [], False),
        ("partially_filled", [(0, 0), (1, 1)], False),
        ("filled", ALL_POSITIONS, True)
    ])
    def test_is_filled(self, _, filled, expected):
        self.model.add_block(filled)

        self.assertEqual(self.model.is_filled(), expected)

    def test_total_positions(self):
        self.assertEqual(self.model.total_positions(), 16)

    def test_add_tile(self):
        tile1 = [(0, 0), (0, 1), (0, 2)]
        tile2 = [(1, 0), (1, 1), (1, 2)]

        self.model.add_block(tile1)
        self.model.add_block(tile2)

        self.assertEqual(self.model.block_nu, 3)

        for pos in tile1:
            self.assertEqual(self.model.state[pos].number, 1)

        for pos in tile2:
            self.assertEqual(self.model.state[pos].number, 2)

    def test_empty_positions(self):
        total = self.model.total_positions()

        tile1 = [(0, 0), (0, 1), (0, 2)]
        tile2 = [(1, 0), (1, 1), (1, 2)]

        self.model.add_block(tile1)
        self.assertEqual(self.model.empty_positions(), total - 3)

        self.model.add_block(tile2)
        self.assertEqual(self.model.empty_positions(), total - 6)


class TestPyramidCoveringModel(unittest.TestCase):
    """
    Tests for the PyramidCoveringModel class
    """
    ALL_POSITIONS = [
        (0, 0, 0),
        (1, 0, 0),
        (2, 0, 0),
        (0, 1, 0),
        (1, 1, 0),
        (0, 2, 0),
        (0, 0, 1),
        (1, 0, 1),
        (0, 1, 1),
        (0, 0, 2),
    ]

    def setUp(self):
        self.model = PyramidCoveringModel(3, 5, 5)

    def test_all_positions(self):
        all_pos = set(self.model.all_positions())
        expected = set(self.ALL_POSITIONS)

        self.assertEqual(all_pos, expected)

    def test_reset(self):
        self.model.add_block(self.ALL_POSITIONS)
        self.model.reset()

        self.assertFalse(self.model.is_filled())

        for pos in self.model.all_positions():
            self.assertEqual(self.model.state[pos], Block.EMPTY,
                             f"Position {pos} should be empty, but is not")

    @parameterized.expand([
        ("empty", [], False),
        ("partially_filled", [(0, 0, 0), (0, 1, 1)], False),
        ("filled", ALL_POSITIONS, True)
    ])
    def test_is_filled(self, _, filled, expected):
        self.model.add_block(filled)

        self.assertEqual(self.model.is_filled(), expected)

    def test_total_positions(self):
        self.assertEqual(self.model.total_positions(), 10)

    def test_add_tile(self):
        tile1 = [(0, 0, 0), (0, 1, 0), (0, 0, 1)]
        tile2 = [(1, 0, 0), (2, 0, 0), (1, 1, 0)]

        self.model.add_block(tile1)
        self.model.add_block(tile2)

        self.assertEqual(self.model.block_nu, 3)

        for pos in tile1:
            self.assertEqual(self.model.state[pos].number, 1)

        for pos in tile2:
            self.assertEqual(self.model.state[pos].number, 2)

    def test_empty_positions(self):
        total = self.model.total_positions()

        tile1 = [(0, 0, 0), (0, 1, 0), (0, 0, 1)]
        tile2 = [(1, 0, 0), (2, 0, 0), (1, 1, 0)]

        self.model.add_block(tile1)
        self.assertEqual(self.model.empty_positions(), total - 3)

        self.model.add_block(tile2)
        self.assertEqual(self.model.empty_positions(), total - 6)
