import numpy as np

import problem_reader
from problem_solver import ProblemSolver

if __name__ == '__main__':
    problem_reader = problem_reader.ProblemReader()
    problem_solver = ProblemSolver()

    print(np.isclose(problem_solver.solve(problem_reader.read_problem("btu_ss2022_opt1_ue3_a1.csv")).z, 4))
    print(np.isclose(problem_solver.solve(problem_reader.read_problem("btu_ss2022_opt1_ue2_a2.csv")).z, 211))
    print(problem_solver.solve(problem_reader.read_problem("btu_ss2022_opt1_ha6_a1.csv")).z == "UNBOUNDED")
    print()
    print(np.isclose(problem_solver.solve(problem_reader.read_problem("btu_ss2022_opt1_ha6_a2.csv")).z, 30))
