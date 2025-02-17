'''functions to run pygame GUI'''

import time
import argparse
import pygame
import environ
import agent
import param
import snake

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



def event_handler(board: environ.Board, buttons: tuple,
                  metric: dict, snake_agent: agent.Snake_Agent,
                  dontlearn: bool) -> bool:
    '''pygame event handler'''
    for event in pygame.event.get():
        # if window is closed
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            elif event.key == pygame.K_RETURN:
                if metric["Session"] < metric["Total Session"]:
                    snake.run_game_gui(board, snake_agent, metric, dontlearn)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # step_button
            if buttons[0] is not None and buttons[0].collidepoint(event.pos):
                if metric["Session"] < metric["Total Session"]:
                    snake.run_game_gui(board, snake_agent, metric, dontlearn)
            elif buttons[1].collidepoint(event.pos):
                if metric['Speed'] < 10 and metric["Session"] <\
                    metric["Total Session"]:
                    metric['Speed'] += 1
                    param.LOOP["count"] = 0
            elif buttons[2].collidepoint(event.pos):
                if metric['Speed'] > 1 and metric["Session"] <\
                    metric["Total Session"]:
                    metric['Speed'] -= 1
                    param.LOOP["count"] = 0
    return True

def draw_metric(screen: pygame.Surface, metric: dict,
                pixel_size: int, snake_agent: agent.Snake_Agent,
                dontlearn: bool, board: environ.Board) -> None:
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
        if key != "Duration":
            font = pygame.font.Font(None, param.TEXT_SIZE)
            text = font.render(f"{key} : {value}", True, param.ORANGE)
            rect = text.get_rect(topleft=(
                pixel_size + (param.CELL_SIZE
                            * param.EDGE_OFFSET * 2),
                height_pixel))
            screen.blit(text, rect)
            # render the following agent metrics on same height as game metrics
            if index == 0:
                text = font.render(
                    f"Sessions : {snake_agent.session}",
                    True, param.ORANGE)
                rect = text.get_rect(topleft=(
                    pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2) +
                    param.AGENT_OFFSET,
                    height_pixel))
                screen.blit(text, rect)
            if index == 1:
                text = font.render(
                    f"Duration : {snake_agent.steps}",
                    True, param.ORANGE)
                rect = text.get_rect(topleft=(
                    pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2) +
                    param.AGENT_OFFSET,
                    height_pixel))
                screen.blit(text, rect)
            if index == 3:
                text = font.render(
                    f"Main network train : {snake_agent.training}",
                    True, param.ORANGE)
                rect = text.get_rect(topleft=(
                    pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2) +
                    param.AGENT_OFFSET,
                    height_pixel))
                screen.blit(text, rect)
            if index == 4:
                text = font.render(
                    f"Network transfer : {snake_agent.transfer_weight}",
                    True, param.ORANGE)
                rect = text.get_rect(topleft=(
                    pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2) +
                    param.AGENT_OFFSET,
                    height_pixel))
                screen.blit(text, rect)
            if index == 5 and dontlearn is True:
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
    text = font.render(f"Length: {len(board.snake)}", True, param.ORANGE)
    rect = text.get_rect(topright=(
            pixel_size,
            param.CELL_SIZE * 2))
    screen.blit(text, rect)
    text = font.render(f"Duration: {metric["Duration"]}", True, param.ORANGE)
    rect = text.get_rect(topright=(
            pixel_size,
            (param.CELL_SIZE * 2) + param.TEXT_SIZE - 5))
    screen.blit(text, rect)
    # render prev action for snake
    font = pygame.font.Font(None, param.TEXT_SIZE)
    if board.prev_action is not None:
        color = None
        result: str = None
        if board.prev_action == -2:
            result = "DIED"
            color = param.RED
        elif board.prev_action == -1:
            result = "ILLEGAL MOVE"
            color = param.RED
        else:
            result = param.Action(board.prev_action).name
            color = param.GREEN
        text = font.render(f"prev: {result}", True, color)
        rect = text.get_rect(topleft=(
            pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2),
            height_pixel))
        screen.blit(text, rect)
 
    # render exploration/exploitation metrics for agent
    text = font.render(
        f"ε: {snake_agent.e:.1f} r: {snake_agent.random_float:.1f}",
        True, param.GREEN)
    rect = text.get_rect(topleft=(
        pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2) +
        param.AGENT_OFFSET,
        height_pixel))
    screen.blit(text, rect)
    height_pixel += param.TEXT_SIZE

    # render current action for snake
    text = font.render(
        f"current: {param.Action(board.action).name}", True, param.GREEN)
    rect = text.get_rect(topleft=(
        pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2),
        height_pixel))
    screen.blit(text, rect)
    text = font.render(
        f"{"Exploration" if snake_agent.random_float < snake_agent.e
           else "Exploitation"}",
        True, param.GREEN)
    rect = text.get_rect(topleft=(
        pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2) +
        param.AGENT_OFFSET,
        height_pixel))
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

