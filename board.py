'''board / environment class with attributes and methods'''

import random
import 

class Board():
    '''The environment will determine the predefined rules as per subject.pdf
    and pass states to agent.
    '''
    def __init__(self, size:int = 10, speed: int = 1):
        self._size:int = size
        self._speed:int = speed
        self._board:list = []

        self.init_board(size) 
    
    def init_board(size:int)->None:
        '''set values for 2D array which represent board'''
        for i in range(size):
            row:list = []
            for j in range(size):
                if i == 0 and j == 0:
                    row.append()
        
    
    def move(action:str) -> 
        