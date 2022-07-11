import os
import sys
import time

from problem_reader import ProblemReader
from problem_solver import ProblemSolver


def cli():
    print("Enter a problem (csv file) you want to solve (include .csv)...")
    problem = input()
    if problem[-4:] != ".csv" or not os.path.isfile(problem):
        print("Invalid input, enter a existing csv file including .csv, exit...\n")
        exit(1)
    print()

    print("Print the steps? (y/n)")
    print_steps = input()
    if print_steps == 'y':
        print_steps = True
    elif print_steps == 'n':
        print_steps = False
    else:
        print("Invalid input, use only y or n, exit...\n")
        exit(1)
    print()

    print("Use eta basis factorisation? (y/n)")
    use_eta = input()
    if use_eta == 'y':
        use_eta = True
    elif use_eta == 'n':
        use_eta = False
    else:
        print("Invalid input, use only y or n, exit...\n")
        exit(1)
    print()

    eta_steps = -1
    if use_eta:
        print("After how many iteration shall the basis factorisation reset?")
        try:
            eta_steps = int(input())
        except ValueError:
            print("Invalid input, enter a number, exit...\n")
            exit(1)
        print()

    print(f'Starting to solve problem "{problem}"\n...\n')

    start_time = time.time()

    if print_steps:
        problem_solver.solve(problem_reader.read_problem(problem),
                             eta_factorisation=use_eta, eta_reset=eta_steps,
                             print_steps=True, print_iteration=True)
    else:
        solution = problem_solver.solve(problem_reader.read_problem(problem),
                                        eta_factorisation=use_eta, eta_reset=eta_steps)
        print(f"=> Optimum={solution}")

    print(f"\n=== Finished in around {round(time.time() - start_time, 3)} seconds ===\n")


def cl_out():
    args = sys.argv[1:]

    problem = None
    use_eta = False
    eta_steps = 20
    print_steps = False

    for arg in args:
        arg = str(arg)
        if arg[-4:] == ".csv":
            if os.path.isfile(arg):
                problem = arg
            else:
                print(f"The csv file >> {arg} << was not found, exit...\n")
                exit(1)
        elif arg == "eta":
            use_eta = True
        elif arg[:4] == "eta-":
            use_eta = True
            try:
                eta_steps = int(arg[4:])
            except ValueError:
                print("Invalid input, enter a number, exit...\n")
                exit(1)
        elif arg == "print":
            print_steps = True
        else:
            print(f"Invalid argument >> {arg} <<, visit https://github.com/DustinScharf/linopt for help, exit...\n")
            exit(1)

    if problem is None:
        print("Missing necessary problem argument, exit...\n")
        exit(1)

    print(f"Starting to solve problem >> {problem} <<\n...\n")

    start_time = time.time()

    if print_steps:
        problem_solver.solve(problem_reader.read_problem(problem),
                             eta_factorisation=use_eta, eta_reset=eta_steps,
                             print_steps=True, print_iteration=True)
    else:
        solution = problem_solver.solve(problem_reader.read_problem(problem),
                                        eta_factorisation=use_eta, eta_reset=eta_steps)
        print(f"=> Optimum={solution}")

    print(f"\n=== Finished in around {round(time.time() - start_time, 3)} seconds ===\n")


if __name__ == '__main__':
    print("\nWelcome to linopt")
    print("=================\n")

    print("*use CTRL+C to quit\n")

    args = sys.argv[1:]
    if len(args) == 1 and (args[0] == "v" or args[0] == "version"):
        print("1.0")
        exit(0)

    problem_reader = ProblemReader()
    problem_solver = ProblemSolver()

    if len(args) == 0:
        cli()
    else:
        cl_out()
