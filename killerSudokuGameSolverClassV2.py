# -*- coding: utf-8 -*-
"""
 a killer sudoku game solver v2

"""
import time

import numpy

from filledKillerSudoku import killerSudoku
from killerSudokuGame import killerSudokuGame
import turtle
GRID_SIZE = 9

# UI object
turtle.colormode(255)
#turtle.delay(0) # if want to see the drawing procedure slower, comment this line
myPen = turtle.Turtle()
myPen.speed(0)
myPen.color((0, 0, 0)) #grid color = black
myPen.hideturtle()
#turtle.tracer(0, 0) # if want to see the drawing procedure, comment this line

# UI Constants
topLeft_x = -150
topLeft_y = 150
cellSize = 36

class killerSudokuGameSolverV2(killerSudokuGame):
    def __init__(self,seed=5, method='oc', maxCageSize=5, numAttempts=6,  visualization=True):
        super().__init__(seed=seed, method=method, maxCageSize=maxCageSize)
        self.color = {}
        self.visualization = visualization
        self.genGame(numAttempts=numAttempts)
        self.solGrid = self.getSolGrid()
        self.gameGrid = self.getGameGrid()
        self.gameCages = self.getGameCages()
        self.backupGrid = numpy.copy(self.gameGrid)
        self.render()

    def solve(self):
        self._start = time.time()
        if self.visualization:
            bgn_message = f'Start solving killer sudoku'
            self.text4timer(bgn_message, topLeft_x + 3 * cellSize,
                            topLeft_y - 10 * cellSize, 15, color='black')
        # first fill the cell who is in an one-cell-vide cage.
        for cageID in self.gameCages.keys():
            if cageID != None:
                num_blank_in_cage = 0
                index_blank = -1
                not_blank_sum = 0
                for index, cell in enumerate(self.gameCages[cageID][1]):
                    if self.gameGrid[cell[0], cell[1]] == 0:
                        num_blank_in_cage += 1
                        index_blank = index
                    else:
                        not_blank_sum += self.gameGrid[cell[0], cell[1]]
                if num_blank_in_cage == 1:
                    blank_row = self.gameCages[cageID][1][index_blank][0]
                    blank_col = self.gameCages[cageID][1][index_blank][1]
                    self.gameGrid[blank_row, blank_col] = self.gameCages[cageID][0] - not_blank_sum
                    self.text4solver(self.gameGrid[blank_row, blank_col], topLeft_x + blank_col * cellSize + 13,
                            topLeft_y - blank_row * cellSize - cellSize + 4.5, 18, color="red")
        self.solve_recursive()

    def solve_recursive(self):
        # Check if there are empty values, if not, then the game is solved
        emptyCell = self.empty(self.gameGrid)
        if not emptyCell:
            if not self.visualization:
                for row in range(GRID_SIZE):
                    for col in range(GRID_SIZE):
                        if self.backupGrid[row, col] == 0:
                            self.text4solver(self.gameGrid[row, col], topLeft_x + col * cellSize + 13,
                                            topLeft_y - row * cellSize - cellSize + 4.5, 18, color="red")
            if self.visualization:
                self.color4removetimer()
                self.elapsed_time = time.time() - self._start
                self.elapsed_time = '{:.2f}'.format(self.elapsed_time)
                fin_message = f'game is solved in: {self.elapsed_time}'
                self.text4timer(fin_message, topLeft_x + 3 * cellSize,
                                topLeft_y - 10 * cellSize, 15, color='black')
            else:
                print('solved')
                end = time.time()
                print('time for solving ' + str(round(end - self._start, 3)) + 's')
            turtle.getscreen()._root.mainloop()
            return True
        else:
            row, col = emptyCell

        for k in range(1, 10):

            if self.valid(self.gameGrid, self.gameCages, k, (row, col)):
                self.gameGrid[row][col] = k
                if self.visualization:
                    self.text4solver(self.gameGrid[row, col], topLeft_x + col * cellSize + 13,
                              topLeft_y - row * cellSize - cellSize + 4.5, 18, color="red")


                if self.solve_recursive():
                    return True

                self.gameGrid[row, col] = 0
                #remove the number in UI
                if self.visualization:
                    self.fillCellColor4solver(row, col, self.color[(row, col)])

        return False

    def valid(self, grid, cages, val, pos):
        # Check if valid in row
        if not self.validNum(grid, pos[0], pos[1], val):
            return False

        # Check if valid in cage
        cageID = self.getCageID(cages, pos)

        # Check that the value is not repeated within the cage
        for cell in cages[cageID][1]:
            if grid[cell[0], cell[1]] == val and cell != pos:
                return False

        # Check that the sum of the cage is respected
        valueList = self.getCurrentValues(grid, cages, cageID)

        count_0 = 0
        for num in valueList:
            if num == 0:
                count_0 += 1

        if count_0 == 1:
            if sum(valueList) + val != cages[cageID][0]:
                return False
        if count_0 > 1:
            if sum(valueList) + val > cages[cageID][0]:
                return False

        return True

    def getCurrentValues(self, grid, cages, cageID):
        cellList = cages[cageID][1]
        valueList = []
        for cell in cellList:
            valueList.append(grid[cell[0], cell[1]])

        return valueList

    def validNum(self, grid, row, col, n):
        if n not in self.getRow(grid, row):
            if n not in self.getCol(grid, col):
                if n not in self.getNonet(grid, (row, col)):
                    return True

    def getNonet(self, grid, coordinate):
        row = coordinate[0] // 3
        col = coordinate[1] // 3
        return grid[3 * row:3 * row + 3, 3 * col:3 * col + 3]

    def getRow(self, grid, idx):
        return grid[idx, :]

    def getCol(self, grid, idx):
        return grid[:, idx]

    def getCageID(self, dic, pos):
        for key, value in dic.items():
            cellList = value[1]
            for cell in cellList:
                if cell[0] == pos[0] and cell[1] == pos[1] :
                    return key

    def empty(self, grid):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if grid[row, col] == 0:
                    return (row, col)
        return None

    def render(self):
        grid = self.gameGrid
        cages = self.gameCages

        for row in range(0, 10):
            myPen.pensize(1)
            myPen.penup()  # Puts pen up for defaut turtle
            myPen.goto(topLeft_x, topLeft_y - row * cellSize)  # draw row from the topleft to the bottom
            myPen.pendown()  # begin to draw
            myPen.goto(topLeft_x + 9 * cellSize, topLeft_y - row * cellSize)  # draw the line till 9 cellsize long,
            # myPen.penup()

        for col in range(0, 10):
            myPen.pensize(1)
            myPen.penup()
            myPen.goto(topLeft_x + col * cellSize, topLeft_y)
            myPen.pendown()
            myPen.goto(topLeft_x + col * cellSize, topLeft_y - 9 * cellSize)
            # myPen.penup()

        for cage in list(cages.keys()):
            color = self.getRandomColor()
            for cell in cages[cage][1]:
                cellRow = cell[0]
                cellCol = cell[1]
                self.color[(cellRow, cellCol)] = color
                self.fillCellColor(cellRow, cellCol, color)

        for cageRowLine in range(0, 10):
            if (cageRowLine % 3) == 0:
                myPen.pensize(3)
                myPen.penup()
                myPen.goto(topLeft_x, topLeft_y - cageRowLine * cellSize)  # draw horizontal lines
                myPen.pendown()
                myPen.goto(topLeft_x + 9 * cellSize, topLeft_y - cageRowLine * cellSize)
                # myPen.penup()

        for cageColLine in range(0, 10):
            if (cageColLine % 3) == 0:
                myPen.pensize(3)
                myPen.penup()
                myPen.goto(topLeft_x + cageColLine * cellSize, topLeft_y)  # drawing vertical lines
                myPen.pendown()
                myPen.goto(topLeft_x + cageColLine * cellSize, topLeft_y - 9 * cellSize)
                # myPen.penup()

        for cage in list(cages.keys()):  # draw sum in the cage
            if cage != None:
                self.text(cages[cage][0],  # number - sum
                          topLeft_x + cages[cage][1][0][1] * cellSize + 3,  # place on x-axis to try,
                          topLeft_y - cages[cage][1][0][0] * cellSize - cellSize + 23,
                          # locate the bottom of number on this line, need to move down
                          7)  # size to try


        for row in range(GRID_SIZE): # draw cell values
            for col in range(GRID_SIZE):
                if grid[row, col] != 0:
                    self.text(grid[row, col], topLeft_x + col * cellSize + 13,
                         topLeft_y - row * cellSize - cellSize + 4.5, 18)

        #turtle.getscreen()._root.mainloop()

    def text4solver(self, message, x, y, size, color="black"):  # draw the sum on the top-left corner
        FONT = ('Arial', size, 'normal')
        myPen.penup()
        myPen.goto(x, y)
        myPen.color(color)
        myPen.write(message, align="left", font=FONT)

    def fillCellColor4solver(self, row, col, color):
        myPen.penup()
        myPen.goto(topLeft_x + col * cellSize+12, topLeft_y - row * cellSize-9)
        myPen.pensize(0.5)
        myPen.color(color)
        myPen.pendown()
        myPen.fillcolor(color)
        myPen.begin_fill()
        for side in range(4):
            myPen.forward(cellSize-20)
            myPen.right(90)
        myPen.end_fill()
        myPen.penup()

    def text4timer(self, message, x, y, size, color='black'):
        FONT = ('Arial', size, 'normal')
        myPen.penup()
        myPen.goto(x, y)
        myPen.color(color)
        myPen.write(message, align="left", font=FONT)

    def color4removetimer(self):
        myPen.penup()
        myPen.goto(topLeft_x + 3 * cellSize,
                   topLeft_y - 9.1 * cellSize)
        myPen.pensize(0.5)
        myPen.color('white')
        myPen.pendown()
        myPen.fillcolor('white')
        myPen.begin_fill()
        for side in range(4):
            myPen.forward(cellSize + 200)
            myPen.right(90)
        myPen.end_fill()
        myPen.penup()






