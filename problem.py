import numpy as np

class Problem(object):
    def __init__(self, c: np.ndarray, A: np.ndarray, b: np.ndarray):
        self.c: np.ndarray = c
        self.A: np.ndarray = A
        self.b: np.ndarray = b
