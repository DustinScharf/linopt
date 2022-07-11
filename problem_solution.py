from typing import Union

import numpy as np


class ProblemSolution(object):
    def __init__(self, z: Union[float, str], x: np.ndarray):
        self.z: float = z
        self.x: np.ndarray = x

    def __str__(self) -> str:
        return f"{self.z}"

    def full_info(self) -> str:
        return f"Solution:\n(Row 1: i, Row 2: xi)\n{self.x}\n\n=> OPTIMUM={self.z}"
