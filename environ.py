'''board / environment class with attributes and methods'''

import random
import param


class Board():
    '''The environment will determine the predefined rules as per subject.pdf
    and pass states to agent.
    '''
    def __init__(self, size: int = 10, speed: int = 1):
        self._size: int = size + 2 # to account for walls
        self._speed: int = speed
        self._board: list = []
        self._snake: list = []
        self._direction: str = random.randint(0, len(param.Direction) - 1)
        self._state: list = []
        self._length: int = 3
        self._duration: int = 0
        self.reset_board()
        print("\nGAME START\n")
        self._print_state()



    @property
    def board(self) -> list:
        '''getter for board attribute'''
        return self._board
 
    @property
    def snake(self) -> list:
        '''getter for snake attribute'''
        return self._snake
    
    @property
    def size(self) -> int:
        '''getter for board attribute'''
        return self._size

    def reset_board(self) -> None:
        '''wrapper function to reset board and snake'''
        self._create_board()
        self._create_direction()
        self._create_snake()
        self._create_apple(param.State.G_APPLE.value)
        self._create_apple(param.State.G_APPLE.value)
        self._create_apple(param.State.R_APPLE.value)


    def _create_direction(self) -> None:
        '''generate random direction of snake'''
        self._direction = random.randint(0, len(param.Direction) - 1)

    def _create_apple(self, apple_type: str) -> None:
        '''generate random apple position in board'''
        rand_row_pos: int = random.randint(1, self._size - 2)
        rand_col_pos: int = random.randint(1, self._size - 2)
        while self._board[rand_row_pos][rand_col_pos]\
                != param.State.SPACE.value\
                or (rand_row_pos, rand_col_pos) in self._snake:
            rand_row_pos = random.randint(1, self._size - 2)
            rand_col_pos = random.randint(1, self._size - 2)
        if apple_type == param.State.G_APPLE.value:
            self._board[rand_row_pos][rand_col_pos] = param.State.G_APPLE.value
        else:
            self._board[rand_row_pos][rand_col_pos] = param.State.R_APPLE.value
         
    def _create_board(self) -> None:
        '''generate board(2D array) with walls and empty space'''
        self._board: list = []
        for i in range(self._size):
            row: list = []
            for j in range(self._size):
                if i == 0 or i == self._size - 1 or j == 0 or\
                    j == self._size - 1:
                    row.append(param.State.WALL.value)
                else:
                    row.append(param.State.SPACE.value)
            self._board.append(row)
    
    def _create_snake(self) -> None:
        '''generate random snake position in board.'''
        self._snake: list = []
        # allow 3 spaces from edge of board for wall and tail of snake(2)
        rand_row_pos: int = random.randint(3, self._size - 4)
        rand_col_pos: int = random.randint(3, self._size - 4)
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

    def _get_next_pos(self, next_direction: int) -> tuple:
        next_row: int = self._snake[0][0]
        next_col: int = self._snake[0][1]
        if next_direction == param.Direction.UP.value:
            next_row = next_row - 1
        elif next_direction == param.Direction.DOWN.value:
            next_row = next_row + 1
        elif next_direction == param.Direction.LEFT.value:
            next_col = next_col - 1
        else:
            next_col = next_col + 1
        return (next_row, next_col)

    def _check_died(self, next_direction: int) -> bool:
        '''function to check snake died and start a new episode'''
        next_row, next_col = self._get_next_pos(next_direction)
        if self._board[next_row][next_col] == param.State.WALL.value\
            or (self._board[next_row][next_col] == param.State.R_APPLE.value
                and len(self._snake) == 1)\
                or (next_row, next_col) in self._snake:
            return True
        return False

    def _check_illegal(self, next_direction: int) -> bool:
        '''function to check for illegal move'''
        # if current direction is up and next direction is down,
        # and length of snake > 1, return True
        if len(self._snake) > 1:
            if (self._direction == param.Direction.UP.value and
                    next_direction == param.Direction.DOWN.value) or\
                (self._direction == param.Direction.DOWN.value and
                    next_direction == param.Direction.UP.value) or\
                (self._direction == param.Direction.LEFT.value and
                    next_direction == param.Direction.RIGHT.value) or\
                (self._direction == param.Direction.RIGHT.value and
                    next_direction == param.Direction.LEFT.value):
                return True
        return False
    
    def _check_green_apple(self, next_direction: int) -> bool:
        '''function to check move consume green apple'''
        next_row, next_col = self._get_next_pos(next_direction)
        if self._board[next_row][next_col] == param.State.G_APPLE.value:
            return True
        return False
    

    def _check_red_apple(self, next_direction: int) -> bool:
        '''function to check move consume red apple'''
        next_row, next_col = self._get_next_pos(next_direction)
        if self._board[next_row][next_col] == param.State.R_APPLE.value:
            return True
        return False

    def _get_state(self) -> list:
        '''function to get line of view (state) of 4 directions from head of
        snake. State values are [dist to wall, dist to first green apple,
        dist to red apple, dist to tail]'''
        state: list = []
        # 4 directions following param.Direction enum
        for i in range(len(param.Direction)):
            # UP
            if i == 0:
                # Distance to wall
                state.append(self._snake[0][0] / self._size)
                # Distance to first green apple
                g_apple_visible: int = 0
                for j in range(self._snake[0][0] - 1, 0, -1):
                    if self._board[j][self._snake[0][1]] ==\
                            param.State.G_APPLE.value:
                        state.append((self._snake[0][0] - j) / self._size)
                        g_apple_visible = 1
                        break
                if g_apple_visible == 0:
                    state.append(0)
                # Distance to first red apple
                r_apple_visible: int = 0
                for j in range(self._snake[0][0] - 1, 0, -1):
                    if self._board[j][self._snake[0][1]] ==\
                            param.State.R_APPLE.value:
                        state.append((self._snake[0][0] - j) / self._size)
                        r_apple_visible = 1
                        break
                if r_apple_visible == 0:
                    state.append(0)
                # Distance to tail
                snake_visible: int = 0
                for j in range(self._snake[0][0] - 1, 0, -1):
                    if (j, self._snake[0][1]) in self._snake:
                        state.append((self._snake[0][0] - j) / self._size)
                        snake_visible = 1
                        break
                if snake_visible == 0:
                    state.append(0)
            # DOWN
            if i == 1:
                # Distance to wall
                state.append((len(self._board[0]) - 1 - self._snake[0][0])
                             / self._size)
                # Distance to first green apple
                g_apple_visible: int = 0
                for j in range(self._snake[0][0] + 1, len(self._board[0]) - 1):
                    if self._board[j][self._snake[0][1]] ==\
                            param.State.G_APPLE.value:
                        state.append((j - self._snake[0][0]) / self._size)
                        g_apple_visible = 1
                        break
                if g_apple_visible == 0:
                    state.append(0)
                # Distance to first red apple
                r_apple_visible: int = 0
                for j in range(self._snake[0][0] + 1, len(self._board[0]) - 1):
                    if self._board[j][self._snake[0][1]] ==\
                            param.State.R_APPLE.value:
                        state.append((j - self._snake[0][0]) / self._size)
                        r_apple_visible = 1
                        break
                if r_apple_visible == 0:
                    state.append(0)
                # Distance to tail
                snake_visible: int = 0
                for j in range(self._snake[0][0] + 1, len(self._board[0]) - 1):
                    if (j, self._snake[0][1]) in self._snake:
                        state.append((j - self._snake[0][0]) / self._size)
                        snake_visible = 1
                        break
                if snake_visible == 0:
                    state.append(0)
            # LEFT
            if i == 2:
                # Distance to wall
                state.append((self._snake[0][1]) / self._size)
                # Distance to first green apple
                g_apple_visible: int = 0
                for j in range(self._snake[0][1] - 1, 0, -1):
                    if self._board[self._snake[0][0]][j] ==\
                            param.State.G_APPLE.value:
                        state.append((self._snake[0][1] - j) / self._size)
                        g_apple_visible = 1
                        break
                if g_apple_visible == 0:
                    state.append(0)
                # Distance to first red apple
                r_apple_visible: int = 0
                for j in range(self._snake[0][1] - 1, 0, -1):
                    if self._board[self._snake[0][0]][j] ==\
                            param.State.R_APPLE.value:
                        state.append((self._snake[0][1] - j) / self._size)
                        r_apple_visible = 1
                        break
                if r_apple_visible == 0:
                    state.append(0)
                # Distance to tail
                snake_visible: int = 0
                for j in range(self._snake[0][1] - 1, 0, -1):
                    if (self._snake[0][0], j) in self._snake:
                        state.append((self._snake[0][1] - j) / self._size)
                        snake_visible = 1
                        break
                if snake_visible == 0:
                    state.append(0)
            # RIGHT
            if i == 3:
                # Distance to wall
                state.append((len(self._board[0]) - 1 - self._snake[0][1])
                             / self._size)
                # Distance to first green apple
                g_apple_visible: int = 0
                for j in range(self._snake[0][1] + 1, len(self._board[0]) - 1):
                    if self._board[self._snake[0][0]][j] ==\
                            param.State.G_APPLE.value:
                        state.append((j - self._snake[0][1]) / self._size)
                        g_apple_visible = 1
                        break
                if g_apple_visible == 0:
                    state.append(0)
                # Distance to first red apple
                r_apple_visible: int = 0
                for j in range(self._snake[0][1] + 1, len(self._board[0]) - 1):
                    if self._board[self._snake[0][0]][j] ==\
                            param.State.R_APPLE.value:
                        state.append((j - self._snake[0][1]) / self._size)
                        r_apple_visible = 1
                        break
                if r_apple_visible == 0:
                    state.append(0)
                # Distance to tail
                snake_visible: int = 0
                for j in range(self._snake[0][1] + 1, len(self._board[0]) - 1):
                    if (self._snake[0][0], j) in self._snake:
                        state.append((j - self._snake[0][1]) / self._size)
                        snake_visible = 1
                        break
                if snake_visible == 0:
                    state.append(0)
        return state

    def get_initial_state(self) -> list:
        '''return initial state before first move by snake.''' 
        return self._get_state()

    def _amend_snake(self, next_direction: int, action: str) -> None:
        '''amend snake list of tuple positions'''
        next_row, next_col = self._get_next_pos(next_direction)
        if action == "lengthen": 
            temp_snake: list = self._snake.copy()
            self._snake: list = [(next_row, next_col), *temp_snake]
        elif action == "shorten":
            self._snake.pop()
            self._snake.pop()
            temp_snake: list = self._snake.copy()
            self._snake: list = [(next_row, next_col), *temp_snake]
        else:
            self._snake.pop()
            temp_snake: list = self._snake.copy()
            self._snake: list = [(next_row, next_col), *temp_snake]
        # reset any food eaten to space
        self._board[next_row][next_col] = param.State.SPACE.value
        

    def _print_state(self) -> None:
        "print state to terminal"
        for index_row, _ in enumerate(self._board):
            state: str = ""
            for index_col, col in enumerate(self._board[index_row]):
                if self._snake[0][0] == index_row\
                      or self._snake[0][1] == index_col:
                    if (index_row, index_col) in self._snake\
                          and (index_row, index_col) == self._snake[0]:
                        state += param.State.HEAD.value
                    elif (index_row, index_col) in self._snake:
                        state += param.State.TAIL.value
                    else:
                        state += col
                else:
                    state += " "
            print(state)


    def move(self, next_direction: int) -> list:
        '''function to change state of board upon a direction move and return
        a list of state values to agent'''
        # return value is a list to be included in agent's replay buffer
        # [direction, reward, new state after direction, terminal move bool]
        reward: int = 0
        fatal: bool = False
        if self._check_illegal(next_direction) is True:
            self.reset_board()
            print("\nRESET BOARD\n")
            reward = param.Reward.ILLEGAL_MOVE.value
            fatal = True
        elif self._check_died(next_direction) is True:
            self.reset_board()
            print("\nRESET BOARD\n")
            reward = param.Reward.GAME_OVER.value
            fatal = True
        elif self._check_green_apple(next_direction) is True:
            self._amend_snake(next_direction, "lengthen")
            self._create_apple(param.State.G_APPLE.value)
            reward = param.Reward.G_APPLE.value 
        elif self._check_red_apple(next_direction) is True:
            self._amend_snake(next_direction, "shorten")
            self._create_apple(param.State.R_APPLE.value)
            reward = param.Reward.R_APPLE.value
        else:
            self._amend_snake(next_direction, "move")
            reward = param.Reward.SPACE.value
        if fatal is not True:
            self._direction = next_direction
            print(f"\n{param.Direction(next_direction).name}\n")
        self._print_state()
        print([next_direction, reward, fatal,
               *self._get_state()])

