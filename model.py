from enums import TileEnum, SymbolEnum, DirEnum, RobotEnum, TileState


class Board:
    """
    self.boardArray is a 2d array, where odd indices are centers of squares, and even indices are between squares (wall data)
    e.g. (1, 15) is a valid location for a robot, but (2, 8) and (5, 2) are not 
    key for translation:

    0: blank
    1: wall
    5-9: robots (Red, Blue, Green, Yellow, Black, respectively)
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