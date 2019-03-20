from class_definitions import BoardState, RandomSolver
import time

game = BoardState(x=10, y=10)

my_solver = RandomSolver(game)

start = time.time()
steps = 0
try:
    while(True):
        steps += 1
        my_solver.solve()
        #print(my_solver.board)
        #time.sleep(0.1)
except:
    pass

end = time.time()

print("Seconds elapsed:", end-start)
print("Steps:", steps)
print("Length:", len(my_solver.board.snakeblocks))
print(game)