# -*- coding: utf-8 -*-

import turtle
import numpy
import time
import random
from collections import defaultdict
import abc

# UI object
turtle.colormode(255)
#turtle.delay(0) # if want to see the drawing procedure slower, comment this line
myPen = turtle.Turtle()
myPen.speed(0)

myPen.color((0, 0, 0)) #grid color = black
myPen.hideturtle()

# Global Constant
MIN_NUM = 1
MAX_NUM = 9
INT_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9]
TRANS_PROB = 0.3

# UI Constants
topLeft_x = -150
topLeft_y = 150
cellSize = 36

# Create Grid



class visualizeOrderedCage:

    def __init__(self, GRID_SIZE=9, seed=5):
        self.GRID_SIZE = GRID_SIZE
        self.__grid = numpy.zeros((self.GRID_SIZE, self.GRID_SIZE), dtype=int)

        random.seed(seed)
        numpy.random.seed(seed) #set up random seed

        self.__cages = defaultdict(lambda: [0, []])
        self._cage_color = {}


    def populateGrid(self):

        for cell in range(self.GRID_SIZE * self.GRID_SIZE):
            row = cell // self.GRID_SIZE
            col = cell % self.GRID_SIZE
            # print(cell)
            if self.__grid[row, col] == 0:
                values = INT_LIST
                random.shuffle(values)
                for num in values:
                    if self.validNum(row, col, num):
                        self.__grid[row, col] = num
                        if self.fullGrid():
                            return True
                        elif self.populateGrid():
                            return True
                break
        self.__grid[row, col] = 0

    def validNum(self, row, col, n):
        if n not in self.getRow(row):
            if n not in self.getCol(col):
                if n not in self.getNonet((row, col)):
                    return True

        return False

    def fullGrid(self):
        for i in range(self.GRID_SIZE):
            row = self.getRow(i)
            col = self.getCol(i)
            if (0 in row) or (0 in col):
                return False
        return True

    def getNonet(self, coordinate):
        row = coordinate[0] // 3
        col = coordinate[1] // 3
        return self.__grid[3 * row:3 * row + 3, 3 * col:3 * col + 3]

    def getRow(self, idx):
        return self.__grid[idx, :]

    def getCol(self, idx):
        return self.__grid[:, idx]

    # Generate Cages
    def genCages(self, method='oc', maxCageSize=5):
        if method == 'rw':
            raise AttributeError('This class only allow Ordered Cage')

        elif method == 'oc':
            randValue = numpy.random.uniform(0, 1, 100)

            # cages = defaultdict(lambda: [0, []])
            cageID = 0

            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):

                    # First cell
                    if row == 0 and col == 0:
                        self.__cages[cageID][1].append((row, col))
                        self.__cages[cageID][0] += self.__grid[row, col]

                    # Identify adjacent cages and their sizes
                    if col > 0:
                        leftCage = self.getCageID(self.__cages, (row, col - 1))
                        leftCageSize = self.getSize(self.__cages, leftCage)
                        leftCageValues = [self.__grid[cell[0], cell[1]] for cell in self.__cages[leftCage][1]]

                    if row > 0:
                        aboveCage = self.getCageID(self.__cages, (row - 1, col))
                        aboveCageSize = self.getSize(self.__cages, aboveCage)
                        aboveCageValues = [self.__grid[cell[0], cell[1]] for cell in self.__cages[aboveCage][1]]

                    # Only consider cells to the left of first row
                    if row == 0 and col > 0:
                        rand = random.choice(randValue)
                        if leftCageSize < maxCageSize and rand >= TRANS_PROB:
                            self.__cages[cageID][1].append((row, col))
                            self.__cages[cageID][0] += self.__grid[row, col]
                        else:
                            cageID += 1
                            self.__cages[cageID][1].append((row, col))
                            self.__cages[cageID][0] += self.__grid[row, col]

                    # Only consider cells above (no cells to the left)
                    if row > 0 and col == 0:
                        rand = random.choice(randValue)
                        if aboveCageSize < maxCageSize and rand >= TRANS_PROB and self.__grid[row, col] not in aboveCageValues:
                            self.__cages[aboveCage][1].append((row, col))
                            self.__cages[aboveCage][0] += self.__grid[row, col]
                        else:
                            cageID += 1
                            self.__cages[cageID][1].append((row, col))
                            self.__cages[cageID][0] += self.__grid[row, col]

                    # Consider cells to the left and above
                    if row > 0 and col > 0:
                        rand = random.choice(randValue)
                        if rand >= TRANS_PROB * 2 and aboveCageSize < maxCageSize and self.__grid[row][col] not in aboveCageValues:
                            self.__cages[aboveCage][1].append((row, col))
                            self.__cages[aboveCage][0] += self.__grid[row, col]

                        elif rand >= TRANS_PROB and leftCageSize < maxCageSize and self.__grid[row][col] not in leftCageValues:
                            self.__cages[leftCage][1].append((row, col))
                            self.__cages[leftCage][0] += self.__grid[row, col]

                        else:
                            cageID += 1
                            self.__cages[cageID][1].append((row, col))
                            self.__cages[cageID][0] += self.__grid[row, col]

            for cage in list(self.__cages.keys()):
                self.__cages[cage] = tuple(self.__cages[cage])
            return print('Killer sudoku has been generated')

        else:
            raise AttributeError('The input method not found')



    def getGrid(self):
        return self.__grid

    def getCages(self):
        return self.__cages

    def getCageID(self, dic, pos):
        for key, value in dic.items():
            cellList = value[1]
            for cell in cellList:
                if cell == pos:
                    return key

                    # Function to get size of the cage

    def getSize(self, dic, cageID):
        size = len(dic[cageID][1])
        return size

    # UI methods
    def render(self):

        for row in range(0, 10):
            myPen.pensize(1)
            myPen.penup() # Puts pen up for defaut turtle
            myPen.goto(topLeft_x, topLeft_y - row * cellSize) # draw row from the topleft to the bottom
            myPen.pendown() #begin to draw
            myPen.goto(topLeft_x + 9 * cellSize, topLeft_y - row * cellSize) #draw the line till 9 cellsize long,
            #myPen.penup()

        for col in range(0, 10):
            myPen.pensize(1)
            myPen.penup()
            myPen.goto(topLeft_x + col * cellSize, topLeft_y)
            myPen.pendown()
            myPen.goto(topLeft_x + col * cellSize, topLeft_y - 9 * cellSize)
            #myPen.penup()

        for cage in list(self.__cages.keys()):
            color = self.getRandomColor()
            self._cage_color[cage] = color



        for cageRowLine in range(0, 10):
            if (cageRowLine % 3) == 0:
                myPen.pensize(3)
                myPen.penup()
                myPen.goto(topLeft_x, topLeft_y - cageRowLine * cellSize) #draw horizontal lines
                myPen.pendown()
                myPen.goto(topLeft_x + 9 * cellSize, topLeft_y - cageRowLine * cellSize)
                #myPen.penup()

        for cageColLine in range(0, 10):
            if (cageColLine % 3) == 0:
                myPen.pensize(3)
                myPen.penup()
                myPen.goto(topLeft_x + cageColLine * cellSize, topLeft_y)  #drawing vertical lines
                myPen.pendown()
                myPen.goto(topLeft_x + cageColLine * cellSize, topLeft_y - 9 * cellSize)
                #myPen.penup()



        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                if self.__grid[row, col] != 0:
                    self.text(self.__grid[row, col], topLeft_x + col * cellSize + 13,
                              topLeft_y - row * cellSize - cellSize + 4.5, 18)

        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                cageId = self.getCageID(self.__cages,(row, col))
                self.fillCellColor(row=row, col=col, color=self._cage_color[cageId])
                self.text(self.__grid[row, col], topLeft_x + col * cellSize + 13,
                          topLeft_y - row * cellSize - cellSize + 4.5, 18)

        for cage in list(self.__cages.keys()):  #draw sum in the cage
            self.text(self.__cages[cage][0],  #number - sum
                      topLeft_x + self.__cages[cage][1][0][1] * cellSize + 3,  # place on x-axis to try,
                      topLeft_y - self.__cages[cage][1][0][0] * cellSize - cellSize + 23,  #locate the bottom of number on this line, need to move down
                      7)  # size to try

        turtle.getscreen()._root.mainloop()

    def getRandomColor(self): #higher the first #, the lighter the color
        R = random.randrange(100, 256, 4)
        G = random.randrange(80, 256, 4)
        B = random.randrange(100, 256, 4)
        return (R, G, B)

    def text(self, message, x, y, size):  #draw the sum on the top-left corner
        FONT = ('Arial', size, 'normal')
        myPen.penup()
        myPen.goto(x, y)
        myPen.write(message, align="left", font=FONT)

    def fillCellColor(self, row, col, color):
        myPen.penup()
        myPen.goto(topLeft_x + col * cellSize, topLeft_y - row * cellSize)
        myPen.pensize(0.5)
        myPen.pendown()
        myPen.fillcolor(color)
        myPen.begin_fill()
        for side in range(4):
            myPen.forward(cellSize)
            myPen.right(90)
        myPen.end_fill()
        myPen.penup()

'''
KS1 = KillerSudoku(Grid, 5)
KS1.populateGrid()

KS1.genCages(method='oc', maxCageSize=5)

print(KS1.getCages())
print(KS1.getGrid())
KS1.render()
'''
'''
KS1 = killerSudoku(GRID_SIZE=9,seed=5)
KS1.populateGrid()

KS1.genCages(method='oc', maxCageSize=5)
print(KS1.getCages())
print(len(KS1.getCages()))
t = KS1.getCages()
print(random.choice(t[len(KS1.getCages())-1][1]))
'''


