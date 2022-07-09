import sys
import time

from problem_reader import ProblemReader
from problem_solver import ProblemSolver
from quicktest import QuickTester


def get_args_or_exit():
    def print_error_and_exit():
        print("\nlinopt was started with wrong input")
        print("===================================\n")

        print("Use\n\t>>> python linopt.py YOUR_CSV_FILE.csv\n\t(Default, solve problem from csv file)\n"
              "or\n\t>>> python linopt.py test\n\t(Test all problems from the exercises)\n")
        print("Or use\n\t"
              ">>> python linopt.py YOUR_CSV_FILE.csv print\n\t(Solve problem from csv file and print steps)\n")
        exit(1)

    args = sys.argv[1:]

    if len(args) == 0 or (len(args) != 1) and (".csv" not in args[0] or (args[1] != "print" or len(args) != 2)):
        print_error_and_exit()

    if ".csv" in args[0]:
        if len(args) == 2:
            return "SOLVE_AND_PRINT", args[0]
        else:
            return "SOLVE", args[0]
    elif args[0] == "test":
        return "TEST", None
    else:
        print_error_and_exit()


if __name__ == '__main__':
    type, problem = get_args_or_exit()

    problem_reader = ProblemReader()
    problem_solver = ProblemSolver()

    print("\nWelcome to linopt")
    print("=================\n")

    if type == "SOLVE":
        print(f'Starting to solve problem "{problem}"\n...\n')

        start_time = time.time()

        solution = problem_solver.solve(problem_reader.read_problem(problem))

        print(solution.full_info())

        print(f"\n=== Finished in around {round(time.time() - start_time, 3)} seconds ===\n")
    elif type == "SOLVE_AND_PRINT":
        print(f'Starting to solve problem "{problem}" and printing steps\n...\n')

        start_time = time.time()

        try:
            problem_solver.solve(problem_reader.read_problem(problem), print_steps=True, print_iteration=True)
        except FileNotFoundError:
            print(f"File {problem} was not found...")

        print(f"\n=== Finished in around {round(time.time() - start_time, 3)} seconds ===\n")
    else:
        print(f'Starting to test all problems from the exercises\n...\n')

        start_time = time.time()

        quick_tester = QuickTester()
        quick_tester.test_all()

        print(f"\n=== Finished in around {round(time.time() - start_time, 3)} seconds ===\n")

