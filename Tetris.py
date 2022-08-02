#################################################
# hw6.py
#
# Your name: Ryan Duan, recitation N
# Your andrew id: ryanduan
#
# Your partner's name: Jacob Morin
# Your partner's andrew id: jmorin
#################################################

from ssl import ALERT_DESCRIPTION_CERTIFICATE_UNKNOWN
import cs112_s22_week6_linter
import math, copy, random

from cmu_112_graphics import *

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#################################################
# Functions for you to write
#################################################

# Helper function to determine whether number is a square
def isPerfectSquare(n):
    for i in range(n):
        if i ** 2 == n:
            return True
    return False

# Helper funciton to check whether number is sortofsquarish
def isSortOfSquarish(n):
    # Check bounds
    if n <= 0:
        return False
    if isPerfectSquare(n):
        return False
    numbers = n
    # Establish list of numbers
    listOfNumbers = []
    # Add numbers to list
    while numbers > 0:
        listOfNumbers = listOfNumbers + [numbers % 10]
        numbers = numbers // 10
    # Check for zeroes
    if listOfNumbers.count(0) > 0:
        return False
    # Sort and reverse the list to make it easy to add togethehr
    listOfNumbers.sort()
    listOfNumbers.reverse()
    number = 0
    # Construct the sorted number
    for i in range(len(listOfNumbers)):
        number = number + listOfNumbers[i] * (10 ** i)
    # Check if the sorted number is sortofsquarish
    if isPerfectSquare(number):
        return True
    return False

def nthSortOfSquarish(n):
    # Establish counters for the nth number count and the number itself
    nthNumber = 0
    # Start at -1 to account for the zeroth number
    count = -1
    # Use the nth number n as loop guard
    while count < n:
        if isSortOfSquarish(nthNumber):
            nthNumber = nthNumber + 1
            count = count + 1
        else:
            nthNumber = nthNumber + 1
    # Take nthNumber - 1 to get the accurate number
    return nthNumber - 1

#################################################
# s21-midterm1-animation
#################################################

def s21MidtermAnimation_appStarted(app):
    # List of coordinates of center of circles 
    app.circles = []
    app.radius = 20
    # Delay is 5 seconds
    app.timerDelay = 1000
    app.counter = 0
def s21MidtermAnimation_mousePressed(app, event):
    # Set parameters of circles when the mouse is pressed
    app.circles.append((event.x, event.y))
    
def s21MidtermAnimation_keyPressed(app, event):
    # Set parameters of reset when r is pressed
    if event.key == "r":
        app.circles = []
        app.counter = 0

def s21MidtermAnimation_timerFired(app):
    # Clear list and set counter to 0 every 5 seconds
    app.counter = app.counter + 1
    if app.counter % 5 == 0:
        app.circles = []

def findDistance(CX, CY, newx, newy):
    return (((CX - newx) ** 2) + ((CY - newy) ** 2)) ** 0.5

def findClosestCircleCenter(app, CX, CY):
    # 2 Circles Required to Draw a Line Between Them
    if len(app.circles) < 2:
        return None
    # Counter interations
    counter = 0
    closestPointX, closestPointY = None, None
    for i in range(len(app.circles)):
        # Find center of Circle
        x, y= app.circles[i][0], app.circles[i][1]
        if (x,y) != (CX, CY):
            # Find distance
            currentDistance = findDistance(x, y, CX, CY)
            # First center is the closest for now
            if counter < 1:
                closestPointX, closestPointY = x, y
                closestDistance = currentDistance
                # Iterate through only once
                counter = counter + 1
            # Replace closest point if current distance is smaller
            if currentDistance < closestDistance:
                closestDistance = currentDistance
                closestPointX, closestPointY = x, y
    # Check for same center
    if closestPointX != None:
        return closestPointX, closestPointY
    else: 
        return None
