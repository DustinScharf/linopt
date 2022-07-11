from typing import Union

import numpy as np


class ProblemSolution(object):
    def __init__(self, z: Union[float, str], x: np.ndarray):
        self.z: float = z
        self.x: np.ndarray = np.round(x)

    def __str__(self) -> str:
        return f"{self.z}"

    def print_full_info(self) -> str:
        print(f"Solution:\n(Row 1: i, Row 2: xi)")
        print(self.x)
        print(f"\n=> OPTIMUM={self.z}")
