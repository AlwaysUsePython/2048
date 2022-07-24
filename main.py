import random

def placeRandomTile(board):
    newBoard = [["", "", "", ""],
                ["", "", "", ""],
                ["", "", "", ""],
                ["", "", "", ""]]

    for r in range(4):
        for c in range(4):
            newBoard[r][c] = board[r][c]

    emptySpaces = []

    for row in range(4):
        for col in range(4):
            if board[row][col] == " ":
                emptySpaces.append([row, col])

    chosenSpace = random.randint(0, len(emptySpaces)-1)

    chosenValue = random.randint(1, 10)
    if chosenValue == 1:
        value = "4"
    else:
        value = "2"

    newBoard[emptySpaces[chosenSpace][0]][emptySpaces[chosenSpace][1]] = value

    return newBoard



# This is fundamentally our usual printboard, but we have to do a few things for spacing
# ideally, we don't want the grid size to change based on whether we have a 2
# or a 2048 in a slot, so we instead have to use the %d stuff to always format it as a
# 4 digit number.

# Will this cause problems if we get to 2^14? yes. but I'm not too worried about that
def printBoard(board):
    for row in board:
        for col in row:
            if col == " ":
                print("____", end = " ")
            else:
                print("%4d" %int(col), end = " ")
        print()
    print()



# There's a bunch of stuff for the shift functions
# Here's how it's organized:

# 1) We need our high level shift functions for all four directions.
# These will just loop through the rows/columns and do the shifts, calling helper functions

# 2) We need the functions that actually do the dirty work, shiftRowRight() and shiftRowLeft()
# These will get called by shiftRight(), shiftLeft(), shiftUp(), and shiftDown()

# 3) Once those two functions are working, they will be replaced with lookup tables

def shiftRight(board):
    newBoard = []

    for row in board:
        newBoard.append(efficientShiftRowRight(row))

    if newBoard == board:
        return False
    return newBoard
# This one is almost identical to shiftRight()
def shiftLeft(board):
    newBoard = []

    for row in board:
        newBoard.append(efficientShiftRowLeft(row))

    if newBoard == board:
        return False
    return newBoard

# Now for columns we do something tricky. When we rotate a column on its side, it becomes a row.
# So we're going to do that and then call the shiftRowRight/Left() functions
def shiftUp(board):
    columns = [[], [], [], []]

    for col in range(4):
        for row in range(4):
            columns[col].append(board[row][col])

    newColumns = []
    for column in columns:
        newColumns.append(efficientShiftRowLeft(column))

    # now we put them back on the board
    newBoard = [[" ", " ", " ", " "],
                [" ", " ", " ", " "],
                [" ", " ", " ", " "],
                [" ", " ", " ", " "]]

    for row in range(4):
        for col in range(4):
            newBoard[row][col] = newColumns[col][row]

    if newBoard == board:
        return False
    return newBoard

def shiftDown(board):
    columns = [[], [], [], []]

    for col in range(4):
        for row in range(4):
            columns[col].append(board[row][col])

    newColumns = []
    for column in columns:
        newColumns.append(efficientShiftRowRight(column))

    # now we put them back on the board
    newBoard = [[" ", " ", " ", " "],
                [" ", " ", " ", " "],
                [" ", " ", " ", " "],
                [" ", " ", " ", " "]]

    for row in range(4):
        for col in range(4):
            newBoard[row][col] = newColumns[col][row]

    if newBoard == board:
        return False
    return newBoard
def shiftRowRight(row):
    # Here's our strategy:
    # 1) remove all the spaces
    # 2) go right to left looking for things to combine

    # STEP 1
    withoutSpaces = []

    for item in row:
        if item != " ":
            withoutSpaces.append(item)

    # STEP 2
    combinedRow = [" ", " ", " ", " "]

    # This variable makes sure we don't double combine something
    firstUncombined = 3

    firstEmptySpace = 3

    for index in range(len(withoutSpaces)-1, -1, -1):
        if index > 0 and index <= firstUncombined and withoutSpaces[index] == withoutSpaces[index-1]:
            combinedRow[firstEmptySpace] = str(2*int(withoutSpaces[index]))
            firstEmptySpace -= 1
            firstUncombined = index - 2


        elif index <= firstUncombined:
            combinedRow[firstEmptySpace] = withoutSpaces[index]
            firstEmptySpace -= 1

    return combinedRow

def shiftRowLeft(row):
    # Here's our strategy:
    # 1) remove all the spaces
    # 2) go left to right looking for things to combine

    # STEP 1
    withoutSpaces = []

    for item in row:
        if item != " ":
            withoutSpaces.append(item)

    # STEP 2
    combinedRow = [" ", " ", " ", " "]

    # This variable makes sure we don't double combine something
    firstUncombined = 0

    firstEmptySpace = 0

    for index in range(0, len(withoutSpaces)):
        if index < len(withoutSpaces)-1 and index >= firstUncombined and withoutSpaces[index] == withoutSpaces[index+1]:
            combinedRow[firstEmptySpace] = str(2*int(withoutSpaces[index]))
            firstEmptySpace += 1
            firstUncombined = index + 2

        elif index >= firstUncombined:
            combinedRow[firstEmptySpace] = withoutSpaces[index]
            firstEmptySpace += 1

    return combinedRow

# Now that shiftRowRight() and shiftRowLeft() are working, we want to replace them with lookup tables
leftLookup = {}
rightLookup = {}

# we're using a dictionary, but that means that our keys can't be lists. So first we need a listToString(list) function
def listToString(list):
    string = ""
    for item in list:
        string += item
        # we're using "/" as a delimiter to separate the spaces
        string += "/"

    return string

def stringToList(string):
    list = []

    currentTile = ""
    for letter in string:
        if letter == "/":
            list.append(currentTile)
            currentTile = ""
        else:
            currentTile += letter

    return list

potentialTiles = [" ", "2", "4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048", "4096"]

for tile1 in range(12):
    for tile2 in range(12):
        for tile3 in range(12):
            for tile4 in range(12):
                potentialRow = potentialTiles[tile1] + "/" + potentialTiles[tile2] + "/" + potentialTiles[tile3] + "/" + potentialTiles[tile4] + "/"
                leftLookup[potentialRow] = shiftRowLeft(stringToList(potentialRow))
                rightLookup[potentialRow] = shiftRowRight(stringToList(potentialRow))

def efficientShiftRowRight(row):
    return rightLookup[listToString(row)]


def efficientShiftRowLeft(row):
    return leftLookup[listToString(row)]

mainBoard = [["2", "2", " ", " "],
             ["2", " ", " ", " "],
             [" ", " ", " ", " "],
             [" ", " ", " ", " "]]

printBoard(mainBoard)

while True:
    move = input("Which move? w/a/s/d ")
    if move == "w":
        newBoard = shiftUp(mainBoard)
        if newBoard != False:
            newBoard = placeRandomTile(newBoard)
            mainBoard = newBoard
        else:
            print("That wasn't a legal move")

    elif move == "a":
        newBoard = shiftLeft(mainBoard)
        if newBoard != False:
            newBoard = placeRandomTile(newBoard)
            mainBoard = newBoard
        else:
            print("That wasn't a legal move")

    elif move == "s":
        newBoard = shiftDown(mainBoard)
        if newBoard != False:
            newBoard = placeRandomTile(newBoard)
            mainBoard = newBoard
        else:
            print("That wasn't a legal move")

    else:
        newBoard = shiftRight(mainBoard)
        if newBoard != False:
            newBoard = placeRandomTile(newBoard)
            mainBoard = newBoard
        else:
            print("That wasn't a legal move")

    printBoard(mainBoard)
