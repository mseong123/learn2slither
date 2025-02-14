'''main script to train and run model simulation with optional GUI
implementation'''

import argparse
import os
import pickle
import param
import environ
import gui
import agent


def define_args() -> argparse.Namespace:
    """define arguments in command line"""
    parser = argparse.ArgumentParser(
        description="A reinforcement learning script for the training and\
        simulation of a snake game.",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--visual", type=str, help=(
        "enable GUI for snake game (on/off).")
    )
    parser.add_argument("--load", type=str, help=(
        "file path (relative to root folder) of model to load from.")
    )
    parser.add_argument("--save", type=str, help=(
        "file path (relative to root folder) to save model.")
    )
    parser.add_argument("--sessions", type=int, help=(
        "no. of snake game simulations to run.")
    )
    parser.add_argument("--dontlearn", action="store_true", help=(
        "flag to switch off learning."
    ))
    parser.add_argument("--step-by-step", action="store_true", help=(
        "flag to toggle step by step mode(space key)."
    ))
    parser.add_argument("--boardsize", default=10, type=int, help=(
        "board size (not including walls). Min size = 10\n"
        "default = 10 grid"
    ))
    parser.add_argument("--e", type=float, help=(
        f"epsilon value. Max size = 1. Min size = {param.MIN_E}\n"
    ))
    return parser.parse_args()

def get_metrics(args: argparse.Namespace) -> dict:
    '''initialize variables to store program metrics'''
    metric: dict = {
        "Max Length": 3,
        "Max Duration": 0,
        "Duration": 0,
        "Session": 0,
        "Total Session": args.sessions,
        "Speed": 1,
    }
    return metric

def reset_metrics(metric: dict, board: environ.Board) -> int:
    '''function to check max length of snake when session ends'''
    if board.final_length > metric["Max Length"]:
        metric["Max Length"] = board.final_length
    if metric["Duration"] > metric["Max Duration"]:
        metric["Max Duration"] = metric["Duration"]
    metric["Duration"] = 0
    metric["Session"] += 1

def run_game_gui(board: environ.Board, snake_agent: agent.Snake_Agent,
                  metric: dict, dontlearn: bool) -> None:
    '''function to run game step by step using GUI''' 
    if metric["Session"] == 0 and metric["Duration"] == 0:
        state = board.get_initial_state()
        action = snake_agent.action([state])
        # Since step by step, need to store persistent state somewhere
        param.BOARD_STATE["state"] = board.move(action)
        metric["Duration"] += 1
        if param.BOARD_STATE["state"][2] is True:
            # have to manually add session to snake_agent
            # not ideal but due to mismatch of timing of execution
            # of statements.
            if dontlearn is False:
                snake_agent.add_session(1)
            reset_metrics(metric, board)
        if metric["Session"] == metric["Total Session"]:
            print(f"Game Over, max length = {metric["Max Length"]}, \
            max duration = {metric["Max Duration"]}")
    else:
        action = snake_agent.action(param.BOARD_STATE["state"])
        param.BOARD_STATE["state"] = board.move(action)
        metric["Duration"] += 1
        if param.BOARD_STATE["state"][2] is True:
            if dontlearn is False:
                snake_agent.add_session(1)
            reset_metrics(metric, board)
        if metric["Session"] == metric["Total Session"]:
            print(f"Game Over, max length = {metric["Max Length"]}, \
            max duration = {metric["Max Duration"]}")
    


def run_game(board: environ.Board, snake_agent: agent.Snake_Agent,
             metric: dict, args: argparse.Namespace) -> None:
    '''function to run game between environ(board) and agents'''
    state: list = []
    action: int = 0
    while metric["Session"] <= metric["Total Session"]:
        if metric["Session"] == 0 and metric["Duration"] == 0:
            state = board.get_initial_state()
            action = snake_agent.action([state])
            state = board.move(action)
            metric["Duration"] += 1
            if state[2] is True:
                if args.dontlearn is False:
                    snake_agent.add_session(1)
                reset_metrics(metric, board)
        else:
            action = snake_agent.action(state)
            state = board.move(action)
            metric["Duration"] += 1
            if state[2] is True:
                if args.dontlearn is False:
                    snake_agent.add_session(1)
                reset_metrics(metric, board)
    print(f"Game Over, max length = {metric["Max Length"]},"
          f"max duration = {metric["Max Duration"]}")

def main():
    '''main function to run program'''
    try:
        os.mkdir("./model")
    except FileExistsError:
        pass
    # ------------------------------------------------------
    # INITIALIZE ALL METRICS AND ARGUMENTS
    snake_agent: agent.Snake_Agent | None = None
    args: argparse.Namespace = define_args()
    metric: dict = get_metrics(args)
    board: environ.Board = environ.Board(size=args.boardsize)
    # ------------------------------------------------------
    # ERROR CHECKING OF ARGUMENT COMBINATIONS
    # At minimum need grid size of 5 since subject.pdf snake have length of 3
    if args.boardsize < 5:
        print("Board size too small. Minimum = 5 grid")
        return
    # at minimum need to provide no. of sessions to run a program, all
    # other flags are optional
    if args.sessions is None:
        print("Please provide no. of sessions to run")
        return
    metric["Total Session"] = args.sessions
    # epsilon range
    if args.e is not None and (args.e > 1
                               or args.e < param.MIN_E):
        print(f"epsilon has to be <= 1 and >= {param.MIN_E}")
        return
    if args.dontlearn is True and args.save is not None:
        print("can't save model when dontlearn option is enabled")
        return
    # ------------------------------------------------------
    # INITIALIZE MODEL
    if args.load is None:
        # if no loading argument, create a new agent instance
        snake_agent = agent.Snake_Agent(decay_scale=param.DECAY_SCALE)
    else:
        if os.path.exists(args.load):
            with open(args.load, "rb") as file:
                snake_agent = pickle.load(file)
            print(f"Load trained model from {args.load}")
        else:
            print("Problem loading model or model doesn't exist. Exiting")
            return
    # set params in agent to dontlearn if arg is set
    if args.dontlearn is True:
        snake_agent.dontlearn = True
        snake_agent.prev_e = snake_agent.e
        snake_agent.e = 0
    else:
        snake_agent.dontlearn = False
        snake_agent.e = snake_agent.prev_e
    # can set epsilon manually ie if want to continue training on another board
    if args.e is not None:
        snake_agent.e = args.e
    # -----------------------------------------------------
    # GAMEPLAY
    # if GUI activated, board state appear on gui and speed of game/training
    # is human readable. If step_by_step activated, game controlled by console
    # in GUI
    if args.visual == 'on':
        board.gui = True
        gui.init_gui(board, args, metric, snake_agent)
        # if args.step_by_step is False:
        #     run_game(board, snake_agent, metric, args)
    # otherwise no cap on speed of session/training
    else:
        run_game(board, snake_agent, metric, args)
    if args.save is not None:
        for i in range(len(snake_agent.replay_buffer) - 1,
                       len(snake_agent.replay_buffer) - 10, -1):
            if len(snake_agent.replay_buffer[i]) != 5:
                del snake_agent.replay_buffer[i]
        with open(f"{args.save}", "wb") as file:
            pickle.dump(snake_agent, file)
        print(f"Save learning state in {args.save}")


if __name__ == '__main__':
    main()

