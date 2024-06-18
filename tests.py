from model import *


def getTestBoard():
    gameBoard = Board()
    fp = open('boardWithRobots.txt', 'r')
    text = fp.read()

    gameBoard.importBoard(text)
    return gameBoard


def testRobotAndSymbolEnums():
    print("testRobotAndSymbolEnums:")
    print("  expect True:")
    print("    ", SymbolEnum.RED_CIRCLE.matchesRobot(RobotEnum.RED))
    print("    ", SymbolEnum.BLUE_TRIANGLE.matchesRobot(RobotEnum.BLUE))
    print("    ", SymbolEnum.GREEN_SQUARE.matchesRobot(RobotEnum.GREEN))
    print("    ", SymbolEnum.YELLOW_HEXAGON.matchesRobot(RobotEnum.YELLOW))
    print("    ", RobotEnum.RED.matchesSymbol(SymbolEnum.RED_SQUARE))
    print("    ", RobotEnum.BLUE.matchesSymbol(SymbolEnum.BLUE_HEXAGON))
    print("    ", RobotEnum.GREEN.matchesSymbol(SymbolEnum.GREEN_CIRCLE))
    print("    ", RobotEnum.YELLOW.matchesSymbol(SymbolEnum.YELLOW_TRIANGLE))


    print("  expect False:")
    print("    ", SymbolEnum.RED_CIRCLE.matchesRobot(RobotEnum.BLUE))
    print("    ", SymbolEnum.BLUE_TRIANGLE.matchesRobot(RobotEnum.GREEN))
    print("    ", SymbolEnum.GREEN_SQUARE.matchesRobot(RobotEnum.YELLOW))
    print("    ", SymbolEnum.YELLOW_HEXAGON.matchesRobot(RobotEnum.RED))
    print("    ", RobotEnum.GREEN.matchesSymbol(SymbolEnum.RED_SQUARE))
    print("    ", RobotEnum.YELLOW.matchesSymbol(SymbolEnum.BLUE_HEXAGON))
    print("    ", RobotEnum.BLUE.matchesSymbol(SymbolEnum.GREEN_CIRCLE))
    print("    ", RobotEnum.RED.matchesSymbol(SymbolEnum.YELLOW_TRIANGLE))


def testBoardToStringInversion():
    print("testBoardToStringInversion")
    testBoard = getTestBoard()

    beforeTranslation = testBoard.toString()
    testBoard.importBoard(beforeTranslation)
    afterTranslation = testBoard.toString()
    print("  expect True:")
    print("    ", beforeTranslation == afterTranslation)


def testRobotsImported():
    print("testRobotsImported")
    testBoard = getTestBoard()
    expectedRobots = {
        RobotEnum.RED: (1, 25),
        RobotEnum.BLUE: (1, 26),
        RobotEnum.GREEN: (2, 31),
        RobotEnum.YELLOW: (30, 1),
        RobotEnum.BLACK: (31, 30),
    }
    print("  expect True:")
    print("    ", testBoard.robots == expectedRobots)


