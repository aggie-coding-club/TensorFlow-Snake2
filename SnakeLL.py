"""
Linkedlist for Snake parts list, since we want to insert at the front
"""

from Part import Part, GameBlock
from Types import CardinalDirections, RelativeDirections


class SnakeLL:
    def __init__(self):
        self.front = None
        self.back = None
        self.length = 0
        self.direction = CardinalDirections.WEST  # game starts always facing west

    def insert_front(self, obj):
        """
        insert a Part to the front of the linked list
        :param obj: a Part
        :return: nothing
        """
        assert isinstance(obj, Part), "Invalid obj type"
        assert obj.part_type == GameBlock.Snake, "You did not insert a snake part"
        # self.ll = [obj, self.ll]
        self.length += 1
        if self.length == 1:
            self.front = obj
            self.back = obj
            obj.pnt_prev = None
            obj.pnt_next = None
        else:
            obj.pnt_next = self.front
            self.front.pnt_prev = obj
            self.front = obj

    def drop_back(self):
        """
        delete the last Part from the back of the linked list
        :return: nothing
        """
        assert self.length >= 1, "you tried to delete from an empty linked list"
        # remList = self.ll

        self.length -= 1
        if self.length > 1:
            self.back.part_type = GameBlock.Blank
            self.back = self.back.pnt_prev
            self.back.pnt_next.pnt_prev = None
            self.back.pnt_next = None
        if self.length is 1:
            self.front = None
            self.back = None
    
    def get_direction(self):
        """
        Get which direction you're facing (North, South, East, West)

        :return: CardinalDirection enum
        """
        return self.direction
    
    def turn(self, turn_dir):
        """
        Change current direction (North, South, East, West) based on input Left, Forward, Right

        :param turn_dir: RelativeDirections => Left, Forward, Right
        :return: void
        """
        assert isinstance(turn_dir, RelativeDirections), "Was expecting RelativeDirections type, got: {}"\
            .format(turn_dir.__class__.__name__)

        # direction values are positive = clockwise
        # so a change of -1, 0, or 1 would do the thing
        self.direction = CardinalDirections((self.direction.value + turn_dir.value) % 4)

    def get_front_coords(self):
        offset = {
            CardinalDirections.NORTH: (0, 1),
            CardinalDirections.EAST: (1, 0),
            CardinalDirections.SOUTH: (0, -1),
            CardinalDirections.WEST: (-1, 0)
        }[self.direction]

        # offset will be a tuple (X, X), based on what self.direction is

        new_x = self.front.x + offset[0]
        new_y = self.front.y + offset[1]

        return new_x, new_y

