import unittest

import board


class TestBoardSetup(unittest.TestCase):

    def test_dimensions(self):
        brd = board.Board()
        self.assertEqual(brd.size, 10, 'incorrect size')

    def test_initialboard_is_empty(self):
        brd = board.Board()
        piece = board.Piece(((0, 0),))
        self.assertTrue(brd.isvalid(piece, 0, 0), 'topleft')
        self.assertTrue(brd.isvalid(piece, 9, 0), 'topright')
        self.assertTrue(brd.isvalid(piece, 0, 9), 'bottomleft')
        self.assertTrue(brd.isvalid(piece, 9, 9), 'bottomright')
        self.assertFalse(brd.isvalid(piece, -1, 9), 'outside left')
        self.assertFalse(brd.isvalid(piece, 10, 9), 'outside right')
        self.assertFalse(brd.isvalid(piece, 5, 10), 'outside down')
        self.assertFalse(brd.isvalid(piece, 5, -1), 'outside up')


class TestPieceSetup(unittest.TestCase):

    def test_pieces_and_blocks_are_tuples(self):
        with self.assertRaises(board.BoardError):
            board.Piece(())  # Empty tuple
        with self.assertRaises(board.BoardError):
            board.Piece(((1,),))  # Block should contain 2 elements
        with self.assertRaises(board.BoardError):
            board.Piece(((1, 2, 3),))  # Block should contain 2 elements
        with self.assertRaises(board.BoardError):
            board.Piece(((1, 2), (1, ),))  # all blocks should contain 2 elements
        with self.assertRaises(board.BoardError):
            board.Piece(((1, 2), (1, 2, 3)))  # Block should contain 2 elements

    def test_dimensions(self):
        piece = board.Piece(((0, 0), (1, 0)))
        self.assertEqual(piece.height, 2)
        self.assertEqual(piece.width, 1)

        piece = board.Piece(((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)))
        self.assertEqual(piece.height, 2)
        self.assertEqual(piece.width, 3)

    def test_all_pieces(self):
        self.assertEqual(len(board.allPieces), 19)

    def test_freqency_parameter(self):
        piece = board.Piece(((0, 0),))
        self.assertEqual(piece.frequency, 5)  # default frequency ~ 5 %
        piece = board.Piece(((0, 0),), 3)
        self.assertEqual(piece.frequency, 3)


class TestPutPiece(unittest.TestCase):

    def test_placepiece(self):
        piece = board.Piece(((0, 0), (1, 0)))
        brd = board.Board()

        brd.placepiece(piece, 0, 0)
        self.assertEqual(brd.board[0][0], 5, 'topblock')
        self.assertEqual(brd.board[1][0], 5, 'bottomblock')

        brd.placepiece(piece, 8, 9)
        self.assertEqual(brd.board[8][9], 5, 'topblock')
        self.assertEqual(brd.board[9][9], 5, 'bottomblock')

        with self.assertRaises(board.BoardError):  # outside
            brd.placepiece(piece, 9, 4)

    def test_placepiece_twice_doesnot_succeed(self):
        piece = board.Piece(((0, 0), (1, 0)))
        brd = board.Board()

        brd.placepiece(piece, 1, 0)
        with self.assertRaises(board.BoardError):
            brd.placepiece(piece, 1, 0)

    def test_placepiece_overlap_doesnot_succeed(self):
        piece = board.Piece(((0, 0), (1, 0)))
        brd = board.Board()

        brd.placepiece(piece, 1, 0)
        with self.assertRaises(board.BoardError):
            brd.placepiece(piece, 0, 0)

    def test_completerow_removes_blocks(self):
        piece = board.Piece(((0, 0), (1, 0)))
        brd = board.Board()
        brd.placepiece(piece, 0, 0)
        brd.placepiece(piece, 2, 0)
        brd.placepiece(piece, 4, 0)
        brd.placepiece(piece, 6, 0)
        self.assertEqual(brd.board[0][0], 5)
        self.assertEqual(brd.board[1][0], 5)
        self.assertEqual(brd.board[2][0], 5)
        self.assertEqual(brd.board[3][0], 5)
        self.assertEqual(brd.board[4][0], 5)
        self.assertEqual(brd.board[5][0], 5)
        self.assertEqual(brd.board[6][0], 5)
        self.assertEqual(brd.board[7][0], 5)
        self.assertEqual(brd.board[8][0], 0)
        self.assertEqual(brd.board[9][0], 0)
        brd.placepiece(piece, 8, 0)
        self.assertEqual(brd.board[0][0], 0, 'block 1 removed')
        self.assertEqual(brd.board[1][0], 0)
        self.assertEqual(brd.board[2][0], 0)
        self.assertEqual(brd.board[3][0], 0)
        self.assertEqual(brd.board[4][0], 0)
        self.assertEqual(brd.board[5][0], 0)
        self.assertEqual(brd.board[6][0], 0)
        self.assertEqual(brd.board[7][0], 0)
        self.assertEqual(brd.board[8][0], 0)
        self.assertEqual(brd.board[9][0], 0)

    def test_complete2rows_removes_blocks(self):
        piece = board.Piece(((0, 0), (1, 0), (0, 1), (1, 1)))
        brd = board.Board()
        for i in [0, 2, 4, 6, 8]:  # Place a complete row
            brd.placepiece(piece, i, 0)
        for i in [0, 2, 4, 6, 8]:  # Doing it agian is OK
            brd.placepiece(piece, i, 0)

    def test_complete2rows_and_cols_removes_blocks(self):
        piece = board.Piece(((0, 0), (1, 0), (0, 1), (1, 1)))
        brd = board.Board()
        for i in [2, 4, 6, 8]:  # prepare columns and rows
            brd.placepiece(piece, 0, i)
            brd.placepiece(piece, i, 0)
        brd.placepiece(piece, 0, 0)  # Completes 2 rows and 2 columns
        brd.placepiece(piece, 0, 0)  # Can do it again
        brd.placepiece(piece, 2, 0)  # place on cleared column
        brd.placepiece(piece, 0, 6)  # place on row

    def test_scorepiece_empty_board(self):
        brd = board.Board()
        piece = board.Piece(((0, 0), (1, 0), (0, 1), (1, 1)))
        self.assertEqual(brd.scorepiece(piece, 0, 0), -8)
        self.assertEqual(brd.scorepiece(piece, 2, 3), -18)


