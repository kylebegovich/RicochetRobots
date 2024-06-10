from enum import Enum


class TileEnum(Enum):
    UNDEFINED = 0
    EMPTY = 1
    WALL = 2
    SYMBOL = 3


class SymbolEnum(Enum):
    UNDEFINED = 0
    RED_CIRCLE = 1
    RED_TRIANGLE = 2
    RED_SQUARE = 3
    RED_HEXAGON = 4
    BLUE_CIRCLE = 5
    BLUE_TRIANGLE = 6
    BLUE_SQUARE = 7
    BLUE_HEXAGON = 8
    GREEN_CIRCLE = 9
    GREEN_TRIANGLE = 10
    GREEN_SQUARE = 11
    GREEN_HEXAGON = 12
    YELLOW_CIRCLE = 13
    YELLOW_TRIANGLE = 14
    YELLOW_SQUARE = 15
    YELLOW_HEXAGON = 16
    WILDCARD = 17

    def toString(self):
        return chr(self.value + ord("A") - 1)


class RobotEnum(Enum):
    UNDEFINED = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    BLACK = 5


class TileState:
    def __init__(self, enum, value=None):
        self.enum = enum
        self.value = value
    
    def getEnum(self):
        return self.enum
    
    def getValue(self):
        return self.value


class Board:
    """
    self.boardArray is a 2d array, where odd indices are centers of squares, and even indices are between squares (wall data)
    e.g. (1, 15) is a valid location for a robot, but (2, 8) and (5, 2) are not 
    key for translation:

    0: blank
    1: wall
    A-Q: symbol tokens (A -> SymbolEnum 1, B -> SymbolEnum 2, etc.) 
    """

    SIZE = 33

    def __init__(self):
        self.board = self._blankBoard()
        self.robots = {}  # a map of robot by enum to their location (row, col) on the board

    def _blankBoard(self):
        board = []
        allWallRow = [TileState(TileEnum.WALL)] * Board.SIZE
        edgeWallRow = [TileState(TileEnum.WALL)] + ([TileState(TileEnum.EMPTY)] * (Board.SIZE - 2)) + [TileState(TileEnum.WALL)]
        board.append(allWallRow)
        for _ in range(Board.SIZE - 2):
            board.append(edgeWallRow)
        board.append(allWallRow)
        return board
    

    def importBoard(self, stringBoard):
        board = []
        for strRow in stringBoard.split("\n"):
            boardRow = []
            for char in strRow:
                if char == "X" or char == "1":
                    boardRow.append(TileState(TileEnum.WALL))
                elif char == " " or char == "0":
                    boardRow.append(TileState(TileEnum.EMPTY))
                else:
                    enumIdx = ord(char) - ord("A") + 1
                    boardRow.append(TileState(TileEnum.SYMBOL, SymbolEnum(enumIdx)))
            board.append(boardRow)

        self.board = board
        return board


    def toString(self):
        output = ""
        for row in self.board:
            outputRow = ""
            for tile in row:
                enum = tile.getEnum()
                if enum == TileEnum.EMPTY:
                    outputRow += " "
                elif enum == TileEnum.WALL:
                    outputRow += "X"
                elif enum == TileEnum.SYMBOL:
                    outputRow += tile.getValue().toString()
            output += outputRow + "\n"

        return output


gameBoard = Board()

fp = open('board.txt', 'r')
text = fp.read()

gameBoard.importBoard(text)
print(gameBoard.toString())