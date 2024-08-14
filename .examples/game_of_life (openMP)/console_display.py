# Build-ins
import os

# Packages
import numpy as np
import fpstimer

# Src imports
from life_game import GameOfLife, string_to_pattern, print_game


if __name__ == "__main__":
    # Init a game
    game = GameOfLife(50)

    # Get a pattern
    pattern = string_to_pattern("6bob$4bob2o$4bobob$4bo3b$2bo5b$obo!")
    game.set_pattern(20,20, pattern)

    # Create a Framerate object with a desired frame rate
    timer = fpstimer.FPSTimer(10)

    try:
        while True:
            os.system("clear")
            game.next()
            print_game(game)
            timer.sleep()
    except KeyboardInterrupt:
        pass
