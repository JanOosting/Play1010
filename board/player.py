import layout
from copy import deepcopy

class Player:

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
        for position in allpossible:
            test_brd = deepcopy(brd)
            test_brd.placepiece(piece, position[0], position[1])
            if self.totalavailable(test_brd) > maxscore:
                result = position
                maxscore = self.totalavailable(test_brd)
        return result


