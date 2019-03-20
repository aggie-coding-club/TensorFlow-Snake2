"""
description of part.py


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
        return '[' + self.part_type + ': (' + self.x + ',' + self.y + ')]'
    raise NotImplementedError()