def s21MidtermAnimation_redrawAll(app, canvas):
    for cx, cy in app.circles:
        # draw the circle
        canvas.create_oval(cx-app.radius, cy-app.radius, cx+app.radius, 
                    cy+app.radius, fill = "green")
        # if there's another circle, draw a line to the closest one
        if findClosestCircleCenter(app, cx, cy) != None:
            closestPointX, closestPointY = findClosestCircleCenter(app, cx, cy)
            canvas.create_line(cx, cy, closestPointX, closestPointY, 
                            fill = "black", width = 5)


def s21Midterm1Animation():
    runApp(width=400, height=400, fnPrefix='s21MidtermAnimation_') 

#################################################
# Tetris
#################################################

# Print 2D list, https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
def repr2dList(L):
    if (L == []): return '[]'
    output = [ ]
    rows = len(L)
    cols = max([len(L[row]) for row in range(rows)])
    M = [['']*cols for row in range(rows)]
    for row in range(rows):
        for col in range(len(L[row])):
            M[row][col] = repr(L[row][col])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(M[row][col]) for row in range(rows)])
    output.append('[\n')
    for row in range(rows):
        output.append(' [ ')
        for col in range(cols):
            if (col > 0):
                output.append(', ' if col < len(L[row]) else '  ')
            output.append(M[row][col].rjust(colWidths[col]))
        output.append((' ],' if row < rows-1 else ' ]') + '\n')
    output.append(']')
    return ''.join(output)

# Helper function to print more easily 
def Print(x):
    print(repr2dList(x))

# Starts function
def appStarted(app):
    # Set some important variables
    app.timerDelay = 1000
    app.paused = False
    app.isGameOver = False
    app.score = 0
    # Set parameters
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.emptyColor = "blue"
    # Change board, delete later
    app.board = [[app.emptyColor] * app.cols for row in range(app.rows)]
    # List of blocks
    iPiece = [
        [  True,  True,  True,  True ]
    ]
    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    # List of tetris pieces and colors
    app.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, 
                            tPiece, zPiece]
    app.tetrisPieceColors = [ "red", "yellow", "magenta", 
                                "pink", "cyan", "green", "orange" ]
    # Falling pieces properties
    app.fallingPiece = None
    app.fallingPieceColor = None
    app.fallingPieceStartRow = None
    app.fallingPieceStartCol = None
    newFallingPiece(app)
    timerFired(app)

# Define game dimensions
def gameDimensions():
    rows = 15
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

# Draw each cell
def drawCell(app, canvas, row, column, color):
    # Get points
    x0 = app.margin + column * app.cellSize   
    y0 = app.margin + row * app.cellSize
    x1 = app.margin + (column+ 1) * app.cellSize
    y1 = app.margin + (row + 1) * app.cellSize
    # Draw rectangle
    canvas.create_rectangle(x0, y0, x1, y1, fill = color)

def drawBoard(app, canvas):
    # Assign variables
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    # Loop through to draw every cell, and board
    for r in range(app.rows):
        for c in range(app.cols):     
            color = app.board[r][c]     
            drawCell(app, canvas, r, c, color)
            
# Randomize starting index
def newFallingPiece(app):
    # Change variables accordingly
    app.fallingPieceStartingI = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[app.fallingPieceStartingI]
    app.fallingPieceColor = app.tetrisPieceColors[app.fallingPieceStartingI]
    # Add drow so have to start at -1
    app.fallingPieceStartRow = 0
    app.fallingPieceStartCol = app.cols // 2 - (len(app.fallingPiece[0])) //2

# Draw the falling piece
def drawFallingPiece(app, canvas):
    for cord in range(len(app.fallingPiece)):
        for cord2 in range(len(app.fallingPiece[0])):
            # Take coordinates and draw square in every 'True' item
            if app.fallingPiece[cord][cord2] == True:
                drawCell(app, canvas, app.fallingPieceStartRow + cord, 
                            app.fallingPieceStartCol + cord2,
                            app.fallingPieceColor)

def moveFallingPiece(app, drow, dcol):    
    # Moves piece once
    app.fallingPieceStartRow = app.fallingPieceStartRow + drow
    app.fallingPieceStartCol = app.fallingPieceStartCol + dcol
    # Move back if touching border or another piece
    if fallingPiecesLegal(app) == False:
        app.fallingPieceStartRow = app.fallingPieceStartRow - drow
        app.fallingPieceStartCol = app.fallingPieceStartCol - dcol  
        return False
    # Check if row has changed
    return True

