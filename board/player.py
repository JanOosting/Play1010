import layout
import random
import numpy
from copy import deepcopy
from itertools import permutations


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

    def getmaxscore(self, brd, piece):
        allpossible = brd.validlocations(piece)
        result = (-1, -1)
        maxfitness = 0
        boardscore = brd.score
        boardboard = numpy.copy(brd.board)
        for position in allpossible:
            brd.score = boardscore
            brd.board = numpy.copy(boardboard)
            brd.placepiece(piece, position[0], position[1])
            fitness = brd.totalavailable()
            if fitness > maxfitness:
                result = position
                maxfitness = fitness
        brd.score = boardscore
        brd.board = numpy.copy(boardboard)
        return result

    def getmaxscoreturn(self, brd, pieces):
        perms = set(permutations(pieces))
        result = -1
        maxfitness = 0
        boardscore = brd.score
        boardboard = numpy.copy(brd.board)
        for perm_pieces in perms:
            brd.board = numpy.copy(boardboard)
            allpossiblefirst = brd.validlocationssorted(perm_pieces[0])
            if len(allpossiblefirst) > 10:
                allpossiblefirst = allpossiblefirst[:10]
            for first_pos in allpossiblefirst:
                brd.board = numpy.copy(boardboard)
                brd.placepiece(perm_pieces[0], first_pos[0], first_pos[1])
                allpossiblesecond = brd.validlocationssorted(perm_pieces[1])
                if len(allpossiblesecond) > 10:
                    allpossiblesecond = allpossiblesecond[:10]
                boardboard1 = numpy.copy(brd.board)
                for second_pos in allpossiblesecond:
                    brd.board = numpy.copy(boardboard1)
                    brd.placepiece(perm_pieces[1], second_pos[0], second_pos[1])
                    allpossiblethird = brd.validlocations(perm_pieces[2])
                    if len(allpossiblethird) > 10:
                        allpossiblethird = allpossiblethird[:10]
                    boardboard2 = numpy.copy(brd.board)
                    for third_pos in allpossiblethird:
                        brd.board = numpy.copy(boardboard2)
                        brd.placepiece(perm_pieces[2], third_pos[0], third_pos[1])
                        fitness = brd.maxgapperline()
                        if fitness > maxfitness:
                            result = [perm_pieces, first_pos, second_pos, third_pos]
                            maxfitness = fitness

        brd.score = boardscore
        brd.board = numpy.copy(boardboard)
        return result

    def getrandompiece(self):
        return layout.allPieces[random.choice(self.piecefrequency)]
