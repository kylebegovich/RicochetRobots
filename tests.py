from model import *
import difflib

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
    gameBoard = Board()
    fp = open('board.txt', 'r')
    text = fp.read()

    gameBoard.importBoard(text)
    beforeTranslation = gameBoard.toString()
    gameBoard.importBoard(beforeTranslation)
    afterTranslation = gameBoard.toString()
    print("  expect True:")
    print("    ", beforeTranslation == afterTranslation)


def testRobotsImported():
    print("testRobotsImported")
    gameBoard = Board()
    fp = open('boardWithRobots.txt', 'r')
    text = fp.read()

    gameBoard.importBoard(text)
    # print(gameBoard.toString())
    expectedRobots = {
        RobotEnum.RED: (1, 25),
        RobotEnum.BLUE: (1, 26),
        RobotEnum.GREEN: (2, 31),
        RobotEnum.YELLOW: (30, 1),
        RobotEnum.BLACK: (31, 30),
    }
    print("  expect True:")
    print("    ", gameBoard.robots == expectedRobots)


def testIsMoveValid():
    pass

def runAllTests():
    testRobotAndSymbolEnums()
    testBoardToStringInversion()
    testRobotsImported()


runAllTests()



