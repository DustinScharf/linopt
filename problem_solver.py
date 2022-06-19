from enum import Enum

from problem import Problem
from revised_simplex import RevisedSimplex


class Methods(Enum):
    revised_simplex = 1


class ProblemSolver(object):
    def __init__(self):
        self.__revised_simplex = RevisedSimplex()

    def solve(self, problem: Problem, method: Methods, print_steps: bool = False):
        if method == Methods.revised_simplex:
            return self.__revised_simplex.solve(problem, print_steps)
        else:
            raise NotImplementedError("Only Methods.revised_simplex is implemented yet")
