''' Unit Tests for methods in SnakeLL '''

from Part import Part
from SnakeLL import SnakeLL

# Testing constructor
snake = SnakeLL()
print("Constructing snake...")
print("Snake's front is:", snake.front)
print("Snake's back is:", snake.back)
print("Snake's length is:", snake.length)
print("Snake's list of blocks is", snake.ll)

# Testing insert_front
snake.insert_front('howdy')
print(snake.ll)

#Testing drop_back