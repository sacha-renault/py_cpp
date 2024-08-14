# You should writte the documentation here
# This step isn't mandatory but it will make you IDE autocomplete / docstring the classes and functions
# You can do this in the binding.cpp file too
from typing import overload
import numpy as np

class GameOfLife:
    @overload
    def __init__(self, x, y) -> None:
        """ Init a game with a grid of size x*y. """

    @overload
    def __init__(self, size) -> None:
        """ Init a game with a grid of size*size. Equivalent to __init__(self, size, size). """

    @property
    def grid(self) -> np.ndarray:
        """ Get the current grid. """

    @property
    def step(self) -> int:
        """ Current step of the game. """

    def set_pattern(self, x_offset: int, y_offset: int, pattern: np.ndarray) -> None:
        """ Set a pattern with the specified index.
        Args:
            x_offset(int): offset on rows.
            y_offset(int): offset on cols.
            pattern(np.ndarray): pattern to add

        Returns:
            NoReturn.

        Raises:
            RuntimeError: The patterns overflows on the grid.
        """

    @overload
    def next(self) -> None:
        """ Compute one step of the game of life. """

    @overload
    def next(self, num_steps: int) -> None:
        """ Compute num_steps steps of the game of life.
        Args:
            num_steps (int): Number of steps to compute
        """
