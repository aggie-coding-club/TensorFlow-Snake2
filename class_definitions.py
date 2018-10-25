import numpy as np
import enum

# __init__ functions are basically constructors
#
# __str__ functions are basically the python equivalent of java toString() functions
#

class GameOver(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class HailVictory(Exception):
    def __init__(self):
        super().__init__("You Win!")

class BoardObject:
    """abstract class that all things that go on the board belong to"""
    def __init__(self):
        raise NotImplementedError

class Nothing(BoardObject):
    def __init__(self):
        pass
    def __str__(self):
        return "🗆"

class Snake(BoardObject):
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
    def __init__(self):
        pass
    def __str__(self):
        return "🍎"

class Solver():
    def __init__(self):
        pass

class Direction(enum.Enum):
    UP = [-1,0]
    RIGHT = [0,1]
    DOWN = [1,0]
    LEFT = [0,-1]

class BoardState:
    """the stuff all the things are on"""
    def __init__(self, x=10, y=10):
        self.x = x
        self.y = y
        self.internal_map = [[Nothing() for _ in range(y)] for _ in range(x)]
        self.internal_map[x//2][y//2] = Snake(id=0)
        self.snakeblocks = [[x//2, y//2]]
        #test
        #self.internal_map[1][2] = Snake(id=0)
        #self.snakeblocks = [[1,2]]
        self.activate_apple()
    def __str__(self):
        out = ""
        for ix in range(self.x):
            out += "["
            for iy in range(self.y):
                out += " " + self.internal_map[ix][iy].__str__()
            out += "]\n"
        return out
    def activate_apple(self):
        empty_indices = []
        for ix in range(self.x):
            for iy in range(self.y):
                if self.internal_map[ix][iy].__class__.__name__ == "Nothing":
                    empty_indices.append([ix, iy])
        chosen_coords = empty_indices[np.random.randint(len(empty_indices))]
        self.internal_map[chosen_coords[0]][chosen_coords[1]] = Apple()
    def move(self, input):
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
            self.snakeblocks[0] = [new_x,new_y]
        if self.internal_map[new_x][new_y].__class__.__name__ == "Apple":
            self.snakeblocks = [[new_x, new_y]] + self.snakeblocks
            last_x = None
            last_y = None
            if len(self.snakeblocks) == self.x*self.y:
                raise HailVictory()
            self.activate_apple()
        if self.internal_map[new_x][new_y].__class__.__name__ == "Snake":
            raise GameOver("You hit yourself!")
        if last_x is not None and last_y is not None:
            self.internal_map[last_x][last_y] = Nothing()
        for idx, i in enumerate(self.snakeblocks):
            self.internal_map[i[0]][i[1]] = Snake(id=idx)