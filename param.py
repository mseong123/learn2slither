'''define parameters for various part of program'''

from enum import Enum

# pygame parameters
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
CELL_SIZE: int = 30
BUTTON_HEIGHT: int = CELL_SIZE * 1.3
BUTTON_WIDTH: int = CELL_SIZE * 4
BUTTON_PADDING: int = 10
GREEN: tuple = (0, 255, 0)
RED: tuple = (255, 0, 0)
BLUE: tuple = (0, 0, 255)
DARK_BLUE: tuple = (0, 0, 139)
BLACK: tuple = (0, 0, 0)
GREY: tuple = (211, 211, 211)
DARK_GREY: tuple = (169, 169, 169)
ORANGE: tuple = (255, 140, 0)
EDGE_OFFSET: int = 1
SIDE_OFFSET: int = 10
HEADER_SIZE: int = 36
TEXT_SIZE: int = 24
PADDING: int = 10

# MLP hyperparams
RANDOM_STATE = 42
# INPUT COUNT OF STATE FROM ENVIRONMENT 
# [DISTANCE TO WALL, G_APPLE, R_APPLE, TAIL X 4 ACTIONS]
INPUT_COUNT = 16
# MAX_BATCH_SIZE 
MAX_BATCH_TEN = 16
MAX_BATCH_HUNDRED = 48
# TRAIN FREQUENCY (no of steps)
FREQ_TEN = 2
FREQ_HUNDRED = 4
# BUFFER SIZE
REPLAY_SIZE_ONE = 100
REPLAY_SIZE_TEN = 500
REPLAY_SIZE_HUNDRED = 5000
# UPDATE TARGET NETWORK (no of steps)
UPDATE_ONE = 10
UPDATE_TEN = 50
UPDATE_HUNDRED = 500

# environment parameters
class State(Enum):
    '''State enum'''
    WALL = 'W'
    R_APPLE = 'R'
    G_APPLE = 'G'
    TAIL = 'S'
    HEAD = 'H'
    SPACE = '0'


class Reward(Enum):
    '''Reward enum'''
    R_APPLE = -7
    G_APPLE = 7
    GAME_OVER = -10
    SPACE = -1
    ILLEGAL_MOVE = -10000


class Action(Enum):
    '''Action enum'''
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3



