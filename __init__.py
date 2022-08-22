import game
from utils import *

# level = int(input("Welcome to bubble sort game, choose difficulty level:\n"
#                   "1) Easy      2) Medium       3) Hard \n"))

# max_color, max_bottle, max_length = set_initial_values(level)
#
# newGame = game.Game(max_color, max_bottle, max_length)  # max_color, max_bottle, max_length
# newGame.generate_bottles()

queue = [1,5,4,3,76]
queue = sorted(queue,reverse=True)
print(queue)