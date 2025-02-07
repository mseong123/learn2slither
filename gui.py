'''functions to run pygame GUI'''

import pygame
import environ
import param


def draw_wall(screen: pygame.Surface, board: environ.Board,
              index_row: int, index_col: int) -> None:
    '''sub function to draw wall with border radius'''
    if index_col == 0 and index_row == 0:
        row: int = index_row + param.EDGE_OFFSET
        col: int = index_col + param.EDGE_OFFSET
        pygame.draw.rect(screen, param.DARK_GREY,
                         (col*param.CELL_SIZE,
                          row*param.CELL_SIZE,
                          param.CELL_SIZE,
                          param.CELL_SIZE),
                         border_top_left_radius=5)
    elif index_col == board.size - 1 and index_row == board.size - 1:
        row: int = index_row + param.EDGE_OFFSET
        col: int = index_col + param.EDGE_OFFSET
        pygame.draw.rect(screen, param.DARK_GREY,
                         (col*param.CELL_SIZE,
                          row*param.CELL_SIZE,
                          param.CELL_SIZE,
                          param.CELL_SIZE),
                         border_bottom_right_radius=5)
    elif index_col == 0 and index_row == board.size - 1:
        row: int = index_row + param.EDGE_OFFSET
        col: int = index_col + param.EDGE_OFFSET
        pygame.draw.rect(screen, param.DARK_GREY,
                         (col*param.CELL_SIZE,
                          row*param.CELL_SIZE,
                          param.CELL_SIZE,
                          param.CELL_SIZE),
                         border_bottom_left_radius=5)
    elif index_col == board.size - 1 and index_row == 0:
        row: int = index_row + param.EDGE_OFFSET
        col: int = index_col + param.EDGE_OFFSET
        pygame.draw.rect(screen, param.DARK_GREY,
                         (col*param.CELL_SIZE,
                          row*param.CELL_SIZE,
                          param.CELL_SIZE,
                          param.CELL_SIZE),
                         border_top_right_radius=5)
    else:
        row: int = index_row + param.EDGE_OFFSET
        col: int = index_col + param.EDGE_OFFSET
        pygame.draw.rect(screen, param.DARK_GREY,
                         (col*param.CELL_SIZE,
                          row*param.CELL_SIZE,
                          param.CELL_SIZE,
                          param.CELL_SIZE))
     
def draw_board(screen: pygame.Surface, board: environ.Board) -> None:
    '''function to draw Wall, space, green/red apple'''
    for index_row, _ in enumerate(board.board):
        for index_col, col in enumerate(board.board[index_row]):
            if col == param.State.WALL.value:
                draw_wall(screen, board, index_row, index_col)
            elif col == param.State.G_APPLE.value:
                pygame.draw.rect(screen, param.GREEN,
                                 ((index_col + param.EDGE_OFFSET)*param.CELL_SIZE,
                                  (index_row + param.EDGE_OFFSET)*param.CELL_SIZE,
                                  param.CELL_SIZE,
                                  param.CELL_SIZE),
                                 border_radius=5)
            elif col == param.State.R_APPLE.value:
                pygame.draw.rect(screen, param.RED,
                                 ((index_col + param.EDGE_OFFSET)*param.CELL_SIZE,
                                  (index_row + param.EDGE_OFFSET)*param.CELL_SIZE,
                                  param.CELL_SIZE,
                                  param.CELL_SIZE),
                                 border_radius=5)

def draw_snake(screen: pygame.Surface, snake:list) -> None:
    '''draw snake'''
    for index_snake, snake in enumerate(snake):
        if index_snake == 0:
            pygame.draw.rect(screen, param.DARK_BLUE,
                             ((snake[1] + param.EDGE_OFFSET)*param.CELL_SIZE,
                              (snake[0] + param.EDGE_OFFSET)*param.CELL_SIZE,
                               param.CELL_SIZE,
                               param.CELL_SIZE),
                             border_radius=5)
        else:
            pygame.draw.rect(screen, param.BLUE,
                             ((snake[1] + param.EDGE_OFFSET)*param.CELL_SIZE,
                              (snake[0] + param.EDGE_OFFSET)*param.CELL_SIZE,
                               param.CELL_SIZE,
                               param.CELL_SIZE),
                             border_radius=5)

                
           
def event_handler() -> bool:
    '''pygame event handler'''
    for event in pygame.event.get():
        # if window is closed
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True



def init_gui(board: environ.Board):
    '''function to init and run pygame loop'''
    pygame.init()
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    pixel_size: int = board.size * param.CELL_SIZE
    
    screen: pygame.Surface = pygame.display.\
        set_mode(size=(pixel_size + (param.CELL_SIZE * param.SIDE_OFFSET),
                       pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2)),
                 flags=pygame.RESIZABLE)
    pygame.display.set_caption("Snake Game")
    running: bool = True
    while running:
        screen.fill(param.GREY)
        running = event_handler()
        
        draw_board(screen, board)
        draw_snake(screen, board.snake)
        pygame.display.flip()

    # explicitly clean up resources once loop ends (ie close window)
    pygame.quit()
