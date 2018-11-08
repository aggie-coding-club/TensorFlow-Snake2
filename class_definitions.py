import numpy as np
import enum

# __init__ functions are basically constructors
#
# __str__ functions are basically the python equivalent of java toString() functions
#

class GameOver(Exception):
    """Exception thrown to end the game. Efficiency is okay for now.
    Meaning: you lose"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class HailVictory(Exception):
    """Exception thrown to end the game. Efficiency is okay for now.
    Meaning: you win"""
    def __init__(self):
        super().__init__("You Win!")

class BoardObject:
    """Abstract class that all things that go on the board belong to"""
    def __init__(self):
        raise NotImplementedError

class Nothing(BoardObject):
    """A blank block"""
    def __init__(self):
        pass
    def __str__(self):
        return "🗆"

class Snake(BoardObject):
    """A snake block"""
    def __init__(self, id=0):
        """
        input id <int> 0-head, 1-first part, 2-second part, etc etc
        """
        self.id = id
    def __str__(self):
        #return str(self.id) #for debugging
        if self.id == 0:
            return "🚈"
        else:
            return "🚃"

class Apple(BoardObject):
    """An apple block"""
    def __init__(self):
        pass
    def __str__(self):
        return "🍎"

class Solver():
    """Abstract base class all solvers belong to."""
    def __init__(self):
        raise NotImplementedError()
    def solve(self):
        raise NotImplementedError()

class Direction(enum.Enum):
    """valid directions fed into BoardState::move()"""
    UP = [0,1]
    RIGHT = [1,0]
    DOWN = [0,-1]
    LEFT = [-1,0]
    NONE = [0, 0]

class BoardState:
    """A board which move operations can be applied to.
    
    Internal variables:
    x - size of board (x constraint)
    y - size of board (y constraint)
    internal_map - list of lists of BoardObjects
    snakeblocks - list of tuples, each tuple is a coordinate of a snake block.
        the first tuple is the head, the second is the first part, etc
    
    Internal methods:
    activate_apple() <private pls> - generates an apple on a blank space
        <private> -> no need to call this method externally.
            -> you can, which may have unintended results, but you don't have to.
    move(Direction) - attempts to move snake in given direction"""
    def __init__(self, x=10, y=10):
        """the constructor
        input x <int> - size of board x
        input y <int> - size of board y"""
        self.x = x #size in x of board
        self.y = y #size in y
        self.internal_map = [[Nothing() for _ in range(y)] for _ in range(x)] #fill board with Nothing
        self.internal_map[x//2][y//2] = Snake(id=0) #put snake in middle
        self.snakeblocks = [(x//2, y//2)] #list of snake parts
        self.activate_apple()
    def __str__(self):
        """print out board"""
        out = ""
        for iy in range(self.y-1,-1,-1):
            out += (str(iy) + "\t[")
            for ix in range(self.x):
                try:
                    out += " " + self.internal_map[ix][iy].__str__()
                except Exception as ex:
                    print(ix, iy, self.x, self.y)
                    raise ex
            out += "]\n"
        out += " \t  "
        for ix in range(self.x):
            out += (str(ix) + " ")
        out += "\n"
        return out
    def activate_apple(self):
        """generates apple in empty space"""
        empty_indices = []
        for ix in range(self.x):
            for iy in range(self.y):
                if self.internal_map[ix][iy].__class__.__name__ == "Nothing":
                    empty_indices.append([ix, iy])
        chosen_coords = empty_indices[np.random.randint(len(empty_indices))]
        self.internal_map[chosen_coords[0]][chosen_coords[1]] = Apple()
    def move(self, input):
        """moves the snake in direction
        input <Direction> - direction snake moves in
        """
        assert input.__class__.__name__ == "Direction", "Unrecognized input"
        new_x = self.snakeblocks[0][0] + input.value[0]
        new_y = self.snakeblocks[0][1] + input.value[1]
        last_x = self.snakeblocks[-1][0]
        last_y = self.snakeblocks[-1][1]
        if new_x >= self.x or new_y >= self.y or new_x < 0 or new_y < 0:
            raise GameOver("You went off the map!")
        if self.internal_map[new_x][new_y].__class__.__name__ == "Nothing":
            for i in range(len(self.snakeblocks)-1, 0,-1):
                self.snakeblocks[i] = self.snakeblocks[i-1]
            self.snakeblocks[0] = (new_x,new_y)
        if self.internal_map[new_x][new_y].__class__.__name__ == "Apple":
            self.snakeblocks = [(new_x, new_y)] + self.snakeblocks
            last_x = None
            last_y = None
            if len(self.snakeblocks) == self.x*self.y:
                raise HailVictory()
            self.activate_apple()
        if self.internal_map[new_x][new_y].__class__.__name__ == "Snake" and [new_x,new_y] != self.snakeblocks[-1]:
            raise GameOver("You hit yourself!")
        if last_x is not None and last_y is not None:
            self.internal_map[last_x][last_y] = Nothing()
        for idx, i in enumerate(self.snakeblocks):
            self.internal_map[i[0]][i[1]] = Snake(id=idx)


class FixedPathSolver(Solver):
    """Solver that attempts to complete by having the snake follow a fixed path"""
    def __init__(self, bs):
        self.board = bs
        self.path = self.generate_path(self.board.x, self.board.y)
        print(self.print_path())

    def solve(self, apply=True):
        moves = [Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT]
        my_dir = moves[np.random.randint(4)]
        if apply:
            self.board.move(my_dir)
        return my_dir

    def generate_path(self, x, y):
        """generates a path

        Inputs
        t_max <2-tuple> - contains maximum size of board (x_max_size, y_max_size)

        Outputs
        list of list of Directions"""

        #IFF = If and only if (logical biconditional)
        #The board has a solution IFF the board can be tiled
        #The board can be tiled IFF the board is not i x j such that i and j are odd numbers
        if x%2==1 and y%2==1:
            raise Exception("No solution exists")

        output = [[Direction.NONE for _ in range(y)] for _ in range(x)]
        
        #algo: go down the even end then wrap along other axis
        if y%2==0:
            #left edge
            for i in range(1,y):
                output[0][i] = Direction.DOWN
            #top edge
            for i in range(1,x):
                output[i][y-1] = Direction.LEFT
            #bottom left
            output[0][0] = Direction.RIGHT
            # top and left edge is done
            
            #bottom up, every 2
            for iy in range(0,y-1,2):
                for ix in range(1,x-1):
                    output[ix][iy] = Direction.RIGHT
                output[x-1][iy] = Direction.UP

            #bottom+1 up, every 2
            for iy in range(1,y-1,2):
                for ix in range(1,x):
                    output[ix][iy] = Direction.LEFT
                output[1][iy] = Direction.UP

        if x%2==0: ###WIP!
            #top edge
            for i in range(1,y):
                output[i][0] = Direction.LEFT
            #top edge
            for i in range(1,x):
                output[i][y-1] = Direction.LEFT
            #bottom left
            output[0][0] = Direction.RIGHT
            # top and left edge is done
            
            #bottom up, every 2
            for iy in range(0,y-1,2):
                for ix in range(1,x-1):
                    output[ix][iy] = Direction.RIGHT
                output[x-1][iy] = Direction.UP

            #bottom+1 up, every 2
            for iy in range(1,y-1,2):
                for ix in range(1,x):
                    output[ix][iy] = Direction.LEFT
                output[1][iy] = Direction.UP

        return output

    def print_path(self):
        """print out path"""
        x = self.board.x
        y = self.board.y
        out = ""
        for iy in range(y-1,-1,-1):
            out += (str(iy) + "\t[")
            for ix in range(x):
                try:
                    out += " "
                    if(self.path[ix][iy]==Direction.UP):
                        out += "U"
                    if(self.path[ix][iy]==Direction.DOWN):
                        out += "D"
                    if(self.path[ix][iy]==Direction.LEFT):
                        out += "L"
                    if(self.path[ix][iy]==Direction.RIGHT):
                        out += "R"
                    if(self.path[ix][iy]==Direction.NONE):
                        out += "N"
                except Exception as ex:
                    print(ix, iy, x, y)
                    raise ex
            out += "]\n"
        out += " \t  "
        for ix in range(x):
            out += (str(ix) + " ")
        out += "\n"
        return out
            


class RandomSolver(Solver):
    """Solver that attempts to complete by having the snake follow a fixed path"""
    def __init__(self, bs):
        self.board = bs

    def solve(self, apply=True):
        moves = [Direction.UP, Direction.DOWN, Direction.RIGHT, Direction.LEFT]
        my_dir = moves[np.random.randint(4)]
        if apply:
            self.board.move(my_dir)
        return my_dir