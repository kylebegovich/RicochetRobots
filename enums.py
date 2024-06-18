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