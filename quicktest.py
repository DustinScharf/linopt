import time

import numpy as np

from problem_reader import ProblemReader
from problem_solver import ProblemSolver


class QuickTester:
    def test_all(self):
        problem_reader = ProblemReader()
        problem_solver = ProblemSolver()

        problems_solutions = [
            ("btu_ss2022_opt1_ue1_a1.csv", 32),  # UE 1
            ("btu_ss2022_opt1_ue1_a2.csv", 211),
            ("btu_ss2022_opt1_ue3_a1.csv", 4),  # UE 3
            ("btu_ss2022_opt1_ue4_a2.csv", 58),  # UE 4
            ("btu_ss2022_opt1_ue5_a1.csv", 2440),  # UE 5

            ("btu_ss2022_opt1_ha6_a1.csv", "UNBOUNDED"),  # HA 6
            ("btu_ss2022_opt1_ha6_a2.csv", 30),

            ("endris_sample_problem.csv", "UNBOUNDED"),  # Other
        ]

        error_counter = 0

        for problem_solution in problems_solutions:
            problem = problem_reader.read_problem(problem_solution[0])
            calc_solution = problem_solver.solve(problem, eta_factorisation=True, eta_reset=20, bland=True).z
            true_solution = problem_solution[1]
            try:
                test_success = np.isclose(calc_solution, true_solution)
            except TypeError:
                try:
                    test_success = (calc_solution == true_solution)
                except TypeError:
                    test_success = False
            if not test_success:
                error_counter += 1
            print(f"Test result: {test_success}")

        print()

        test_counter = len(problems_solutions)
        if error_counter == 0:
            print(f"{test_counter}/{test_counter} test{('' if len(problems_solutions) == 1 else 's')} succeeded")
        else:
            print(f"{error_counter}/{test_counter} test{('' if error_counter == 1 else 's')} failed")


if __name__ == '__main__':
    quick_tester = QuickTester()
    quick_tester.test_all()
