from class_definitions import BoardState, FixedPathSolver
import time

game = BoardState(x=10, y=10)

my_solver = FixedPathSolver(game)

start = time.time()
steps = 0
try:
    while(True):
        steps += 1
        direction = my_solver.solve(apply=False)
        
        #print(my_solver.board)
        #time.sleep(0.1)
except:
    pass

end = time.time()

print("Seconds elapsed:", end-start)
print("Steps:", steps)
print("Length:", len(my_solver.board.snakeblocks))