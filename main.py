from class_definitions import *

game = BoardState(x=5, y=5)

print(game)

for i in range(10):
    try:
        game.move(Direction.LEFT)
        print(game)
    except GameOver as ex:
        print("You lose!")
        print(ex)
        break
