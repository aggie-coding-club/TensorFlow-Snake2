"""
Linkedlist for Snake parts list, since we want to insert at the front
"""

from Part import Part

class SnakeLL:
    def __init__(self):
        self.front = None
        self.back = None
        self.length = 0

    def insert_front(self, obj):
        """
        insert a Part to the front of the linked list
        :param obj: a Part
        :return: nothing
        """
        assert isinstance(obj, Part), "Invalid obj type"
        assert obj.part_type is 1, "You did not insert a snake part"
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
            self.back = self.back.pnt_prev
            self.back.pnt_next.pnt_prev = None
            self.back.pnt_next = None
        if self.length is 1:
            self.front = None
            self.back = None
