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
        self._direction: str = random.randint(0, len(param.Direction) - 1)

        self.create_board(size)
        self.create_direction()
        self.create_snake()
        self.create_apple(param.State.G_APPLE.value)
        self.create_apple(param.State.G_APPLE.value)
        self.create_apple(param.State.R_APPLE.value)



    @property
    def board(self) -> list:
        '''getter for board attribute'''
        return self._board
 
    @property
    def snake(self) -> list:
        '''getter for snake attribute'''
        return self._snake

    def create_direction(self) -> None:
        '''generate random direction of snake'''
        self._direction = random.randint(0, len(param.Direction) - 1)

    def create_apple(self, apple_type: str) -> None:
        '''generate random apple position in board'''
        rand_row_pos: int = random.randint(1, self._size)
        rand_col_pos: int = random.randint(1, self._size)
        while self._board[rand_row_pos][rand_col_pos]\
                != param.State.SPACE.value\
                or (rand_row_pos, rand_col_pos) in self._snake:
            print("row", rand_row_pos)
            print("col",rand_col_pos) 
            rand_row_pos = random.randint(1, self._size)
            rand_col_pos = random.randint(1, self._size)
        if apple_type == param.State.G_APPLE.value:
            self._board[rand_row_pos][rand_col_pos] = param.State.G_APPLE.value
        else:
            self._board[rand_row_pos][rand_col_pos] = param.State.R_APPLE.value
         
    def create_board(self, size: int) -> None:
        '''generate board(2D array) with walls and empty space'''
        for i in range(size + 2):
            row: list = []
            for j in range(size + 2):
                if i == 0 or i == size + 1 or j == 0 or j == size + 1:
                    row.append(param.State.WALL.value)
                else:
                    row.append(param.State.SPACE.value)
            self._board.append(row)
    
    def create_snake(self) -> None:
        '''generate random snake position in board.'''
        # allow 3 spaces from edge of board for wall and tail of snake(2)
        rand_row_pos: int = random.randint(3, self._size - 2)
        rand_col_pos: int = random.randint(3, self._size - 2)
        # append snake head
        self._snake.append((rand_row_pos, rand_col_pos))
        # append 2 snake tails 
        if self._direction == param.Direction.LEFT.value:
            self._snake.append((rand_row_pos, rand_col_pos + 1))
            self._snake.append((rand_row_pos, rand_col_pos + 2))
        elif self._direction == param.Direction.RIGHT.value:
            self._snake.append((rand_row_pos, rand_col_pos - 1))
            self._snake.append((rand_row_pos, rand_col_pos - 2))
        elif self._direction == param.Direction.UP.value:
            self._snake.append((rand_row_pos + 1, rand_col_pos))
            self._snake.append((rand_row_pos + 2, rand_col_pos))
        else:
            self._snake.append((rand_row_pos - 1, rand_col_pos))
            self._snake.append((rand_row_pos - 2, rand_col_pos))
 