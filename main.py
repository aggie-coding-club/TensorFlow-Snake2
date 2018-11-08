from class_definitions import *
import time

game = BoardState(x=8, y=11)

print(game)

exception_test_code = """
for i in range(10):
    try:
        game.move(Direction.LEFT)
        print(game)
    except GameOver as ex:
        print("You lose!")
        print(ex)
        break"""


a="""
dir_dict = {
    "u":Direction.UP,
    "d":Direction.DOWN,
    "l":Direction.LEFT,
    "r":Direction.RIGHT,
    "U":Direction.UP,
    "D":Direction.DOWN,
    "L":Direction.LEFT,
    "R":Direction.RIGHT
}
while(True):
    usr_in = input("Move in a direction: u-<UP> d-<DOWN> l-<LEFT> r-<RIGHT> q-<QUIT>\nInput: ")
    move_dir = usr_in[-1] #get last letter of input
    if move_dir in dir_dict:
        try:
            game.move(dir_dict[move_dir])
            print(game)
        except GameOver as ex:
            print("You lose!")
            print(ex)
            break
        except HailVictory as ex:
            print("Victory!")
            print(ex)
            break
    elif move_dir in ["q", "Q"]:
        print("exiting...")
        break
    else:
        print("unrecognized input")
        continue"""

debug = """
my_solver = RandomSolver(game)
while(True):
    my_solver.solve()
    print(my_solver.board)
    time.sleep(0.1)"""

my_solver = FixedPathSolver(game)
