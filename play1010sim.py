import sys
import board
import random

def main():
    """Main entry point for the script."""
    brd = board.Board()
    plr = board.Player()
    while True:
        piece = random.choice(board.allPieces)
        position = plr.getmaxscore(brd, piece)
        print position, brd.score, piece.blocks
        if position[0] == -1:
            print brd.board
            break
        brd.placepiece(piece, position[0], position[1])

if __name__ == '__main__':
    sys.exit(main())