def fallingPiecesLegal(app):
    # check each item in app 
    rows = len(app.fallingPiece)
    cols = len(app.fallingPiece[0])
    for row in range(rows):
        for col in range(cols):
            # Check each actual piece of the whole piece
            if app.fallingPiece[row][col] == True:
                coord1 = app.fallingPieceStartCol + col
                coord2 = app.fallingPieceStartRow + row
                # Check for bounds and touching other pieces
                if (coord1 < 0 or coord1 >= app.cols or
                    coord2 < 0 or coord2 >= app.rows or 
                    app.board[coord2][coord1] != app.emptyColor):
                    return False
    return True

def rotateFallingPiece(app):
    # Use temporary copy
    oldPiece = app.fallingPiece
    oldStartRow = app.fallingPieceStartRow
    oldStartCol = app.fallingPieceStartCol
    app.fallingPiece = rotatePiece(oldPiece)
    # Find center to rotate around
    oldCenterRow = oldStartRow + len(oldPiece)//2
    oldCenterCol = oldStartCol + len(oldPiece[0])//2
    # Find new centers
    newStartRow =  oldCenterRow - len(app.fallingPiece)//2
    newStartCol =  oldCenterCol - len(app.fallingPiece[0])//2
    # Find new starting point
    app.fallingPieceStartRow = newStartRow
    app.fallingPieceStartCol = newStartCol
    # Check if movement valid
    if fallingPiecesLegal(app) == False:
        # Reset piece
        app.fallingPiece = oldPiece
        app.fallingPieceStartRow = oldStartRow
        app.fallingPieceStartCol = oldStartCol

def rotatePiece(L):
    # Create variables
    oldRows = len(L)
    oldCols = len(L[0])
    newRows = oldCols
    newCols = oldRows
    # Flip the list
    flipList = flipColumns(L)
    # Create a counterclockwise list
    counterClockwiseList = [[None]*newCols for row in range(newRows)]
    # Loop through and add the right values
    for r in range(oldRows):
        for c in range(oldCols):
            counterClockwiseList[c][r] = flipList[r][c]
    return counterClockwiseList

