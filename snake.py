'''main script to train and run model simulation with optional GUI implementation'''

import argparse
import pygame
import param
import environ
import gui

def define_args() -> argparse.Namespace:
    """define arguments in command line"""
    parser = argparse.ArgumentParser(
        description="A reinforcement learning script for the training and\
        simulation of a snake game.",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--visual",
                        type=str, help=(
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
    return parser.parse_args()




def main():
    '''main function to run program'''
    # initialize variables to store program metrics
    metric:dict = {
        "max_length": 3,
        "max_duration": 0,
        "curr_length": 3,
        "curr_duration": 0,
        "session": 1,
        "speed": 1
    }

    args: argparse.Namespace = define_args()
    if (args.boardsize < 5):
        print("Board size too small. Minimum = 5 grid")
        return
    board: environ.Board = environ.Board(size=args.boardsize)
    if args.visual == 'on':
        gui.init_gui(board, args, metric)





if __name__ == '__main__':
    main()

