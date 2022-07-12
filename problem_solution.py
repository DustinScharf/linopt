from typing import Union

import numpy as np


class ProblemSolution(object):
    def __init__(self, z: Union[float, str], x: Union[np.ndarray, None], slack: Union[np.ndarray, None]):
        self.z: float = z
        if x is not None and slack is not None:
            self.x: np.ndarray = np.round(x)
            self.slack: np.ndarray = np.round(slack)

    def __str__(self) -> str:
        return f"{self.z}"

    def print_full_info(self):
        if self.z != "/ (NO SOLUTION)" and self.z != "UNBOUNDED":
            print("--- --- --- --- --- --- --- --- ---")
            print(f"Solution for x:\n(Row 1: i, Row 2: x_i)")
            print(self.x)
            print("*Index starts at 0")
            print()
            print(f"Slack:")
            print(self.slack)
            print(f"\n=> OPTIMUM = {self.z}")
            print("--- --- --- --- --- --- --- --- ---")
        else:
            print(f"OPTIMUM = {self.z}")
