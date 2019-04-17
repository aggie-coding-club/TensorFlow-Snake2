from enum import Enum


class GameBlock(Enum):
    Blank = 0
    Snake = 1
    Apple = 2


class CardinalDirections(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class RelativeDirections(Enum):
    FORWARD = 0
    LEFT = -1
    RIGHT = 1
