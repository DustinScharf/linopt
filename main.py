import time

from problem_reader import ProblemReader
from problem_solver import ProblemSolver, Methods

if __name__ == '__main__':
    problem_reader = ProblemReader()

    problem = problem_reader.read_problem("btu_ss2022_opt1_ue1_a1.csv")  # 32
    # problem = problem_reader.read_problem("btu_ss2022_opt1_ue2_a2.csv")  # 211
    # problem = problem_reader.read_problem("btu_ss2022_opt1_ue3_a1.csv")  # 4
    # problem = problem_reader.read_problem("btu_ss2022_opt1_ue4_a2.csv")  # 58
    # problem = problem_reader.read_problem("btu_ss2022_opt1_ue5_a1.csv")  # 2440
    # problem = problem_reader.read_problem("btu_ss2022_opt1_ha6_a1.csv")  # UNBOUNDED
    # problem = problem_reader.read_problem("btu_ss2022_opt1_ha6_a2.csv")  # 30

    problem_solver = ProblemSolver()

    start_time = time.time()

    # problem_solver.solve(problem, Methods.revised_simplex, print_steps=True)
    print(problem_solver.solve(problem, Methods.revised_simplex, print_steps=False))

    print(f"\nFinished in {time.time() - start_time} seconds")
