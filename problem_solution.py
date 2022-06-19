import numpy as np


class ProblemSolution(object):
    def __init__(self, z: float, x: np.ndarray):
        self.z: float = z
        self.x: np.ndarray = x

    def __str__(self):
        return f"Solution:\n{self.x}\n\n=> OPTIMUM={self.z}"
