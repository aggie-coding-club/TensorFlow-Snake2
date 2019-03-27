"""
description of game.py


"""
import numpy as np
import numpy.random
from Part import Part
from SnakeLL import SnakeLL

class Game:
    def __init__(self, x, y):
        # create variables
        self.x = x
        self.y = y
        self.board = [] # list of list of Parts
        self.snake = SnakeLL()
        self.apple = None # a Part

        # create the board of empty Parts
        for ix in range(x): #for (int i=0; i<x; ++i) {} //c++
            self.board.append([])
            for iy in range(y):
                self.board[ix].append(Part(ix, iy))

        # place the first snake block at a random location
        snake_x = numpy.random.randint(0,ix)
        snake_y = numpy.random.randint(0,iy)

        snake_part = self.board[snake_x][snake_y]
        snake_part.part_type = 1
        self.snake.insert_front(snake_part)

        # create an apple at a random spoooky spot
        blank_spaces = x * y - self.snake.length
        nth_blank = numpy.random.randint(0,blank_spaces)
        for ix in range(x):
            for iy in range(y):
                if self.board[ix][iy].part_type == 0:
                    nth_blank -= 1
                if nth_blank == 0:
                    #this is apple
                    self.apple = self.board[ix][iy]
                    self.apple.part_type = 2





#mygame = Game(5,5)