def flipColumns(L):
    # Flips columns to counterclockwise list
    rows = len(L)
    cols = len(L[0])
    newList = [[None] * cols for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            # keeps row the same
            newList[row][cols - col - 1] = L[row][col]
    return newList

def placeFallingPiece(app):
    # Get the rows and starting
    totalRows = len(app.fallingPiece)
    totalCols = len(app.fallingPiece[0])
    startRow = app.fallingPieceStartRow
    startCol = app.fallingPieceStartCol
    # Change colors of board accordingly
    for row in range(totalRows):
        for col in range(totalCols):
            if app.fallingPiece[row][col] == True:
                app.board[row + startRow][col + startCol]=app.fallingPieceColor
    removeFullRows(app)

# Remove full rows
def removeFullRows(app):
    # Create a newboard
    newBoard = [[app.emptyColor] * app.cols for row in range(app.rows)]
    counter = 0
    score = 0
    # Count the score and change the full row to all blue
    for row in app.board:
        if row.count("blue") == 0:
            score = score + 1
            row = ["blue"] * len(row)
        newBoard[counter] = row
        counter = counter + 1
    # Add the proper score
    app.score = app.score + score ** 2
    count = 0
    # Remove all blue rows
    while count < len(newBoard):
        if newBoard[count].count("blue") == len(newBoard[0]):
            newBoard.remove(newBoard[count])
        else:
            count = count + 1
    # Add blue rows until the board is full again
    while len(newBoard) < len(app.board):
        newBoard = [[app.emptyColor] * len(app.board[0])] + newBoard
    # Reassign variables
    app.board = newBoard

# Hard drop
def hardDrop(app):
    for r in range(1, app.rows):
        # Checks if move is valid
        if (moveFallingPiece(app, r, 0) == True):
            moveFallingPiece(app, -r, 0)
        # Moves to the right place
        elif (moveFallingPiece(app, r, 0) == False):
            moveFallingPiece(app, r-1, 0)
            break
    doStep(app)

# Do the step
def doStep(app):
    if moveFallingPiece(app, 1, 0) == False:
        placeFallingPiece(app)
        # Check if the game should end
        if app.fallingPieceStartRow < 1:
            app.isGameOver = True
            return
        # Another check just in case
        newFallingPiece(app)
        if fallingPiecesLegal(app) == False:
            app.isGameOver = True

def keyPressed(app, event):
    if app.isGameOver == False:
        # Pause button
        # Left
        if event.key == "Left":
            moveFallingPiece(app, 0, -1)
        # Right
        elif event.key == "Right":
            moveFallingPiece(app, 0, 1)
        # Down
        elif event.key == "Down":
            moveFallingPiece(app, 1, 0)
        # Rotate
        elif event.key == "Up":
            rotateFallingPiece(app)
        #
        elif event.key == "Space":
            hardDrop(app)
        # Pause
        if event.key == "p":
            app.paused = not app.paused
        # Do step
        elif event.key == "s" and app.paused:
                doStep(app)
        # Restart
        elif event.key == "r":
            appStarted(app)
    # Restart out of loop
    elif event.key == "r":
        appStarted(app)

def timerFired(app):
    # Pause
    if (not app.paused) and app.isGameOver == False:
        doStep(app)

# Redrawall
def redrawAll(app, canvas):
    # Draw the board
    if app.isGameOver == False:
        canvas.create_rectangle(0,0, app.width, app.height, fill = "orange")
        drawBoard(app, canvas)
        drawFallingPiece(app, canvas)
        canvas.create_text(app.width // 2, app.margin // 2, 
                        text = f"Score: {app.score}", fill = "black")
    # Draw the moving
    else:
        canvas.create_text(app.width // 2, app.height // 2, 
                            text = f"GAME OVER \n Score: {app.score}", 
                            font='Arial 30 bold', 
                            fill = "black")

def playTetris():
    # Play Tetris with proper dimensions
    runApp(width = 2 * gameDimensions()[3] + 
                    gameDimensions()[1] * gameDimensions()[2], 
           height = 2 * gameDimensions()[3] + 
                    gameDimensions()[0] * gameDimensions()[2])

#################################################
# Test Functions
#################################################

def testIsPerfectSquare():
    print('Testing isPerfectSquare(n))...', end='')
    assert(isPerfectSquare(4) == True)
    assert(isPerfectSquare(9) == True)
    assert(isPerfectSquare(10) == False)
    assert(isPerfectSquare(225) == True)
    assert(isPerfectSquare(1225) == True)
    assert(isPerfectSquare(1226) == False)
    print('Passed')


def testIsSortOfSquarish():
    print('Testing isSortOfSquarish(n))...', end='')
    assert(isSortOfSquarish(52) == True)
    assert(isSortOfSquarish(16) == False)
    assert(isSortOfSquarish(502) == False)
    assert(isSortOfSquarish(414) == True)
    assert(isSortOfSquarish(5221) == True)
    assert(isSortOfSquarish(6221) == False)
    assert(isSortOfSquarish(-52) == False)
    print('Passed')


def testNthSortOfSquarish():
    print('Testing nthSortOfSquarish()...', end='')
    assert(nthSortOfSquarish(0) == 52)
    assert(nthSortOfSquarish(1) == 61)
    assert(nthSortOfSquarish(2) == 63)
    assert(nthSortOfSquarish(3) == 94)
    assert(nthSortOfSquarish(4) == 252)
    assert(nthSortOfSquarish(8) == 522)
    print('Passed')

def testAll():
    testIsPerfectSquare()
    testIsSortOfSquarish()
    testNthSortOfSquarish()
#################################################
# main
#################################################

def main():
    cs112_s22_week6_linter.lint()
    testAll()
    s21Midterm1Animation()
    playTetris()

if __name__ == '__main__':
    main()
