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
        self.board = numpy.zeros((self.size, self.size), numpy.int32)
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

    def scorepiece(self, piece, row, col):
        result = -100
        tmpboard = numpy.copy(self.board)
        collision = False
        if 0 <= row <= self.size - piece.height and 0 <= col <= self.size - piece.width:
            for block in piece.blocks:
                if self.board[row + block[0]][col + block[1]] != 0:
                    collision = True
                    break
                else:
                    tmpboard[row + block[0]][col + block[1]] = -1
        if not collision:
            totalgapsbefore = 0
            totalgapsafter = 0
            for arow in xrange(piece.height):
                maxgapbefore = 0
                maxgapafter = 0
                gapbefore = 0
                gapafter = 0
                for acol in xrange(self.size):
                    if tmpboard[row + arow][acol] > 0:
                        if gapbefore > maxgapbefore:
                            maxgapbefore = gapbefore
                        gapbefore = 0
                    else:
                        gapbefore += 1
                    if tmpboard[row + arow][acol] != 0:
                        if gapafter > maxgapafter:
                            maxgapafter = gapafter
                        gapafter = 0
                    else:
                        gapafter += 1
                totalgapsbefore += max(maxgapbefore, gapbefore)
                if gapafter == 0 and maxgapafter == 0:
                    totalgapsafter += 10
                else:
                    totalgapsafter += max(maxgapafter, gapafter)
            for acol in xrange(piece.width):
                maxgapbefore = 0
                maxgapafter = 0
                gapbefore = 0
                gapafter = 0
                for arow in xrange(self.size):
                    if tmpboard[arow][col + acol] > 0:
                        if gapbefore > maxgapbefore:
                            maxgapbefore = gapbefore
                        gapbefore = 0
                    else:
                        gapbefore += 1
                    if tmpboard[arow][col + acol] != 0:
                        if gapafter > maxgapafter:
                            maxgapafter = gapafter
                        gapafter = 0
                    else:
                        gapafter += 1
                totalgapsbefore += max(maxgapbefore, gapbefore)
                if gapafter == 0 and maxgapafter == 0:
                    totalgapsafter += 10
                else:
                    totalgapsafter += max(maxgapafter, gapafter)
            result = totalgapsafter - totalgapsbefore
        return result

    def placepiece(self, piece, row, col):
        if self.isvalid(piece, row, col):
            for block in piece.blocks:
                self.board[row + block[0]][col + block[1]] = piece.color
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
                    result.append((row, col),)
        return result

    def validlocationssorted(self, piece):
        """generate a list of possible loactions for the piece"""
        result = []
        for col in xrange(11 - piece.width):
            for row in xrange(11 - piece.height):
                newscore = self.scorepiece(piece, row, col)
                if newscore > -100:
                    result.append((row, col, newscore),)
        result.sort(key=lambda tup: tup[2], reverse=True)
        return result

    def totalavailable(self):
        result = 0
        for piece in allPieces:
            available = self.validlocations(piece)
            result += len(available)
        return result

    def importantavailable(self):
        # scores 3x3, 5x1 and 1x5
        result = 0
        for i in [7, 8, 10]:
            piece = allPieces[i]
            available = self.validlocations(piece)
            result += len(available)
        return result

    def squaresavailable(self):
        # scores 1x1, 2x2 and 3x3
        result = 0
        for i in [0, 9, 10]:
            piece = allPieces[i]
            available = self.validlocations(piece)
            result += len(available)
        return result

    def maxgapperline(self):
        result = 0
        for row in xrange(self.size):
            maxgap = 0
            gap = 0
            for col in xrange(self.size):
                if self.board[row][col] > 0:
                    if gap > maxgap:
                        maxgap = gap
                    gap = 0
                else:
                    gap += 1
            result += max(maxgap, gap)
        for col in xrange(self.size):
            maxgap = 0
            gap = 0
            for row in xrange(self.size):
                if self.board[row][col] > 0:
                    if gap > maxgap:
                        maxgap = gap
                    gap = 0
                else:
                    gap += 1
            result += max(maxgap, gap)
        return result


class Piece:

    def __init__(self, blocks, frequency=5, color=5):
        self.blocks = blocks
        self.width = 1
        self.height = 1
        self.color = color
        self.frequency = frequency
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

allPieces = [Piece(((0, 0),), 5, 1),
             Piece(((0, 0), (1, 0)), 8, 2),
             Piece(((0, 0), (0, 1)), 8, 2),
             Piece(((0, 0), (1, 0), (2, 0)), 7, 3),
             Piece(((0, 0), (0, 1), (0, 2)), 7, 3),
             Piece(((0, 0), (1, 0), (2, 0), (3, 0)), 6, 4),  # 5
             Piece(((0, 0), (0, 1), (0, 2), (0, 3)), 6, 4),
             Piece(((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)), 5, 5),
             Piece(((0, 0), (0, 1), (0, 2), (0, 3), (0, 4)), 5, 5),
             Piece(((0, 0), (1, 0), (0, 1), (1, 1)), 15, 6),
             Piece(((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)), 5, 7),  # 10
             Piece(((1, 0), (0, 1), (1, 1)), 4, 8),
             Piece(((0, 0), (0, 1), (1, 1)), 4, 8),
             Piece(((0, 0), (1, 0), (1, 1)), 4, 8),
             Piece(((0, 0), (1, 0), (0, 1)), 4, 8),
             Piece(((0, 0), (1, 0), (2, 0), (0, 1), (0, 2)), 2, 9),  # 15
             Piece(((0, 0), (1, 0), (2, 0), (2, 1), (2, 2)), 2, 9),
             Piece(((0, 0), (0, 1), (0, 2), (1, 2), (2, 2)), 2, 9),
             Piece(((2, 0), (2, 1), (0, 2), (1, 2), (2, 2)), 2, 9),
             ]

piececolors = [(32, 32, 32), # Dark tile
               (50, 0, 255),
               (255, 200, 0),
               (226, 107, 10), 
               (204, 0, 100),
               (150, 50, 50),
               (50, 255, 0),
               (40, 164, 132),
               (0, 100, 0),
               (0, 148, 237),
              ]