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
        moves = plr.getmaxscoreturn(brd, (plr.getrandompiece(), plr.getrandompiece(), plr.getrandompiece()))
        if isinstance(moves, int):
            maxscore = max(maxscore, brd.score)
            print brd.score, turncount, int(time.time() - t0), maxscore
            # print brd.board
            brd = board.Board()
            turncount = 0
            t0 = time.time()
        else:
            turncount += 1
            # print turncount, brd.score
            brd.placepiece(moves[0][0], moves[1][0], moves[1][1])
            brd.placepiece(moves[0][1], moves[2][0], moves[2][1])
            brd.placepiece(moves[0][2], moves[3][0], moves[3][1])

if __name__ == '__main__':
    sys.exit(main())