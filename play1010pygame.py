import os, sys
import pygame
import board
import time

def drawboard(screen, brd, turncount, maxscore, pieces = None):
    black = 0, 0, 0
    dark = 32, 32, 32
    tilecolor = 192, 192, 192
    font = pygame.font.Font(None, 35)
    screen.fill(black)
    for row in xrange(brd.size):
        for col in xrange(brd.size):
            pygame.draw.rect(screen, board.piececolors[brd.board[row][col]], (200 + col * 60, row * 60, 55, 55))
    score_text = font.render(str(brd.score), True, tilecolor)
    screen.blit(score_text, (10, 50))
    score_text = font.render(str(turncount), True, tilecolor)
    screen.blit(score_text, (10, 100))
    score_text = font.render(str(maxscore), True, tilecolor)
    screen.blit(score_text, (10, 150))
    if pieces != None:
        for index, piece in enumerate(pieces):
            color = board.piececolors[piece.color]
            for block in piece.blocks:
                pygame.draw.rect(screen, color, (200 + index * 200 + block[1] *30 , 620 + block[0] * 30, 27, 27))


    pygame.display.flip()


def main():
    pygame.init()

    size = width, height = 1024, 768
    screen = pygame.display.set_mode(size)

    brd = board.Board()
    plr = board.Player()
    maxscore = 0
    sleeptime = 0.05
    turncount = 0
    t0 = time.time()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    sleeptime = 1.1 - sleeptime
        pieces = (plr.getrandompiece(), plr.getrandompiece(), plr.getrandompiece())
        drawboard(screen, brd, turncount, maxscore, pieces)
        moves = plr.getmaxscoreturn(brd, pieces)
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
            drawboard(screen, brd, turncount, maxscore, pieces)
            time.sleep(sleeptime)
            brd.placepiece(moves[0][1], moves[2][0], moves[2][1])
            drawboard(screen, brd, turncount, maxscore, pieces)
            time.sleep(sleeptime)
            brd.placepiece(moves[0][2], moves[3][0], moves[3][1])
            drawboard(screen, brd, turncount, maxscore, pieces)
            time.sleep(sleeptime)



if __name__ == '__main__': main()