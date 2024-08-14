import numpy as np
from .life_game import GameOfLife


def string_to_pattern(str_pattern: str) -> np.ndarray:
    states = {'o' : 1, 'b' : 0}
    n = len(str_pattern)
    rows = []
    row = []
    num = 0
    ptr = 0

    while ptr < n:
        # Access at index
        char = str_pattern[ptr]

        if char == "!": # End of pattern
            rows.append(row)
            break;

        elif char == "$": # End of line
            rows.append(row)
            row = []

        elif char in states: # State of cell
            cell = states.get(char)
            row.extend([cell]*max(1, num))
            num = 0
        else: # Number
            num = num * 10 + int(char)

        # Go further
        ptr += 1
        print(ptr, end="\r")

    # padd rows
    max_length = max([len(row) for row in rows])
    for row in rows:
        row.extend([0] * (max_length - len(row)))
    return np.array(rows)

# Prettier print than 0 and 1s
def print_game(game : GameOfLife):
    print(f"Game at step : {game.step}")
    for row in game.grid:
        for val in row:
            if val == 1:
                print("■", end=" ")
            elif val == 0:
                print(" ", end=" ")
            else:
                raise ValueError(f"Cannot display value that isn't 0 or 1, got : {val}")
        print()