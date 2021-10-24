# -*- coding: utf-8 -*-

import unittest
from python import sgfparser, game

def create_board(fic):
   with open("python/tests/%s" % fic) as f:
       cursor = sgfparser.Cursor(f.read())

   return game.Game(cursor)

class TestBoard(unittest.TestCase):
    """ Test for the board management.
    """

    def testConvCoord(self):
        """ Test the conversion in the coordinates system.
        """

        self.assertEqual((1,2),game.Game.conv_coord("ab"))
        self.assertEqual((1,1),game.Game.conv_coord("aa"))

    def test_createTree(self):

        def fun(pos, action):
            return pos

        with open("python/tests/test.sgf") as f:
            cursor = sgfparser.Cursor(f.read())

        cursor.next()

        expected_tee = \
            [{'AB': ['or', 'pr', 'qr', 'rr', 'sr'], 'AW': ['ro', 'nq', 'oq', 'pq', 'qq', 'rq', 'mr']},
                [
                    [{'W': ['os']},
                        [
                            [{'B': ['ps']}, {'W': ['rs']}, {'B': ['ns']}, {'W': ['nr']}],
                            [{'B': ['ns']}, {'W': ['nr']}, {'B': ['rs']}, {'W': ['ps']}, {'B': ['qs']}, {'W': ['os']}]
                        ]
                    ],
                    [{'W': ['rs']},
                        [
                            [{'B': ['os']}, {'W': ['qs']}],
                            [{'B': ['qs']}, {'W': ['os']}, {'B': ['nr']}, {'W': ['ns']}]
                        ]
                    ]
                ]
            ]
        self.assertEqual(expected_tee, game.Game.create_tree(cursor, fun))

    def test_init(self):

        def fun(pos):
            return (0,0)
        currentgame = create_board("test.sgf")

        self.assertEqual(11, currentgame.min_x)
        self.assertEqual(13, currentgame.min_y)
        self.assertEqual(19, currentgame.max_x)
        self.assertEqual(19, currentgame.max_y)

        self.assertEqual((9, 7), currentgame.get_size())

        # There is only 2 state : initial board, and 2 possibilities.
        self.assertEqual(2, len(currentgame.tree))

        self.assertFalse(currentgame.side['TOP'])
        self.assertFalse(currentgame.side['LEFT'])
        self.assertTrue(currentgame.side['BOTTOM'])
        self.assertTrue(currentgame.side['RIGHT'])

        currentgame.normalize()

        self.assertEqual('W', currentgame.current_player)

