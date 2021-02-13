import numpy
import random
import turtle
from filledKillerSudoku import killerSudoku

# UI object
turtle.colormode(255)
myPen = turtle.Turtle()
myPen.speed(0)
myPen.color((0, 0, 0))  # grid color = black
myPen.hideturtle()

# UI Constants
topLeft_x = -150
topLeft_y = 150
cellSize = 36

# Create Grid
GRID_SIZE = 9
emptyGrid = numpy.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

filledGame = killerSudoku(GRID_SIZE=9, seed=5)
filledGame.populateGrid()
filledGame.genCages(method='oc', maxCageSize=5)
# filledGame.render()

generatedFilledGrid = filledGame.getGrid()
generatedGameCages = filledGame.getCages()

numSolutions = 0

############function to generate killer sudoku games##########################
#random.seed(5)


def genGame(filledGrid, gameCages, numAttempts):
    global numSolutions

    gameGrid = filledGrid
    attempts = numAttempts
    gameCage = gameCages
    cages_num = len(gameCage) - 1

    while attempts > 0:
        # Select a random cell that is not already empty
        # Select a random cell that is not already empty
        # Ouput total cage # (e.g. 15 cages in total),
        # While cage# > 0, loop into each cage
        # for each cage, eliminate only one cell, even if it can't be empty (some single cell might not be able to be empty, we try!!)
        # , go to next cage
        # loop until we finish all cages
        # jump into random delete if we have more attempts

        if cages_num >= 0:
            row = random.choice(gameCage[cages_num][1])[0]
            col = random.choice(gameCage[cages_num][1])[1]
        else:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        while gameGrid[row, col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        # Remember its cell value in case we need to put it back
        backup = gameGrid[row, col]
        gameGrid[row, col] = 0

        # Take a full copy of the grid
        copyGrid = numpy.copy(gameGrid)

        # Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)
        numSolutions = 0
        solveSudoku(copyGrid)
        # If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
        if numSolutions != 1:
            gameGrid[row, col] = backup
            # We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
            attempts -= 1

        if cages_num >= 0:
            if len(gameCage[cages_num][1]) > 1:
                if gameGrid[row, col] == backup:
                    pass
                else:
                    cages_num -= 1
            else:
                cages_num -= 1

    return gameGrid, gameCages


def solveSudoku(grid):
    global numSolutions
    # Find next empty cell
    for cell in range(GRID_SIZE * GRID_SIZE):
        row = cell // GRID_SIZE
        col = cell % GRID_SIZE
        if grid[row, col] == 0:
            for num in range(1, 10):
                # Check that this value has not already be used on this row
                if validNum(grid, row, col, num):
                    grid[row][col] = num
                    if fullGrid(grid):
                        numSolutions += 1
                        break
                    else:
                        if solveSudoku(grid):
                            return True
            break
    grid[row, col] = 0


# Helpper functions for solve function
def fullGrid(grid):
    for i in range(GRID_SIZE):
        row = getRow(grid, i)
        col = getCol(grid, i)
        if (0 in row) or (0 in col):
            return False
    return True


def validNum(grid, row, col, n):
    if n not in getRow(grid, row):
        if n not in getCol(grid, col):
            if n not in getNonet(grid, (row, col)):
                return True


def getNonet(grid, coordinate):
    row = coordinate[0] // 3
    col = coordinate[1] // 3
    return grid[3 * row:3 * row + 3, 3 * col:3 * col + 3]


def getRow(grid, idx):
    return grid[idx, :]


def getCol(grid, idx):
    return grid[:, idx]


# Game graphics
def render(grid, cages):
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
        color = getRandomColor()
        for cell in cages[cage][1]:
            cellRow = cell[0]
            cellCol = cell[1]
            fillCellColor(cellRow, cellCol, color)

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
        text(cages[cage][0],  # number - sum
             topLeft_x + cages[cage][1][0][1] * cellSize + 3,  # place on x-axis to try,
             topLeft_y - cages[cage][1][0][0] * cellSize - cellSize + 23,
             # locate the bottom of number on this line, need to move down
             7)  # size to try

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row, col] != 0:
                text(grid[row, col], topLeft_x + col * cellSize + 13,
                     topLeft_y - row * cellSize - cellSize + 4.5, 18)

    turtle.getscreen()._root.mainloop()


def getRandomColor():  # higher the first #, the lighter the color
    R = random.randrange(100, 256, 4)
    G = random.randrange(80, 256, 4)
    B = random.randrange(100, 256, 4)
    return (R, G, B)


def text(message, x, y, size):  # draw the sum on the top-left corner
    FONT = ('Arial', size, 'normal')
    myPen.penup()
    myPen.goto(x, y)
    myPen.write(message, align="left", font=FONT)


def fillCellColor(row, col, color):
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


##Generate Game

gameGrid, gameCages = genGame(filledGrid=generatedFilledGrid, gameCages=generatedGameCages, numAttempts=6)
render(gameGrid, gameCages)

print()


