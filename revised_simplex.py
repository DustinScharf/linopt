import numpy as np

from problem import Problem
from problem_solution import ProblemSolution


class RevisedSimplex(object):
    def solve(self, problem: Problem, print_steps: bool = False) -> ProblemSolution:
        xi_b = np.arange(problem.A.shape[1], problem.A.shape[1] + problem.b.size)
        xi_n = np.arange(0, problem.A.shape[1])

        x_b = problem.b

        A_b = np.eye(x_b.size)
        A_n = problem.A
        A = np.concatenate((A_n, A_b), axis=1)

        c_b = np.zeros(x_b.size)
        c_n = problem.c
        c = np.concatenate((c_n, c_b))

        x_n = np.zeros_like(c_n)

        l = np.zeros_like(c_n)
        u = np.array([8, 6, 4, 15, 2, 10, 10, 3])

        return self.__iteration(xi_b, xi_n, x_b, x_n, l, u, A, c, print_steps)

    def __all_at_upper_bound(self, ins, u) -> bool:
        for in_var, upper_bound in zip(ins, u):
            if not np.isclose(in_var, upper_bound):
                return False
        return True

    def __iteration(self, xi_b, xi_n, x_b, x_n, l, u, A, c, print_steps: bool = False) -> ProblemSolution:
        # todo expand for boundaries

        iteration = 0
        ins = np.full_like(len(xi_n), 1)
        while np.max(ins) > 0 and not self.__all_at_upper_bound(ins, u):
            print("iteration", iteration)
            iteration += 1

            A_b = A[:, xi_b]
            A_n = A[:, xi_n]

            c_b = c[xi_b]
            c_n = c[xi_n]

            # solve (y * A_b = c_b) for y
            y = np.linalg.solve(np.matrix.transpose(A_b), c_b)

            # c_n - y * A_n
            ins = np.subtract(c_n, np.dot(y, A_n))
            if print_steps:
                print("Ins:", ins)
            if np.max(ins) <= 0:
                x_solution = np.array([xi_b, x_b])
                solution = ProblemSolution(np.dot(c_b, x_b), x_solution)
                if print_steps:
                    print("> DONE")
                    print()
                    print(solution)
                return solution
            in_idx = np.argmax(ins)
            if print_steps:
                print("> In x", xi_n[in_idx])
            a = A_n[:, in_idx]

            d = np.linalg.solve(A_b, a)

            outs = np.multiply(x_b, 1 / d)

            valid_out_idx = np.where(outs > 0)[0]
            if len(valid_out_idx) == 0:
                x_solution = np.array([xi_b, x_b])
                solution = ProblemSolution("UNBOUNDED", x_solution)
                if print_steps:
                    print("> DONE")
                    print()
                    print(solution)
                return solution
            out_idx = valid_out_idx[outs[valid_out_idx].argmin()]
            if print_steps:
                print("Outs:", outs)
            t = outs[out_idx]
            if print_steps:
                print("> Out x", xi_b[out_idx])

            xi_b[out_idx], xi_n[in_idx] = xi_n[in_idx], xi_b[out_idx]

            x_b = np.subtract(x_b, np.multiply(t, d))
            x_b[out_idx] = t

            if print_steps:
                print()
