'''define parameters for various part of program'''

from enum import Enum

# pygame parameters
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600

# environment parameters


class State(Enum):
    WALL = 'W'
    R_APPLE = 'R'
    G_APPLE = 'G'
    TAIL = 'S'
    HEAD = 'H'
    SPACE = '0'


class Reward(Enum):
    R_APPLE = -7
    G_APPLE = 7
    GAME_OVER = -10
    SPACE = -1
    ILLEGAL_MOVE = -1000000


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


