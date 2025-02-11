'''functions to run pygame GUI'''

import time
import argparse
import pygame
import environ
import agent
import param

# global variable to keep track of height of sidebar items, hence can render
# items dynamically
height_pixel: int = 0

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
    global height_pixel
    for index_row, _ in enumerate(board.board):
        for index_col, col in enumerate(board.board[index_row]):
            if col == param.State.WALL.value:
                draw_wall(screen, board, index_row, index_col)
            # elif col == param.State.SPACE.value:
            #     pygame.draw.rect(screen, param.BLACK,
            #                      ((index_col + param.EDGE_OFFSET)
            #                       * param.CELL_SIZE,
            #                       (index_row + param.EDGE_OFFSET)
            #                       * param.CELL_SIZE,
            #                       param.CELL_SIZE,
            #                       param.CELL_SIZE)
            #                      )
            elif col == param.State.G_APPLE.value:
                pygame.draw.rect(screen, param.GREEN,
                                 ((index_col + param.EDGE_OFFSET)
                                  * param.CELL_SIZE,
                                  (index_row + param.EDGE_OFFSET)
                                  * param.CELL_SIZE,
                                  param.CELL_SIZE,
                                  param.CELL_SIZE),
                                 border_radius=5)
            elif col == param.State.R_APPLE.value:
                pygame.draw.rect(screen, param.RED,
                                 ((index_col + param.EDGE_OFFSET)
                                  * param.CELL_SIZE,
                                  (index_row + param.EDGE_OFFSET)
                                  * param.CELL_SIZE,
                                  param.CELL_SIZE,
                                  param.CELL_SIZE),
                                 border_radius=5)
    height_pixel += param.EDGE_OFFSET * param.CELL_SIZE

def draw_snake(screen: pygame.Surface, snake: list) -> None:
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


def event_handler(board: environ.Board, buttons:tuple, metric:dict) -> bool:
    '''pygame event handler'''
    for event in pygame.event.get():
        # if window is closed
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # step_button
            if buttons[0] is not None and buttons[0].collidepoint(event.pos):
                print("Button[0] Clicked!")
            elif buttons[1].collidepoint(event.pos):
                if metric['Speed'] < 10:
                    metric['Speed'] += 1
            elif buttons[2].collidepoint(event.pos):
                if metric['Speed'] > 1:
                    metric['Speed'] -= 1
    return True

def draw_metric(screen: pygame.Surface, metric: dict,
                pixel_size: int, agent_s: agent.Snake_Agent,
                dontlearn: bool) -> None:
    '''render metrics and interface into gui'''
    global height_pixel
    # draw header SESSION METRICS
    font = pygame.font.Font(None, param.HEADER_SIZE)
    header = font.render("Session", True, param.BLUE)
    header_rect = header.get_rect(
        topleft=(pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2),
                 height_pixel + param.PADDING))
    screen.blit(header, header_rect)
    # draw header AGENT METRICS
    header_agent = font.render("Agent", True, param.BLUE)
    header_rect_agent = header.get_rect(
        topleft=(pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2) +
                 param.AGENT_OFFSET,
                 height_pixel + param.PADDING))
    screen.blit(header_agent, header_rect_agent)
    height_pixel += param.HEADER_SIZE
    height_pixel += param.PADDING
    # draw other SESSION metrics
    for index, (key, value) in enumerate(metric.items()):
        if key != "Length" and key != "Duration":
            font = pygame.font.Font(None, param.TEXT_SIZE)
            text = font.render(f"{key} : {value}", True, param.ORANGE)
            rect = text.get_rect(topleft=(
                pixel_size + (param.CELL_SIZE
                            * param.EDGE_OFFSET * 2),
                height_pixel))
            screen.blit(text, rect)
            if index == 0:
                text = font.render(
                    f"Sessions trained : {agent_s.session}",
                    True, param.ORANGE)
                rect = text.get_rect(topleft=(
                    pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2) +
                    param.AGENT_OFFSET,
                    height_pixel))
                screen.blit(text, rect)
            if index == 1:
                text = font.render(
                    f"Duration trained : {agent_s.steps}",
                    True, param.ORANGE)
                rect = text.get_rect(topleft=(
                    pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2) +
                    param.AGENT_OFFSET,
                    height_pixel))
                screen.blit(text, rect)
            if index == 4:
                text = font.render(
                    f"Main network train : {agent_s.training}",
                    True, param.ORANGE)
                rect = text.get_rect(topleft=(
                    pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2) +
                    param.AGENT_OFFSET,
                    height_pixel))
                screen.blit(text, rect)
            if index == 5:
                text = font.render(
                    f"Network transfer : {agent_s.transfer_weight}",
                    True, param.ORANGE)
                rect = text.get_rect(topleft=(
                    pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2) +
                    param.AGENT_OFFSET,
                    height_pixel))
                screen.blit(text, rect)
            if index == 6 and dontlearn is True:
                text = font.render(
                    "AGENT NOT LEARNING",
                    True, param.RED)
                rect = text.get_rect(topleft=(
                    pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2) +
                    param.AGENT_OFFSET,
                    height_pixel))
                screen.blit(text, rect)

            height_pixel += param.TEXT_SIZE
    # render current session length and duration inside snake game borders 
    font = pygame.font.Font(None, param.TEXT_SIZE - 5)
    text = font.render(f"Length: {metric["Length"]}", True, param.ORANGE)
    rect = text.get_rect(topright=(
            pixel_size,
            param.CELL_SIZE * 2))
    screen.blit(text, rect)
    text = font.render(f"Duration: {metric["Duration"]}", True, param.ORANGE)
    rect = text.get_rect(topright=(
            pixel_size,
            (param.CELL_SIZE * 2) + param.TEXT_SIZE - 5))
    screen.blit(text, rect) 
      

