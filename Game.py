"""
description of game.py


"""
import numpy as np
import numpy.random
from Part import Part
from SnakeLL import SnakeLL

class Game:
    def __init__(self, x, y):
        """

        :param x: how wide the board is
        :param y: how high the board is
        """
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
        snake_x = numpy.random.randint(0, self.x)
        snake_y = numpy.random.randint(0, self.y)

        snake_part = self.board[snake_x][snake_y]
        snake_part.part_type = 1
        self.snake.insert_front(snake_part)

        # create an apple at a random spoooky spot
        blank_spaces = x * y - self.snake.length
        nth_blank = numpy.random.randint(0,blank_spaces) + 1
        for ix in range(x):
            for iy in range(y):
                if self.board[ix][iy].part_type == 0:
                    nth_blank -= 1
                if nth_blank == 0:
                    #this is apple
                    self.apple = self.board[ix][iy]
                    self.apple.part_type = 2

    def __str__(self):
        return "The board is %sx%s, the snake's head is at: %s, %s" % (self.x,
                                                                       self.y,
                                                                       self.snake.front.x,
                                                                       self.snake.front.y)




if __name__ == "__main__":
    mygame = Game(5, 5)
    print(mygame)
