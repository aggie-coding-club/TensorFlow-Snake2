"""
description of game.py


"""
import numpy as np
import numpy.random
from Part import Part
from SnakeLL import SnakeLL
import numpy as np


class Game:
    """
    the state of the game
    """
    def __init__(self, x, y):
        """
        remember to transpose board if printing**

        :param x: how wide the board is
        :param y: how high the board is
        """
        # create variables
        self.x = x
        self.y = y
        self.board = np.zeros((x, y), dtype=object)  # list of list of Parts
        self.snake = SnakeLL()
        self.apple = None  # a Part

        # create the board of empty Parts
        for ix in range(x):  # for (int i=0; i<x; ++i) {} //c++
            for iy in range(y):
                self.board[ix, iy] = Part(ix, iy, 0)

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
        output = ""
        for iy in range(self.y - 1, -1, -1):
            for ix in range(self.x):  # x=0 => max x
                output += str(self.board[iy, ix])
            output += "\n"
        return output





if __name__ == "__main__":
    mygame = Game(30, 30)
    print(mygame)