class TestScoring(unittest.TestCase):

    def test_single_pieces(self):
        piece = board.Piece(((0, 0), (1, 0), (0, 1), (1, 1)))
        brd = board.Board()
        brd.placepiece(piece, 0, 0)
        self.assertEqual(brd.score, 4, 'first square')
        brd.placepiece(piece, 2, 0)
        self.assertEqual(brd.score, 8, 'second square')

    def test_complete_single_row_scores_10(self):
        piece = board.Piece(((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)))
        brd = board.Board()
        brd.placepiece(piece, 0, 0)
        brd.placepiece(piece, 5, 0)
        self.assertEqual(brd.score, 20)  # 10 for pieces, 10 for row

    def test_complete_double_row_scores_30(self):
        piece = board.Piece(((0, 0), (1, 0), (0, 1), (1, 1)))
        brd = board.Board()
        for i in [0, 2, 4, 6, 8]:  # Place 2 complete rows
            brd.placepiece(piece, i, 0)
        self.assertEqual(brd.score, 50)  # 20 for pieces, 30 for 2 rows

    def test_complete_triple_row_scores_60(self):
        piece = board.Piece(((0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)))
        brd = board.Board()
        for i in [0, 2, 4, 6, 8]:  # Place 2 complete rows
            brd.placepiece(piece, i, 0)
        self.assertEqual(brd.score, 90)  # 30 for pieces, 60 for 3 rows

    def test_complete_4_rows_scores_100(self):
        piece = board.Piece(((0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2), (0, 3), (1, 3)))
        brd = board.Board()
        for i in [0, 2, 4, 6, 8]:  # Place 2 complete rows
            brd.placepiece(piece, i, 0)
        self.assertEqual(brd.score, 140)  # 40 for pieces, 100 for 4 rows

    def test_complete_2_rows_2_cols_scores_100(self):
        piece = board.Piece(((0, 0), (1, 0), (0, 1), (1, 1)))
        brd = board.Board()
        for i in [2, 4, 6, 8]:  # prepare columns and rows
            brd.placepiece(piece, 0, i)
            brd.placepiece(piece, i, 0)
        brd.placepiece(piece, 0, 0)  # Completes 2 rows and 2 columns
        self.assertEqual(brd.score, 136)  # 36 for pieces, 100 for 4 rows


class TestMoves(unittest.TestCase):

    def test_availablelocations_emptyboard(self):
        brd = board.Board()
        locations = brd.validlocations(board.allPieces[0])
        self.assertEqual(len(locations), 100)
        locations = brd.validlocations(board.allPieces[1])
        self.assertEqual(len(locations), 90)
        locations = brd.validlocations(board.allPieces[10])
        self.assertEqual(len(locations), 64)

    def test_availablelocations_filled_board(self):
        brd = board.Board()
        brd.placepiece(board.allPieces[10], 0, 0)
        locations = brd.validlocations(board.allPieces[0])
        self.assertEqual(len(locations), 91)
        locations = brd.validlocations(board.allPieces[1])
        self.assertEqual(len(locations), 81)
        locations = brd.validlocations(board.allPieces[10])
        self.assertEqual(len(locations), 55)
        brd.placepiece(board.allPieces[10], 4, 0)
        locations = brd.validlocations(board.allPieces[0])
        self.assertEqual(len(locations), 82)
        locations = brd.validlocations(board.allPieces[1])
        self.assertEqual(len(locations), 69)
        locations = brd.validlocations(board.allPieces[10])
        self.assertEqual(len(locations), 43)

    def test_all_available_locations(self):
        brd = board.Board()
        self.assertEqual(brd.totalavailable(), 1425)

        brd.placepiece(board.allPieces[9], 0, 0)
        self.assertEqual(brd.totalavailable(), 1354)

    def test_maxgapperline(self):
        brd = board.Board()
        self.assertEqual(brd.maxgapperline(), 200)

        brd.placepiece(board.allPieces[9], 3, 4)
        self.assertEqual(brd.maxgapperline(), 178)

    def test_availablelocationssorted_emptyboard(self):
        brd = board.Board()
        locations = brd.validlocationssorted(board.allPieces[0])
        self.assertEqual(len(locations), 100)
        locations = brd.validlocationssorted(board.allPieces[1])
        self.assertEqual(len(locations), 90)
        locations = brd.validlocationssorted(board.allPieces[10])
        self.assertEqual(len(locations), 64)