def testIsMoveValid():
    print("testIsMoveValid")
    testBoard = getTestBoard()

    print("  expect True:")
    print("    ", testBoard.isMoveValid(RobotEnum.RED, DirEnum.DOWN))
    print("    ", testBoard.isMoveValid(RobotEnum.BLUE, DirEnum.DOWN))
    print("    ", testBoard.isMoveValid(RobotEnum.BLUE, DirEnum.RIGHT))
    print("    ", testBoard.isMoveValid(RobotEnum.GREEN, DirEnum.UP))
    print("    ", testBoard.isMoveValid(RobotEnum.GREEN, DirEnum.DOWN))
    print("    ", testBoard.isMoveValid(RobotEnum.GREEN, DirEnum.LEFT))
    print("    ", testBoard.isMoveValid(RobotEnum.YELLOW, DirEnum.UP))
    print("    ", testBoard.isMoveValid(RobotEnum.YELLOW, DirEnum.DOWN))
    print("    ", testBoard.isMoveValid(RobotEnum.YELLOW, DirEnum.RIGHT))
    print("    ", testBoard.isMoveValid(RobotEnum.BLACK, DirEnum.UP))
    print("    ", testBoard.isMoveValid(RobotEnum.BLACK, DirEnum.LEFT))
    print("    ", testBoard.isMoveValid(RobotEnum.BLACK, DirEnum.RIGHT))

    print("  expect False:")
    print("    ", testBoard.isMoveValid(RobotEnum.RED, DirEnum.UP))
    print("    ", testBoard.isMoveValid(RobotEnum.RED, DirEnum.LEFT))
    print("    ", testBoard.isMoveValid(RobotEnum.RED, DirEnum.RIGHT))
    print("    ", testBoard.isMoveValid(RobotEnum.BLUE, DirEnum.UP))
    print("    ", testBoard.isMoveValid(RobotEnum.BLUE, DirEnum.LEFT))
    print("    ", testBoard.isMoveValid(RobotEnum.GREEN, DirEnum.RIGHT))
    print("    ", testBoard.isMoveValid(RobotEnum.YELLOW, DirEnum.LEFT))
    print("    ", testBoard.isMoveValid(RobotEnum.BLACK, DirEnum.DOWN))


def testGetAdjacentTileState():
    print("testGetAdjacentTileState")
    testBoard = getTestBoard()
    redPos = testBoard.robots[RobotEnum.RED]
    bluePos = testBoard.robots[RobotEnum.BLUE]
    print("  expect True:")
    print("    ", testBoard.getAdjacentTileState(redPos, DirEnum.LEFT).getEnum() == TileEnum.WALL)
    print("    ", testBoard.getAdjacentTileState(redPos, DirEnum.DOWN).getEnum() == TileEnum.EMPTY)
    print("    ", testBoard.getAdjacentTileState(redPos, DirEnum.RIGHT).getEnum() == TileEnum.EMPTY)
    print("    ", testBoard.getAdjacentTileState(redPos, DirEnum.RIGHT).getRobot() == RobotEnum.BLUE)
    print("    ", testBoard.getAdjacentTileState(bluePos, DirEnum.LEFT).getEnum() == TileEnum.EMPTY)
    print("    ", testBoard.getAdjacentTileState(bluePos, DirEnum.LEFT).getRobot() == RobotEnum.RED)


def testMoveRobot():
    print("testMoveRobot")
    testBoard = getTestBoard()
    print("  expect False:")
    print("    ", testBoard.isTurnOver(SymbolEnum.WILDCARD))
    print("    ", testBoard.isTurnOver(SymbolEnum.GREEN_TRIANGLE))
    print("    ", testBoard.isTurnOver(SymbolEnum.RED_CIRCLE))
    testBoard.moveRobot(RobotEnum.GREEN, DirEnum.LEFT)
    testBoard.moveRobot(RobotEnum.GREEN, DirEnum.DOWN)
    testBoard.moveRobot(RobotEnum.GREEN, DirEnum.LEFT)
    print("    ", testBoard.isTurnOver(SymbolEnum.RED_TRIANGLE))
    testBoard.moveRobot(RobotEnum.RED, DirEnum.DOWN)
    testBoard.moveRobot(RobotEnum.RED, DirEnum.LEFT)
    testBoard.moveRobot(RobotEnum.RED, DirEnum.UP)
    print("    ", testBoard.isTurnOver(SymbolEnum.RED_TRIANGLE))
    testBoard.moveRobot(RobotEnum.RED, DirEnum.LEFT)
    print("  expect True:")
    print("    ", testBoard.isTurnOver(SymbolEnum.RED_TRIANGLE))
    print("  expect False:")
    print("    ", testBoard.isTurnOver(SymbolEnum.WILDCARD))
    print("    ", testBoard.isTurnOver(SymbolEnum.GREEN_TRIANGLE))
    print("    ", testBoard.isTurnOver(SymbolEnum.RED_CIRCLE))


def runAllTests():
    testRobotAndSymbolEnums()
    testBoardToStringInversion()
    testRobotsImported()
    testIsMoveValid()
    testGetAdjacentTileState()
    testMoveRobot()


runAllTests()



