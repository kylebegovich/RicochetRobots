from enum import Enum


class TileEnum(Enum):
    UNDEFINED = 0
    EMPTY = 1
    WALL = 2
    SYMBOL = 3


class DirEnum(Enum):
    UNDEFINED = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


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
    
    def matchingRobot(self):
        if self == self.RED_CIRCLE or self == self.RED_TRIANGLE or self == self.RED_SQUARE or self == self.RED_HEXAGON:
            return RobotEnum.RED
        if self == self.BLUE_CIRCLE or self == self.BLUE_TRIANGLE or self == self.BLUE_SQUARE or self == self.BLUE_HEXAGON:
            return RobotEnum.BLUE
        if self == self.GREEN_CIRCLE or self == self.GREEN_TRIANGLE or self == self.GREEN_SQUARE or self == self.GREEN_HEXAGON:
            return RobotEnum.GREEN
        if self == self.YELLOW_CIRCLE or self == self.YELLOW_TRIANGLE or self == self.YELLOW_SQUARE or self == self.YELLOW_HEXAGON:
            return RobotEnum.YELLOW
        
    
    def matchesRobot(self, robotEnum):
        if type(robotEnum) is not RobotEnum:
            return None
        
        if self == self.WILDCARD:
            return True
        return robotEnum == self.matchingRobot()


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


class TileState:
    def __init__(self, enum, value=None, position=None, robot=None):
        self.enum = enum
        self.value = value
        self.position = position
        self.robot = robot

    def getEnum(self):
        return self.enum

    def getValue(self):
        return self.value
    
    def getPosition(self):
        return self.position
    
    def getRobot(self):
        return self.robot

    def setRobot(self, robot):
        self.robot = robot

    def robotMatchesDestination(self):
        if self.value is None or self.robot is None:
            return False
        
        if self.value.matchesRobot(self.robot):
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
        for row, strRow in enumerate(stringBoard.split("\n")):
            boardRow = []
            for col, char in enumerate(strRow):
                if char == "X" or char == "1":
                    boardRow.append(TileState(enum=TileEnum.WALL, position=(row, col)))
                elif char == " " or char == "0":
                    boardRow.append(TileState(enum=TileEnum.EMPTY, position=(row, col)))
                elif char == "5" or char == "🔴":
                    self.robots[RobotEnum.RED] = (row, col)
                    boardRow.append(TileState(enum=TileEnum.EMPTY, position=(row, col), robot=RobotEnum.RED))
                elif char == "6" or char == "🔵":
                    self.robots[RobotEnum.BLUE] = (row, col)
                    boardRow.append(TileState(enum=TileEnum.EMPTY, position=(row, col), robot=RobotEnum.BLUE))
                elif char == "7" or char == "🟢":
                    self.robots[RobotEnum.GREEN] = (row, col)
                    boardRow.append(TileState(enum=TileEnum.EMPTY, position=(row, col), robot=RobotEnum.GREEN))
                elif char == "8" or char == "🟡":
                    self.robots[RobotEnum.YELLOW] = (row, col)
                    boardRow.append(TileState(enum=TileEnum.EMPTY, position=(row, col), robot=RobotEnum.YELLOW))
                elif char == "9" or char == "⚫":
                    self.robots[RobotEnum.BLACK] = (row, col)
                    boardRow.append(TileState(enum=TileEnum.EMPTY, position=(row, col), robot=RobotEnum.BLACK))
                elif ord(char) >= ord("A") and ord(char) <= ord("Z"):
                    enumIdx = ord(char) - ord("A") + 1
                    boardRow.append(TileState(enum=TileEnum.SYMBOL, value=SymbolEnum(enumIdx), position=(row, col)))

            # handle newline at the end of files, whitespace lines, etc.
            if len(boardRow) > 0:
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

        for robotEnum, position in self.robots.items():
            row = position[0]
            col = position[1]
            strPos = row * (self.SIZE+1) + col
            symbol = None
            if robotEnum == RobotEnum.RED:
                symbol = "5"
            elif robotEnum == RobotEnum.BLUE:
                symbol = "6"
            elif robotEnum == RobotEnum.GREEN:
                symbol = "7"
            elif robotEnum == RobotEnum.YELLOW:
                symbol = "8"
            elif robotEnum == RobotEnum.BLACK:
                symbol = "9"

            # TODO: if possible, use emoji like below that's still monospaced
            # if robotEnum == RobotEnum.RED:
            #     symbol = "🔴"
            # elif robotEnum == RobotEnum.BLUE:
            #     symbol = "🔵"
            # elif robotEnum == RobotEnum.GREEN:
            #     symbol = "🟢"
            # elif robotEnum == RobotEnum.YELLOW:
            #     symbol = "🟡"
            # elif robotEnum == RobotEnum.BLACK:
            #     symbol = "⚫"

            output = output[:strPos] + symbol + output[strPos+1:]

        return output


    def getAdjacentTileState(self, position, dirEnum):
        if type(dirEnum) != DirEnum:
            return None

        row = position[0]
        col = position[1]
        # pos off the board
        if row < 1 or row >= self.SIZE or col < 1 or col >= self.SIZE:
            return None
        
        adjTilePos = [row, col]
        if dirEnum == DirEnum.UP:
            adjTilePos[0] -= 1
        elif dirEnum == DirEnum.DOWN:
            adjTilePos[0] += 1
        elif dirEnum == DirEnum.LEFT:
            adjTilePos[1] -= 1
        elif dirEnum == DirEnum.RIGHT:
            adjTilePos[1] += 1

        return self.board[adjTilePos[0]][adjTilePos[1]]


    def isMoveValid(self, robotEnum, dirEnum):
        if type(robotEnum) != RobotEnum:
            return None
        
        if robotEnum not in self.robots:
            return None
        position = self.robots[robotEnum]

        adjTileState = self.getAdjacentTileState(position, dirEnum)
        # blocked by a wall
        if adjTileState.enum == TileEnum.WALL:
            return False
        
        for pos in self.robots.values():
            # blocked by robot
            if adjTileState.position[0] == pos[0] and adjTileState.position[1] == pos[1]:
                return False
            
        return True
    

    def moveRobot(self, robotEnum, dirEnum):
        if not self.isMoveValid(robotEnum, dirEnum):
            return None
        
        startPos = self.robots[robotEnum]
        startTile = self.board[startPos[0]][startPos[1]]
        currPos = startPos
        adjTile = self.getAdjacentTileState(currPos, dirEnum)
        while adjTile.enum != TileEnum.WALL and adjTile.robot is None:
            tempPos = adjTile.position
            adjTile = self.getAdjacentTileState(tempPos, dirEnum)
            currPos = tempPos

        startTile.setRobot(None)
        destTile = self.board[currPos[0]][currPos[1]]
        destTile.setRobot(robotEnum)
        self.robots[robotEnum] = destTile.position

    
    def isTurnOver(self, destinationSymbol):
        for pos in self.robots.values():
            tile = self.board[pos[0]][pos[1]]
            if tile.enum == TileEnum.SYMBOL and tile.value is not None and tile.value == destinationSymbol:
                return tile.robotMatchesDestination() == destinationSymbol
        return False