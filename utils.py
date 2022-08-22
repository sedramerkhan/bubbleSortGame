COLORS = ["darkorchid", "hotpink", "cyan", "cornflowerblue", "lime", "yellow", "crimson"]
COLORS_CONSOLE = ["purple", "pink", "cyan", "blue", "green", "yellow", "crimson"]
NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

MESSAGE = ["Source List Is Empty",  # 0
           "Destination List Is Full",  # 1
           "Source List's Colors Are Correct,You Don't Have To Change Them",
           "Two Different Balls' Colors",  # 3
           "move is done",  # 4
           "You Won, Restart Game",  # 5
           "You Lost, Restart Game",  # 6
           "You Have To Enter Only Integers between 1 and {}",  # 7
           "You Have To Enter Source And Destination Numbers.",  # 8
           "You Have To Enter Only Integers."  # 9
           ]

game_states = []


def set_initial_values(level):
    if level == 1:
        max_color, max_bottle, max_length = 3, 3, 4
    elif level == 2:
        max_color, max_bottle, max_length = 5, 5, 4
    else:
        max_color, max_bottle, max_length = 7, 7, 4
    return max_color, max_bottle, max_length
