# -*- coding: utf-8 -*-

import unittest

from python.transformations import Rotation, Translation, Symmetry, ToIndex

class FakeBoard():

    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

    def get_size(self):
        x_size = self.max_x - self.min_x
        y_size = self.max_y - self.min_y
        return min(19, x_size), min(19, y_size)

class TestRotation(unittest.TestCase):
    """ Test the rotation transformation
    """

    def test_apply_points(self):
        """ Test the points rotation.
        """
        rotation = Rotation(FakeBoard(2, 1, 8, 5))
        self.assertEqual((4, 2), rotation.apply_points((2, 1)))

        rotation = Rotation(FakeBoard(0, 0, 6, 4))
        self.assertEqual((4, 0), rotation.apply_points((0, 0)))
        self.assertEqual((4, 3), rotation.apply_points((3, 0)))
        self.assertEqual((1, 0), rotation.apply_points((0, 3)))
        self.assertEqual((1, 3), rotation.apply_points((3, 3)))

        rotation = Rotation(FakeBoard(1, 1, 6, 4))
        self.assertEqual((4, 1), rotation.apply_points((1, 0)))



    def test_get_new_size(self):
        """ Test the goban size rotation.
        """
        rotation = Rotation(FakeBoard(2, 1, 8, 5))
        self.assertEqual((0, 2, 4, 8), rotation.get_new_size())

        rotation = Rotation(FakeBoard(0, 0, 6, 4))
        self.assertEqual((0, 0, 4, 6), rotation.get_new_size())

    def test_is_valid(self):
        """ Test the is_valid method.
        """

        # Do not rotate if height > width
        rotation = Rotation(FakeBoard(0, 0, 6, 4))
        self.assertTrue(rotation.is_valid())

        # Always rotate if width > height
        rotation = Rotation(FakeBoard(0, 0, 4, 6))
        self.assertFalse(rotation.is_valid())

        # May rotate if width = height (not tested here…)

class TestTranslation(unittest.TestCase):
    """ Test the translation transformation.
    """

    def test_apply_points(self):
        """ Test the points translation.
        """
        translation = Translation(FakeBoard(2, 1, 8, 5))
        self.assertEqual((0, 0), translation.apply_points((2, 1)))
        self.assertEqual((6, 4), translation.apply_points((8, 5)))

    def test_get_new_size(self):
        """ Test the goban size translation.
        """
        translation = Translation(FakeBoard(2, 1, 8, 5))

        self.assertEqual((0, 0, 6, 4), translation.get_new_size())

    def test_is_valid(self):
        """ Test the is_valid method.
        """

        translation = Translation(FakeBoard(1, 0, 6, 4))
        self.assertTrue(translation.is_valid())

        translation = Translation(FakeBoard(0, 1, 6, 4))
        self.assertTrue(translation.is_valid())

        translation = Translation(FakeBoard(0, 0, 4, 6))
        self.assertFalse(translation.is_valid())

class TestRotation(unittest.TestCase):
    """ Test the simetry transformation.
    """

    def test_apply_points(self):
        """ Test the points Symmetry.
        """
        symmetry = Symmetry(FakeBoard(2, 1, 8, 5))
        symmetry.x_flip = True
        symmetry.y_flip = False
        self.assertEqual((8, 1), symmetry.apply_points((2, 1)))
        self.assertEqual((2, 5), symmetry.apply_points((8, 5)))

        symmetry.x_flip = False
        symmetry.y_flip = True
        self.assertEqual((2, 5), symmetry.apply_points((2, 1)))
        self.assertEqual((8, 1), symmetry.apply_points((8, 5)))

    def test_get_new_size(self):
        """ Test the goban size Symmetry.
        """
        symmetry = Symmetry(FakeBoard(2, 1, 8, 5))

        self.assertEqual((2, 1, 8, 5), symmetry.get_new_size())

    def test_is_valid(self):
        """ Test the is_valid method.
        """

        symmetry = Symmetry(FakeBoard(1, 0, 6, 4))
        symmetry.x_flip = True
        self.assertTrue(symmetry.is_valid())


        symmetry = Symmetry(FakeBoard(0, 0, 4, 6))
        symmetry.x_flip = False
        symmetry.y_flip = False
        self.assertFalse(symmetry.is_valid())


class TestToIndex(unittest.TestCase):
    """ Test the toIndex transformation.
    """

    def test_apply_points(self):
        """ Test the points index.
        """
        toIndex = ToIndex(FakeBoard(2, 1, 8, 5))
        self.assertEqual(0, toIndex.apply_points((2, 1)))
        self.assertEqual(7, toIndex.apply_points((2, 2)))
        self.assertEqual(8, toIndex.apply_points((3, 2)))
