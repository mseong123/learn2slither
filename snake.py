'''main script to train and run model simulation with optional GUI implementation'''

import argparse
import os
import pickle
import pygame
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

def get_metrics() -> dict:
    '''initialize variables to store program metrics'''
    metric: dict = {
        "Max Length": 3,
        "Max Duration": 0,
        "Length": 3,
        "Duration": 0,
        "Session": 0,
        "Total Session": 1,
        "Speed": 1
    }
    return metric

def main():
    '''main function to run program'''
    try:
        os.mkdir("./model")
    except FileExistsError:
        pass
    # ------------------------------------------------------
    # INITIALIZE ALL METRICS AND ARGUMENTS
    metric: dict = get_metrics()
    snake_agent: agent.Snake_Agent | None = None
    args: argparse.Namespace = define_args()
    board: environ.Board = environ.Board(size=args.boardsize)
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
    if args.load is None:
        # if no loading argument, create a new agent instance 
        snake_agent = agent.Snake_Agent()
    else:
        if os.path.exists(args.load):
            with open(args.load, "rb") as file:
                snake_agent = pickle.load(file)
            # set params in agent to dontlearn if arg is set
            if args.dontlearn is True:
                snake_agent.dontlearn = True
            else:
                snake_agent.dontlearn = False
        else:
            print("Problem loading model or model doesn't exist. Exiting")
            return
    # -----------------------------------------------------
    # if gui activated, board/agent/speed/training handled by GUI
    if args.visual == 'on':
        gui.init_gui(board, args, metric, snake_agent)
    # otherwise no cap on speed of session/training
    # else:
    #     for i in range(int(args.session)):




    
    
    





if __name__ == '__main__':
    main()

