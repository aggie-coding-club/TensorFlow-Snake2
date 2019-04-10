"""
testing methods in SnakeLL

do some tests to make sure stuff works properly
"""

from Part import Part
from SnakeLL import SnakeLL

if __name__ == "__main__":
    sll = SnakeLL()
    assert sll.length is 0, "WRONG LENGTH!!! <initialize>"

    for _ in range(10):  # insert 10 snake parts into a snake linked list
        part = Part(0, 0, 1)
        sll.insert_front(part)
    assert sll.length is 10, "WRONG LENGTH!!! <insert front>"

    for _ in range(10):
        sll.drop_back()
    assert sll.length is 0, "WRONG LENGTH!!! <drop back> found: %s" % sll.length

    print("Test passed")
