import sys
import board
import time
import random

def main():
    """Main entry point for the script."""
    brd = board.Board()
    plr = board.Player()
    maxscore = 0
    turncount = 0
    t0 = time.time()
    while True:
        piece = plr.getrandompiece()
        position = plr.getmaxscore(brd, piece)
        if position[0] == -1:
            maxscore = max(maxscore, brd.score)
            print brd.score, turncount, time.time() - t0, maxscore
            # print brd.board
            brd = board.Board()
            turncount = 0
            t0 = time.time()
        else:
            turncount += 1
            brd.placepiece(piece, position[0], position[1])

if __name__ == '__main__':
    sys.exit(main())