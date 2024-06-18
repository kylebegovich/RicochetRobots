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
    
    def matchesRobot(self, robotEnum):
        if type(robotEnum) is not RobotEnum:
            return None
        
        if robotEnum == RobotEnum.RED:
            return self == self.RED_CIRCLE or self == self.RED_TRIANGLE or self == self.RED_SQUARE or self == self.RED_HEXAGON
        if robotEnum == RobotEnum.BLUE:
            return self == self.BLUE_CIRCLE or self == self.BLUE_TRIANGLE or self == self.BLUE_SQUARE or self == self.BLUE_HEXAGON
        if robotEnum == RobotEnum.GREEN:
            return self == self.GREEN_CIRCLE or self == self.GREEN_TRIANGLE or self == self.GREEN_SQUARE or self == self.GREEN_HEXAGON
        if robotEnum == RobotEnum.YELLOW:
            return self == self.YELLOW_CIRCLE or self == self.YELLOW_TRIANGLE or self == self.YELLOW_SQUARE or self == self.YELLOW_HEXAGON
        
        return None


class RobotEnum(Enum):
    UNDEFINED = 0
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    BLACK = 5

    def matchesSymbol(self, symbolEnum):
        if type(symbolEnum) is not SymbolEnum:
            return None
        
        return symbolEnum.matchesRobot(self)
    

def testRobotAndSymbolEnums():
    print("expect True:")
    print("  ", SymbolEnum.RED_CIRCLE.matchesRobot(RobotEnum.RED))
    print("  ", SymbolEnum.BLUE_TRIANGLE.matchesRobot(RobotEnum.BLUE))
    print("  ", SymbolEnum.GREEN_SQUARE.matchesRobot(RobotEnum.GREEN))
    print("  ", SymbolEnum.YELLOW_HEXAGON.matchesRobot(RobotEnum.YELLOW))
    print("  ", RobotEnum.RED.matchesSymbol(SymbolEnum.RED_SQUARE))
    print("  ", RobotEnum.BLUE.matchesSymbol(SymbolEnum.BLUE_HEXAGON))
    print("  ", RobotEnum.GREEN.matchesSymbol(SymbolEnum.GREEN_CIRCLE))
    print("  ", RobotEnum.YELLOW.matchesSymbol(SymbolEnum.YELLOW_TRIANGLE))


    print("expect False:")
    print("  ", SymbolEnum.RED_CIRCLE.matchesRobot(RobotEnum.BLUE))
    print("  ", SymbolEnum.BLUE_TRIANGLE.matchesRobot(RobotEnum.GREEN))
    print("  ", SymbolEnum.GREEN_SQUARE.matchesRobot(RobotEnum.YELLOW))
    print("  ", SymbolEnum.YELLOW_HEXAGON.matchesRobot(RobotEnum.RED))
    print("  ", RobotEnum.GREEN.matchesSymbol(SymbolEnum.RED_SQUARE))
    print("  ", RobotEnum.YELLOW.matchesSymbol(SymbolEnum.BLUE_HEXAGON))
    print("  ", RobotEnum.BLUE.matchesSymbol(SymbolEnum.GREEN_CIRCLE))
    print("  ", RobotEnum.RED.matchesSymbol(SymbolEnum.YELLOW_TRIANGLE))


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
        # define a blank board for designing new board directions
        board = []
        allWallRow = [TileState(TileEnum.WALL)] * Board.SIZE
        edgeWallRow = [TileState(TileEnum.WALL)] + ([TileState(TileEnum.EMPTY)] * (Board.SIZE - 2)) + [TileState(TileEnum.WALL)]
        board.append(allWallRow)
        for _ in range(Board.SIZE - 2):
            board.append(edgeWallRow)
        board.append(allWallRow)
        return board
    

    def importBoard(self, stringBoard):
        # Takes stringBoard in a few formats, inverse of toString
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

        # both write to self state and returns new board
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