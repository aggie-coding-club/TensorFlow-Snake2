"""
Testing the speed of SnakeLL

At iterations: 5000
Linked list time: 0.017 s
List time: 0.050 s
Linked lists are: 2.965 times faster than lists

At iterations: 10000
Linked list time: 0.033 s
List time: 0.183 s
Linked lists are: 5.498 times faster than lists

At iterations: 25000
Linked list time: 0.062 s
List time: 1.354 s
Linked lists are: 21.821 times faster than lists

At iterations: 100000
Linked list time: 0.167 s
List time: 27.989 s
Linked lists are: 167.941 times faster than lists

Conclusions:
    Linked lists are O(n)
    Lists are O(n^2)
    Not really performance benefits to linked lists until 2000 elements.

"""

from Part import Part
from SnakeLL import SnakeLL
import time

if __name__ == "__main__":
    for ITERATIONS in [5000, 10000, 25000, 100000]:
        sll = SnakeLL()
        ll_start_time = time.time()
        for _ in range(ITERATIONS):  # insert 10 snake parts into a snake linked list
            part = Part(0, 0, 1)
            sll.insert_front(part)
        for _ in range(ITERATIONS):
            sll.drop_back()
        ll_end_time = time.time()

        sll2 = []
        list_start_time = time.time()
        for _ in range(ITERATIONS):
            part = Part(0, 0, 1)
            sll2 = [part] + sll2
        for _ in range(ITERATIONS):
            sll2.pop(-1)
        list_end_time = time.time()

        ll_time = (ll_end_time - ll_start_time)
        l_time = (list_end_time - list_start_time)

        print("At iterations: %s" % ITERATIONS)
        print("Linked list time: %.3f s" % ll_time)
        print("List time: %.3f s" % l_time)
        print("Linked lists are: %.3f times faster than lists\n" % (l_time / ll_time))
