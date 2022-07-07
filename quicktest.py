import time

import numpy as np

import problem_reader
from problem_solver import ProblemSolver

if __name__ == '__main__':
    problem_reader = problem_reader.ProblemReader()
    problem_solver = ProblemSolver()

    print("===== TEST START =====")

    start_time = time.time()

    # UE
    # 1
    print(np.isclose(problem_solver.solve(problem_reader.read_problem("btu_ss2022_opt1_ue1_a1.csv")).z, 32))
    print(np.isclose(problem_solver.solve(problem_reader.read_problem("btu_ss2022_opt1_ue2_a2.csv")).z, 211))
    # 3
    print(np.isclose(problem_solver.solve(problem_reader.read_problem("btu_ss2022_opt1_ue3_a1.csv")).z, 4))
    # 4
    print(np.isclose(problem_solver.solve(problem_reader.read_problem("btu_ss2022_opt1_ue4_a2.csv")).z, 58))
    # 5
    print(np.isclose(problem_solver.solve(problem_reader.read_problem("btu_ss2022_opt1_ue5_a1.csv")).z, 2440))

    # HA
    # 6
    print(problem_solver.solve(problem_reader.read_problem("btu_ss2022_opt1_ha6_a1.csv")).z == "UNBOUNDED")
    print(np.isclose(problem_solver.solve(problem_reader.read_problem("btu_ss2022_opt1_ha6_a2.csv")).z, 30))

    print(f"===== TEST END IN {round(time.time() - start_time, 3)} SECONDS =====")
