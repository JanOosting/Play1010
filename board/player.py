import layout
import random
import numpy
from copy import deepcopy


class Player:

    def __init__(self):
        self.piecefrequency = []
        for piece in xrange(len(layout.allPieces)):
            for i in xrange(layout.allPieces[piece].frequency):
                self.piecefrequency.append(piece)

    def testpiece(self, brd, piece, row, col):
        test_brd = deepcopy(brd)
        old_score = test_brd.score
        test_brd.placepiece(piece, row, col)
        return test_brd.score - old_score

    def totalavailable(self, brd):
        result = 0
        for piece in layout.allPieces:
            available = brd.validlocations(piece)
            result += len(available)
        return result

    def getmaxscore(self, brd, piece):
        allpossible = brd.validlocations(piece)
        result = (-1, -1)
        maxscore = 0
        boardscore = brd.score
        boardboard = numpy.copy(brd.board)
        for position in allpossible:
            brd.score = boardscore
            brd.board = numpy.copy(boardboard)
            brd.placepiece(piece, position[0], position[1])
            if self.totalavailable(brd) > maxscore:
                result = position
                maxscore = self.totalavailable(brd)
        brd.score = boardscore
        brd.board = numpy.copy(boardboard)
        return result

    def getrandompiece(self):
        return layout.allPieces[random.choice(self.piecefrequency)]
