'''utility functions'''
import argparse


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

