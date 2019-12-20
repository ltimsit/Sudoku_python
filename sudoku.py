import numpy as np
import pygame as pg
from pygame.locals import *

class Grid():
    def __init__(self, smap):
        self.grid = [[None]*9, [None]*9, [None]*9, [None]*9, [None]*9,[None]*9,[None]*9,[None]*9,[None]*9]
        self.smap = smap
        self.myfont = pg.font.SysFont('Comic Sans MS', 30)
        self.initGrid()

        for row in self.grid:
            print(id(row))

    class Block():
        def __init__(self, rect, value, x, y, font, locked=False):
            
            self.rect = rect
            self.value = value        
            self.text = font.render(self.value, True, (255, 0, 0))
            # self.empty = font.render(' ', True, (255, 0, 0))
            self.font = font
            self.rectX = self.rect.x
            self.rectY = self.rect.y
            self.x = x
            self.y = y
            self.locked = locked

        def changeValue(self, value):
            self.value = value
            if self.locked:
                self.text = self.font.render(self.value, True, (255, 0, 0))
            else:
                self.text = self.font.render(self.value, True, (0, 255, 0))
                


    def initGrid(self):
        for row in range(9):
            for col in range(9):
                r  = pg.Rect(col * 50, row * 50, 50, 50)
                if self.smap[row, col] != 0:
                    self.grid[row][col] = self.Block(r, str(self.smap[row, col]), col, row, self.myfont, locked=True)
                else:
                    self.grid[row][col] = self.Block(r, '', col, row, self.myfont)
                

class Sudoku():

    def __init__(self, board):
        self.board = board

    def startGI(self):
        pg.init()
        # self.myfont = pg.font.SysFont('Comic Sans MS', 30)
        self.win = pg.display.set_mode((800, 800))
        self.win.fill(152)
        self.grid = Grid(self.board)
        self.inputActive = False
        self.inputValue = ''
        self.inputBlock = None
        self.eventListener()

    def drawGrid(self):
        for row in self.grid.grid:
            for block in row:
                pg.draw.rect(self.win, (100, 0, 66), block.rect, 3)
                if block.value != '':
                    # text = self.myfont.render(block.value, True, (255, 0, 0))
                    # self.win.blit(block.empty, (block.rectX + 18, block.rectY + 18))
                    self.win.blit(block.text, (block.rectX + 18, block.rectY + 18))


    def checkMousePos(self, event):
        check = False
        for row in self.grid.grid:
            for block in row:
                if block.rect.collidepoint(event.pos) and not block.locked:
                    print(block.rect.x, block.rect.y)
                    self.inputActive = True
                    check = True
                    self.inputBlock = block
        if not check:
            print('patate')
            self.inputActive = False
            self.inputBlock = None


    def eventListener(self):
        running = True
        while running:
            self.drawGrid()
            pg.display.update()
            self.win.fill((0, 0, 0))
            for event in pg.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    self.checkMousePos(event)
                if self.inputActive and event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        self.addInput()
                        self.inputValue = ''
                        self.inputActive = False
                    elif event.key == K_BACKSPACE:
                        self.inputValue = self.inputValue[:-1]
                    elif event.key == K_SPACE:
                        self.findSolution(0, 0)
                    else:
                        self.inputValue = event.unicode
                        print(self.inputValue)

    def addInput(self):
        x = self.inputBlock.x
        y = self.inputBlock.y
        self.grid.grid[y][x].changeValue(self.inputValue)

    def loopInAlg(self, x, y, val):
        running = True
        self.grid.grid[y][x].changeValue(str(val))
        MYEVENT = USEREVENT + 1
        pg.time.set_timer(MYEVENT, 50)
        # print('test')
        while running:
            self.drawGrid()
            pg.display.update()
            self.win.fill((0, 0, 0))
            for event in pg.event.get():
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False
                    exit()
                if event.type == MYEVENT:
                    return

    def findSolution(self, x, y):
        val = self.evaluatePossibleValue((y, x))
        if self.board[y, x] != 0:
            if y != 8 and x == 8:
                return self.findSolution(0, y + 1)
            elif x == 8 and y == 8:
                return 1
            else:
                return self.findSolution(x + 1, y)
        for elem in val:
            self.board[y, x] = elem
            self.loopInAlg(x, y, elem)
            if x == 8:
                if y == 8:
                    return 1
                elif self.findSolution(0, y + 1):
                    return 1
            elif self.findSolution(x+1, y):
                return 1
        self.board[y, x] = 0
        return 0

    def printBoard(self):
        print(self.board)

    def evaluatePossibleValue(self, position):
        sol = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # global it
        # it += 1
        for elem in self.board[position[0], :]:
            if int(elem) != 0 and elem in sol:
                sol.remove(elem)
        for elem in self.board[:, position[1]]:
            if elem != 0 and elem in sol:
                sol.remove(elem)
        mini = self.board[position[0]//3*3:position[0]//3*3+3, position[1]//3*3:position[1]//3*3+3]
        for elem in mini:
            for xelem in elem:
                if xelem != 0 and xelem in sol:
                    sol.remove(xelem)
        return sol



if __name__ == '__main__':

    A1,A2,A3,A4,A5,A6,A7,A8,A9 = 9,0,7,0,1,0,0,4,0
    B1,B2,B3,B4,B5,B6,B7,B8,B9 = 0,8,2,0,0,4,0,0,7
    C1,C2,C3,C4,C5,C6,C7,C8,C9 = 1,4,0,7,3,0,0,0,0
    D1,D2,D3,D4,D5,D6,D7,D8,D9 = 0,0,0,4,0,7,0,0,3
    E1,E2,E3,E4,E5,E6,E7,E8,E9 = 0,7,0,0,0,0,0,2,0
    F1,F2,F3,F4,F5,F6,F7,F8,F9 = 2,0,0,5,0,9,0,0,0
    G1,G2,G3,G4,G5,G6,G7,G8,G9 = 0,0,0,0,4,3,0,9,8
    H1,H2,H3,H4,H5,H6,H7,H8,H9 = 7,0,0,6,0,0,1,3,0
    I1,I2,I3,I4,I5,I6,I7,I8,I9 = 0,9,0,0,7,0,6,0,2

    board = np.array([[A1,A2,A3,A4,A5,A6,A7,A8,A9],
				 [B1,B2,B3,B4,B5,B6,B7,B8,B9],
				 [C1,C2,C3,C4,C5,C6,C7,C8,C9],
				 [D1,D2,D3,D4,D5,D6,D7,D8,D9],
				 [E1,E2,E3,E4,E5,E6,E7,E8,E9],
				 [F1,F2,F3,F4,F5,F6,F7,F8,F9],
				 [G1,G2,G3,G4,G5,G6,G7,G8,G9],
				 [H1,H2,H3,H4,H5,H6,H7,H8,H9],
				 [I1,I2,I3,I4,I5,I6,I7,I8,I9]])


    it = 0
    # board = np.zeros((9, 9), dtype=int)
    sudoku = Sudoku(board)
    # sudoku.findSolution(0, 0)
    # sudoku.printBoard()
    sudoku.startGI()