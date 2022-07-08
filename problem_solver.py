from enum import Enum

from problem import Problem
from revised_simplex import RevisedSimplex


class Methods(Enum):
    revised_simplex = 1


class ProblemSolver(object):
    def __init__(self):
        self.__revised_simplex = RevisedSimplex()

    def solve(self, problem: Problem, method: Methods = Methods.revised_simplex,
              print_steps: bool = False, print_iteration: bool = False):
        if method == Methods.revised_simplex:
            return self.__revised_simplex.solve(problem, print_steps, print_iteration)
        else:
            raise NotImplementedError("The passed method is not supported, use Methods.revised_simplex")
