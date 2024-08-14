# Build-ins
import time

# Packages
import fpstimer

# Src imports
from life_game import GameOfLife, string_to_pattern

if __name__ == "__main__":
    # set num of iteration
    num_iteration = 500

    for grid_size in range(100, 1001, 100):
        # Init a game
        game = GameOfLife(grid_size)

        # Get a pattern
        pattern = string_to_pattern("6bob$4bob2o$4bobob$4bo3b$2bo5b$obo!")
        game.set_pattern(20,20, pattern)

        # Create a Framerate object with a desired frame rate
        timer = fpstimer.FPSTimer(10)

        # start timer
        start = time.perf_counter()

        # Compute
        game.next(num_iteration)

        # Display avg time / iteration
        print(f"At grid size {grid_size:3}, avg execution is {1e3*(time.perf_counter() - start) / num_iteration:.3f} ms / iterations. (Performed : {game.step} iterations).")

