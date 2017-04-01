import unittest

import board


class TestSingleMove(unittest.TestCase):

    def test_evaluate_piece(self):
        brd = board.Board()
        plr = board.Player()
        score = plr.testpiece(brd, board.allPieces[2], 0, 0)
        self.assertEqual(score, 2)
        brd.placepiece(board.allPieces[2], 0, 0)
        with self.assertRaises(board.BoardError):
            plr.testpiece(brd, board.allPieces[2], 0, 0)
        score = plr.testpiece(brd, board.allPieces[2], 2, 0)
        self.assertEqual(score, 2)

    def test_all_available_locations(self):
        brd = board.Board()
        plr = board.Player()
        self.assertEqual(plr.totalavailable(brd), 1425)

        brd.placepiece(board.allPieces[9], 0, 0)
        self.assertEqual(plr.totalavailable(brd), 1354)

    def test_max_score_after_move(self):
        brd = board.Board()
        plr = board.Player()
        # fill a colum with a single missing piece
        brd.placepiece(board.allPieces[1], 0, 2)
        brd.placepiece(board.allPieces[1], 2, 2)
        brd.placepiece(board.allPieces[1], 6, 2)
        brd.placepiece(board.allPieces[1], 8, 2)
        position = plr.getmaxscore(brd, board.allPieces[1])
        self.assertEqual(position[0], 4)
        self.assertEqual(position[1], 2)
