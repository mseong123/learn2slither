'''functions to run pygame GUI'''

import pygame
import environ
import param


def draw_wall(screen: pygame.Surface, board: environ.Board,
              index_row: int, index_col: int) -> None:
    '''sub function to draw wall with border radius'''
    if index_col == 0 and index_row == 0:
        pygame.draw.rect(screen, param.DARK_GREY,
                         (index_col*param.CELL_SIZE,
                          index_row*param.CELL_SIZE,
                          param.CELL_SIZE,
                          param.CELL_SIZE),
                         border_top_left_radius=5)
    elif index_col == board.size - 1 and index_row == board.size - 1:
        pygame.draw.rect(screen, param.DARK_GREY,
                         (index_col*param.CELL_SIZE,
                          index_row*param.CELL_SIZE,
                          param.CELL_SIZE,
                          param.CELL_SIZE),
                         border_bottom_right_radius=5) 
    elif index_col == 0 and index_row == board.size - 1:
        pygame.draw.rect(screen, param.DARK_GREY,
                         (index_col*param.CELL_SIZE,
                          index_row*param.CELL_SIZE,
                          param.CELL_SIZE,
                          param.CELL_SIZE),
                         border_bottom_left_radius=5)
    elif index_col == board.size - 1 and index_row == 0:
        pygame.draw.rect(screen, param.DARK_GREY,
                         (index_col*param.CELL_SIZE,
                          index_row*param.CELL_SIZE,
                          param.CELL_SIZE,
                          param.CELL_SIZE),
                         border_top_right_radius=5)
    else:
        pygame.draw.rect(screen, param.DARK_GREY,
                         (index_col*param.CELL_SIZE,
                          index_row*param.CELL_SIZE,
                          param.CELL_SIZE,
                          param.CELL_SIZE))


         
                
                    
def draw_board(screen: pygame.Surface, board: environ.Board) -> None:
    '''function to draw Wall, space, green/red apple'''
    for index_row, row in enumerate(board.board):
        for index_col, col in enumerate(board.board[index_row]):
            if col == param.State.WALL.value:
                draw_wall(screen, board, index_row, index_col)
                
                
           



def init_gui(board: environ.Board):
    '''function to init and run pygame loop'''
    pygame.init()
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    pixel_size: int = board.size * param.CELL_SIZE
    
    screen: pygame.Surface = pygame.display.\
        set_mode(size=(pixel_size + (param.CELL_SIZE * 2),
                       pixel_size), flags=pygame.RESIZABLE)
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    running: bool = True
    while running:
        screen.fill(param.GREY)
        for event in pygame.event.get():
            # if window is closed
            if event.type == pygame.QUIT:
                running = False
        draw_board(screen, board)
        pygame.display.flip()

    # explicitly clean up resources once loop ends (ie close window)
    pygame.quit()
