'''define parameters for various part of program'''

from enum import Enum

# pygame parameters
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
CELL_SIZE: int = 30
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREY = (211, 211, 211)
DARK_GREEN = (0, 100, 0)
DARK_GREY = (169, 169, 169)
EDGE_OFFSET = 1
SIDE_OFFSET = 5




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