def draw_console(screen: pygame.Surface, args: argparse.Namespace,
                 pixel_size: int):
    '''draw buttons for interactions'''
    global height_pixel
    # draw header
    font = pygame.font.Font(None, param.HEADER_SIZE)
    header = font.render("Console", True, param.BLUE)
    header_rect = header.get_rect(
        topleft=(pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2),
                 height_pixel))
    height_pixel += param.HEADER_SIZE
    screen.blit(header, header_rect)
    # render buttons
    step_button = None
    up_button = pygame.Rect(pixel_size
                            + (param.CELL_SIZE *
                               param.EDGE_OFFSET * 2),
                            height_pixel,
                            param.BUTTON_WIDTH, param.BUTTON_HEIGHT)
    pygame.draw.rect(screen, param.ORANGE, up_button, border_radius=5)
    font = pygame.font.Font(None, param.TEXT_SIZE)
    up_font = font.render("Speed UP", True, param.DARK_BLUE)
    up_font_rect = up_font.get_rect(
        topleft=(pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2)
                 + param.BUTTON_PADDING,
                 height_pixel + param.BUTTON_PADDING))
    screen.blit(up_font, up_font_rect)

    down_button = pygame.Rect(pixel_size +
                              (param.CELL_SIZE *
                               param.EDGE_OFFSET * 2) +
                              param.BUTTON_WIDTH + param.BUTTON_PADDING,
                              height_pixel,
                              param.BUTTON_WIDTH, param.BUTTON_HEIGHT)
    pygame.draw.rect(screen, param.ORANGE, down_button, border_radius=5)
    font = pygame.font.Font(None, param.TEXT_SIZE)
    down_font = font.render("Slow DOWN", True, param.DARK_BLUE)
    down_font_rect = down_font.get_rect(
        topleft=(pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2)
                 + (param.BUTTON_PADDING * 2) + param.BUTTON_WIDTH,
                 height_pixel + param.BUTTON_PADDING))
    height_pixel += param.BUTTON_HEIGHT
    height_pixel += param.BUTTON_PADDING
    screen.blit(down_font, down_font_rect)

    if args.step_by_step is True:
        step_button = pygame.Rect(pixel_size +
                                  (param.CELL_SIZE *
                                   param.EDGE_OFFSET * 2),
                                  height_pixel + param.BUTTON_PADDING,
                                  param.BUTTON_WIDTH, param.BUTTON_HEIGHT) 
        pygame.draw.rect(screen, param.GREEN, step_button, border_radius=5)
        font = pygame.font.Font(None, param.TEXT_SIZE)
        step_font = font.render("NEXT STEP", True, param.DARK_BLUE)
        step_font_rect = step_font.get_rect(
            topleft=(pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2)
                     + param.BUTTON_PADDING,
                     height_pixel + (param.BUTTON_PADDING * 2)))
        height_pixel += param.BUTTON_HEIGHT
        height_pixel += param.BUTTON_PADDING
        screen.blit(step_font, step_font_rect)
    return (step_button, up_button, down_button)


def run_game(board: environ.Board, agent_s: agent.Snake_Agent,
             metric: dict, args: argparse.Namespace) -> None:
    board.get_initial_state()




def init_gui(board: environ.Board, args: argparse.Namespace, metric: dict,
             agent_s: agent.Snake_Agent):
    '''function to init and run pygame loop'''
    global height_pixel
    pygame.init()
    pygame.display.set_caption("SNAKE GAME")
    pixel_size: int = board.size * param.CELL_SIZE
    screen: pygame.Surface = pygame.display.\
        set_mode(size=(pixel_size + (param.CELL_SIZE * param.SIDE_OFFSET),
                       pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2)),
                 flags=pygame.RESIZABLE)
    running: bool = True
    while running:
        screen.fill(param.BLACK)
        draw_board(screen, board)
        draw_snake(screen, board.snake)
        buttons = draw_console(screen, args, pixel_size)
        draw_metric(screen, metric, pixel_size, agent_s, args.dontlearn)
        running = event_handler(board, buttons, metric)
        pygame.display.flip()
        if args.step_by_step is False:
            time.sleep(1)
            run_game(board, agent_s, metric)
        height_pixel = 0
    # explicitly clean up resources once loop ends (ie close window)
    pygame.quit()
