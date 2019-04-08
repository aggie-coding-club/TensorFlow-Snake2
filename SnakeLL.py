"""
Linkedlist for Snake parts list, since we want to insert at the front
"""

from Part import Part

class SnakeLL:
    def __init__(self):
        self.ll = []
        self.front = None
        self.back = None
        self.length = 0
    def insert_front(self, obj):
        self.ll = [obj,self.ll]
        self.length += 1
        self.front = obj
    def drop_back(self):
        raise NotImplementedError()
