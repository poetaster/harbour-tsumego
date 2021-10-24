# -*- coding: utf-8 -*-

import random
random.seed()

class Translation(object):
    """ A translation transformation.
    """

    def __init__(self, board):
        """ Create a new translation from the board.
        """
        self.board = board

    def is_valid(self):
        """ Apply if a translation if the goban is not maximized.
        """
        return self.board.min_x != 0 or self.board.min_y != 0

    def apply_points(self, coord, name = None):
        """ Move the points to the lower position.
        """
        x, y = coord
        return (x - self.board.min_x, y - self.board.min_y)

    def get_new_size(self):
        """ The goban size does not change.
        """
        return 0, 0, self.board.max_x - self.board.min_x, self.board.max_y - self.board.min_y

    def get_new_side(self):
        """ There is no changes on the sides.
        """
        return self.board.side

class Rotation(object):
    """ A rotation transformation.
    """

    def __init__(self, board):
        """ Create a new roation from the board.
        """
        self.board = board

    def is_valid(self):
        """ Apply the rotation in following cases :
        * if the board is widther than heigther
        * randomly is width == heigth
        * never if the board is heigther than widther
        """

        width, heigth = self.board.get_size()
        should = heigth - width
        if should == 0:
            return random.randint(0, 1) == 1
        return should < 0

    def apply_points(self, coord, name = None):
        """ Apply the transformation on a point.
        """
        x, y = coord
        return (self.board.max_y - y, x)

    def get_new_size(self):
        """ Apply the transformation on the goban size.
        """
        max_x = self.board.max_y - self.board.min_y
        return 0, self.board.min_x, max_x, self.board.max_x

    def get_new_side(self):
        """ Apply the transformations on the sides.
        """
        return {
            "BOTTOM":   self.board.side["RIGHT"],
            "RIGHT":  self.board.side["TOP"],
            "LEFT": self.board.side["BOTTOM"],
            "TOP":self.board.side["LEFT"]
        }

class Symmetry(object):
    """ A translation transformation.
    """

    def __init__(self, board):
        self.board = board

        self.x_flip = random.randint(0, 1) == 1
        self.y_flip = random.randint(0, 1) == 1

    def is_valid(self):
        """ The transformation is valid if one flip is required in one
        direction.  """
        return self.x_flip or self.y_flip

    def apply_points(self, coord, name = None):
        """ Flip in both directions.
        """
        x, y = coord
        if self.x_flip:
            new_x = self.board.max_x - x + self.board.min_x
        else:
            new_x = x

        if self.y_flip:
            new_y = self.board.max_y - y + self.board.min_y
        else:
            new_y = y

        return (new_x, new_y)

    def get_new_size(self):
        """ The size is not changed.
        """
        return self.board.min_x, self.board.min_y, self.board.max_x, self.board.max_y

    def get_new_side(self):
        """ There is no changes on the sides.
        """
        return {
            "TOP":   self.board.side["BOTTOM" if self.y_flip else "TOP"],
            "LEFT":  self.board.side["RIGHT" if self.x_flip else "LEFT"],
            "RIGHT": self.board.side["LEFT" if self.x_flip else "RIGHT"],
            "BOTTOM":self.board.side["TOP" if self.y_flip else "BOTTOM"]
        }

class ToIndex(object):
    """" Transform each point position in point index.
    """

    def __init__(self, board):
        self.board = board

    def is_valid(self):
        """ This transformation is always valid.
        """
        return True;

    def apply_points(self, coord, name = None):
        """
        """
        x_size = min(19, self.board.max_x - self.board.min_x + 1)
        x, y = coord
        return (x - self.board.min_x) + (y - self.board.min_y) * x_size

    def get_new_size(self):
        """ The size is not changed.
        """
        return self.board.min_x, self.board.min_y, self.board.max_x, self.board.max_y

    def get_new_side(self):
        """ There is no changes on the sides.
        """
        return self.board.side
