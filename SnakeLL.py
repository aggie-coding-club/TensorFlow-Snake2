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
        raise NotImplementedError()
    def drop_back(self):
        raise NotImplementedError()
