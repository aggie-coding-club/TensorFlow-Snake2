"""
description of game.py


"""
import numpy.random
from Part import Part
from Types import CardinalDirections, RelativeDirections, GameBlock
from SnakeLL import SnakeLL
import numpy as np
import time


class InvalidMove(Exception):
    pass


class Win(Exception):
    pass


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
                self.board[ix, iy] = Part(ix, iy, GameBlock.Blank)

        # place the first snake block at a random location
        snake_x = numpy.random.randint(0, self.x)
        snake_y = numpy.random.randint(0, self.y)

        snake_part = self.board[snake_x][snake_y]
        snake_part.part_type = GameBlock.Snake
        self.snake.insert_front(snake_part)

        # create an apple at a random spoooky spot
        blank_spaces = x * y - self.snake.length
        nth_blank = numpy.random.randint(0, blank_spaces) + 1
        for ix in range(x):
            for iy in range(y):
                if self.board[ix][iy].part_type == GameBlock.Blank:
                    nth_blank -= 1
                if nth_blank == 0:
                    # this is apple
                    self.apple = self.board[ix][iy]
                    self.apple.part_type = GameBlock.Apple

    def move(self, direction):
        assert isinstance(direction, RelativeDirections), "Was expecting RelativeDirections type, got: {}" \
            .format(direction.__class__.__name__)
        self.snake.turn(direction)
        x, y = self.snake.get_front_coords()

        # verify coordinates are valid
        if x < 0 or y < 0 or x >= self.x or y >= self.y:
            raise InvalidMove()  # you've gone off the board

        if self.board[x, y].part_type == GameBlock.Snake:
            raise InvalidMove()  # you've hit yourself

        touched_apple = self.board[x, y].part_type == GameBlock.Apple
        if self.snake.length == self.x * self.y - 1 and touched_apple:
            raise Win()

        self.board[x, y].part_type = GameBlock.Snake
        self.snake.insert_front(self.board[x, y])

        if not touched_apple:
            self.snake.drop_back()

    def __str__(self):
        padding = 4

        def pad(in_str, tl=4):
            for _ in range(tl - len(in_str)):
                in_str += " "
            return in_str

        output = ""
        for iy in range(self.y - 1, -1, -1):
            output += pad(str(iy), padding)
            for ix in range(self.x):  # x=0 => max x
                output += str(self.board[ix, iy]) + " "
            output += "\n"

        num_digs = len(str(self.x))
        for i in range(num_digs):
            output += " " * padding
            for j in range(self.x):
                output += pad(str(j), num_digs)[i] + " " * (2 if j % 2 == 0 else 1)
            output += "\n"
        return output


if __name__ == "__main__":
    my_game = Game(13, 11)
    print(my_game)
