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
        if self.length == 1:
            self.back = obj
    def drop_back(self):
        remList = self.ll
        back = None
        while remList[1]:
            back = remList[0]
            remList = remList[1]
        self.back = back
        remList.clear()
        self.length -= 1
        if not self.ll:
            self.front = None
