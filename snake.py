

class GameState:
    def __init__(self, size_x=15, size_y=15, start_x=10, start_y=10):
        """
        Constructor for the state of the board object. Current values are arbitrary!
        Inputs:
            size_x <int>: x component size of the board
            size_y <int>: y component size of the board
            start_x <int>: x component head position
            start_y <int>: y component head position
        """
        self.size_x = size_x
        self.size_y = size_y
        self.start_x = start_x
        self.start_y = start_y
    

class Snake:
    def __init__(self, body_position):
        """
        Constructor for the snake's position data
        Inputs:
            body_position <nx2 ndarray of ints>: position of body.
                First pair should always be (0,0)
                Ex. [[0,0],[x1,y1],[x2,y2],...,[xn,yn]]
        """
        self.body_position = body_position
    
    def detect_selfcollision(self):
        """
        Attempts to detect if the snake it colliding with itself
        """
        raise NotImplementedError()