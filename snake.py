'''main script to train and run model simulation'''
import argparse
import pygame
import util_function
import param


def init_gui():
    '''function to init pygame loop'''
    pygame.init()
    screen:pygame.Surface = pygame.display.\
        set_mode(size=(param.SCREEN_WIDTH, param.SCREEN_HEIGHT), flags=pygame.RESIZABLE)
    while True:
        pygame.display.flip()


def main():
    '''main function'''
    # init_gui()
    args:argparse.Namespace = util_function.define_args()


if __name__ == '__main__':
    main()