def draw_game_over(screen: pygame.Surface, pixel_size: int) -> None:
    '''draw Game Over screen'''
    font = pygame.font.Font(None, param.HEADER_SIZE * 2)
    game_over_font = font.render("GAME OVER", True, param.WHITE)
    game_over_font_rect = game_over_font.get_rect(
        center=((pixel_size + (param.CELL_SIZE * param.SIDE_OFFSET)) // 2,
                (pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2)) // 2)
    )
    screen.blit(game_over_font, game_over_font_rect)

def scale_image(image, screen_size):
    """Resize image to fit the screen."""
    return pygame.transform.scale(image, screen_size)

def draw_lobby(image, screen) -> None:
    '''draw lobby'''
    for event in pygame.event.get():
        # if window is closed
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            image = scale_image(image, screen.get_size())
    screen.blit(image, (0, 0))
    pygame.display.flip()
    return True
         


def init_gui(board: environ.Board, args: argparse.Namespace, metric: dict,
             snake_agent: agent.Snake_Agent):
    '''function to init and run pygame loop'''
    global height_pixel
    pygame.init()
    pygame.display.set_caption("SNAKE GAME")
    pixel_size: int = board.size * param.CELL_SIZE
    screen: pygame.Surface = pygame.display.\
        set_mode(size=(pixel_size + (param.CELL_SIZE * param.SIDE_OFFSET),
                       pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2)),
                 flags=pygame.RESIZABLE)
    lobby_image = pygame.image.load(param.LOGO_URL)
    lobby_image = scale_image(lobby_image, (
        pixel_size + (param.CELL_SIZE * param.SIDE_OFFSET),
        pixel_size + (param.CELL_SIZE * param.EDGE_OFFSET * 2))
        )
    running: bool = True
    while running:
        if board.lobby is True:
            running = draw_lobby(lobby_image, screen)
        else: 
            screen.fill(param.BLACK)
            draw_board(screen, board)
            draw_snake(screen, board.snake)
            buttons = draw_console(screen, args, pixel_size)
            draw_metric(screen, metric, pixel_size, snake_agent,
                        args.dontlearn, board)
            if metric["Session"] == metric["Total Session"]:
                draw_game_over(screen, pixel_size)
            running = event_handler(board, buttons, metric,
                                    snake_agent, args.dontlearn)
            if args.step_by_step is False and\
            metric["Session"] < metric["Total Session"]:
                param.LOOP["count"] += 1
                if param.LOOP["count"] ==\
                (param.LOOP["limit"] // metric["Speed"]):
                    snake.run_game_gui(board, snake_agent,
                                    metric, args.dontlearn)
                    param.LOOP["count"] = 0
            pygame.display.flip()
            height_pixel = 0
    # explicitly clean up resources once loop ends (ie close window)
    pygame.quit()
