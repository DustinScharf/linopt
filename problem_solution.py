from typing import Union

import numpy as np


class ProblemSolution(object):
    def __init__(self, z: Union[float, str], x: np.ndarray):
        self.z: float = z
        self.x: np.ndarray = np.round(x)

    def __str__(self) -> str:
        return f"{self.z}"

    def print_full_info(self):
        if self.z != "/ (NO SOLUTION)" and self.z != "UNBOUNDED":
            print(f"Solution:\n(Row 1: i, Row 2: x_i)")
            print(self.x)
            print("*Index starts at 0, slack is included\n")
            print(f"=> OPTIMUM = {self.z}")
        else:
            print(f"\nOPTIMUM = {self.z}")
