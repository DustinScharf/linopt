from enum import Enum

from problem import Problem
from revised_simplex import RevisedSimplex


class Methods(Enum):
    revised_simplex = 1


class ProblemSolver(object):
    def __init__(self):
        self.__revised_simplex = RevisedSimplex()

    def solve(self, problem: Problem, eta_factorisation: bool = True, eta_reset: int = 20,
              print_steps: bool = False, print_iteration: bool = False):
        eta_reset = max(eta_reset, 1)
        return self.__revised_simplex.solve(problem, eta_factorisation, eta_reset, print_steps, print_iteration)
