import time

from problem_reader import ProblemReader
from problem_solver import ProblemSolver, Methods

if __name__ == '__main__':
    start_time = time.time()

    problem_reader = ProblemReader()

    # problem = problem_reader.read_problem("btu_ss2022_opt1_ue5_a1.csv")  # 2440
    # problem = problem_reader.read_problem("btu_ss2022_opt1_ue4_a2.csv")  # 58
    problem = problem_reader.read_problem("btu_ss2022_opt1_ue2_a2.csv")  # 211
    # problem = problem_reader.read_problem("test100.csv")  # 39259.79 (iteration 112, 1.03 seconds)
    # problem = problem_reader.read_problem("test250.csv")  # 101252.89 (iteration 365, 27.91 seconds)
    # problem = problem_reader.read_problem("test500.csv")  # 199058.75 (iteration 2119, 249.21 seconds ~ 4min)
    # problem = problem_reader.read_problem("test750.csv")  # 288670.13 (iteration 3544, 934.85 seconds ~ 15min)
    # problem = problem_reader.read_problem("test1000.csv")  # 400755.57 (iteration 7881, 2130.92 seconds ~ 35min)

    problem_solver = ProblemSolver()
    print(problem_solver.solve(problem, Methods.revised_simplex))

    print(f"\nFinished in {time.time() - start_time} seconds")
