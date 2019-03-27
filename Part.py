"""
description of part.py

part_type = 0 is blank space
part_type = 1 is snake part
part_type = 2 is apple
"""


class Part:
    """
    description of part class
    """
    def __init__(self, x, y, part_type):
        """
        description of our constructor
        """
        self.x = x
        self.y = y
        self.part_type = part_type
    def __str__(self):
        return '[%s: (%s,%s)]' % (self.part_type,self.x,self.y)
    raise NotImplementedError()
