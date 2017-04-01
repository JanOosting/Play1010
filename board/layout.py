import numpy


class BoardError(Exception):
    """Base class for module errors"""
    pass


def allnonzero(x):
    return min(x) > 0


def which(x):
    # Identify indexes of true vaules in an (1-dim) array
    return [i for i, j in enumerate(x) if j]


class Board:

    def __init__(self):
        self.size = 10
        self.board = numpy.zeros((self.size, self.size))
        self.score = 0

    def clearrow(self, row):
        for i in xrange(self.size):
            self.board[row][i] = 0

    def clearcol(self, col):
        for i in xrange(self.size):
            self.board[i][col] = 0

    def isvalid(self, piece, row, col):
        found = False
        if row < 0 or col < 0 or row > self.size - piece.height or col > self.size - piece.width:
            found = True
        else:
            for block in piece.blocks:
                if self.board[row + block[0]][col + block[1]] != 0:
                    found = True
        return not found

    def placepiece(self, piece, row, col):
        if self.isvalid(piece, row, col):
            for block in piece.blocks:
                self.board[row + block[0]][col + block[1]] = 1
            self.score += len(piece.blocks)
            # Check complete rows, cols
            complete_rows = which(numpy.apply_along_axis(allnonzero, 1, self.board))
            complete_cols = which(numpy.apply_along_axis(allnonzero, 0, self.board))
            for complete_row in complete_rows:
                self.clearrow(complete_row)
            for complete_col in complete_cols:
                self.clearcol(complete_col)
            total_complete = len(complete_rows) + len(complete_cols)
            for line in xrange(total_complete):
                self.score += 10 * (line + 1)
        else:
            raise BoardError

    def validlocations(self, piece):
        """generate a list of possible loactions for the piece"""
        result = []
        for col in xrange(11 - piece.width):
            for row in xrange(11 - piece.height):
                if self.isvalid(piece, row, col):
                    result.append(((row, col),))
        return result


class Piece:

    def __init__(self, blocks):
        self.blocks = blocks
        self.width = 1
        self.height = 1
        if not isinstance(blocks, tuple):
            raise BoardError
        if len(blocks) < 1:
            raise BoardError
        for block in blocks:
            if not isinstance(block, tuple):
                raise BoardError
            if len(block) != 2:
                raise BoardError
            self.height = max(self.height, block[0] + 1)
            self.width = max(self.width, block[1] + 1)

allPieces = [Piece(((0, 0),)),
             Piece(((0, 0), (1, 0))),
             Piece(((0, 0), (0, 1))),
             Piece(((0, 0), (1, 0), (2, 0))),
             Piece(((0, 0), (0, 1), (0, 2))),
             Piece(((0, 0), (1, 0), (2, 0), (3, 0))),
             Piece(((0, 0), (0, 1), (0, 2), (0, 3))),
             Piece(((0, 0), (1, 0), (2, 0), (3, 0), (4, 0))),
             Piece(((0, 0), (0, 1), (0, 2), (0, 3), (0, 4))),
             Piece(((0, 0), (1, 0), (0, 1), (1, 1))),
             Piece(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2))),
             Piece(((1, 0), (0, 1), (1, 1))),
             Piece(((0, 0), (0, 1), (1, 1))),
             Piece(((0, 0), (1, 0), (1, 1))),
             Piece(((0, 0), (1, 0), (0, 1))),
             Piece(((0, 0), (1, 0), (2, 0), (0, 1), (0, 2))),
             Piece(((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))),
             Piece(((0, 0), (0, 1), (0, 2), (1, 2), (2, 2))),
             Piece(((2, 0), (2, 1), (0, 2), (1, 2), (2, 2))),
             ]
