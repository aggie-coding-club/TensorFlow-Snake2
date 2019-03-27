"""
description of part.py

part_type = 0 is blank space
part_type = 1 is snake part
part_type = 2 is apple
"""


class Part:
    """
    description of part class
    defines how each part works
    x,y are the row and column values of the part's position
    part_type defines if it is a blank space, snake part, or an apple
    __str__ makes the location and part type string values

    Essentially a struct
    """
    def __init__(self, x, y, part_type=0):
        """
        description of our constructor
        """
        self.x = x
        self.y = y
        self.part_type = part_type

        # specificly for the snake list
        self.pnt_next = None
        self.pnt_prev = None
    def __str__(self):
        return '[%s: (%s,%s)]' % (self.part_type,self.x,self.y)
