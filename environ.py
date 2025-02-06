'''board / environment class with attributes and methods'''

import random
import param


class Board():
    '''The environment will determine the predefined rules as per subject.pdf
    and pass states to agent.
    '''
    def __init__(self, size: int = 10, speed: int = 1):
        self._size: int = size
        self._speed: int = speed
        self._board: list = []
        self._snake: list = []
        self._direction: str = "UP"

        self.create_board(size)
        self.create_snake()
        self.create_apple(param.State.G_APPLE)
        self.create_apple(param.State.G_APPLE)
        self.create_apple(param.State.R_APPLE)



    @property
    def board(self) -> list:
        '''getter for board attribute'''
        return self._board
    
    def create_apple(self, apple_type: str) -> None:
        '''generate random apple position in board'''
        rand_row_pos: int = random.randint(1, self._size)
        rand_col_pos: int = random.randint(1, self._size)
        while self._board[rand_row_pos][rand_col_pos] != param.State.SPACE\
                and (rand_row_pos, rand_col_pos) not in self._snake:
            rand_row_pos = random.randint(1, self._size)
            rand_col_pos = random.randint(1, self._size)
        if apple_type == param.State.G_APPLE:
            self._board[rand_row_pos][rand_col_pos] = param.State.G_APPLE
        else:
            self._board[rand_row_pos][rand_col_pos] = param.State.R_APPLE
         
    def create_board(self, size: int) -> None:
        '''generate board(2D array) with walls and empty space'''
        for i in range(size + 2):
            row: list = []
            for j in range(size + 2):
                if i == 0 or i == size + 1 or j == 0 or j == size + 1:
                    row.append(param.State.WALL)
                else:
                    row.append(param.State.SPACE)
            self._board.append(row)
    
    def create_snake(self) -> None:
        '''generate random snake position in board'''
        # allow 3 spaces from edge of board for wall and tail of snake(2)
        rand_row_pos: int = random.randint(3, self._size - 2)
        rand_col_pos: int = random.randint(3, self._size - 2)
        self._snake.append((rand_row_pos, rand_col_pos))
        rand_direction: int = random.randint(0,3)
        

    
        