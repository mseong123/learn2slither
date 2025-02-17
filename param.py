'''define parameters for various part of program'''

from enum import Enum

# pygame parameters
SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
CELL_SIZE: int = 30
BUTTON_HEIGHT: int = CELL_SIZE * 1.3
BUTTON_WIDTH: int = CELL_SIZE * 4
BUTTON_PADDING: int = 10
WHITE: tuple = (255, 255, 255)
GREEN: tuple = (0, 255, 0)
RED: tuple = (255, 0, 0)
BLUE: tuple = (0, 0, 255)
DARK_BLUE: tuple = (0, 0, 139)
BLACK: tuple = (0, 0, 0)
GREY: tuple = (211, 211, 211)
DARK_GREY: tuple = (169, 169, 169)
ORANGE: tuple = (255, 140, 0)
EDGE_OFFSET: int = 1
SIDE_OFFSET: int = 15
AGENT_OFFSET: int = CELL_SIZE * 6
HEADER_SIZE: int = 36
TEXT_SIZE: int = 24
PADDING: int = 10
BOARD_STATE: dict = {
    "state": []
}
LOOP: dict = {
    "count": 0,
    "limit": 60,
}

# Agent hyperparams - based on how complex environment is,
# empirical data and rule of thumb. No real definite answer
# similar to other ML problems. Using comparison to models
# like cartwheel (simple problem) and atari DQN(more complex)
# All the params below are based on simple problem ie cartwheel
RANDOM_STATE = 42
# MAX_BATCH_SIZE
MAX_BATCH_HUNDRED = 48
# TRAIN FREQUENCY (no of steps)
FREQ = 4
# BUFFER SIZE
REPLAY_SIZE = 40000
# UPDATE TARGET NETWORK (no of steps)
UPDATE_NETWORK = 150
# looping threshold
MAX_LOOP = 3
DEFAULT_E = 1
MIN_E = 0.1

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
    R_APPLE = -20
    G_APPLE = 25
    GAME_OVER = -40
    SPACE = -0.2
    ILLEGAL_MOVE = -40


class Action(Enum):
    '''Action enum'''
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
