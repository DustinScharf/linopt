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

        return self.__iteration(xi_b, xi_n, x_b, A, c, print_steps)

    def __phase_1(self, xi_b, xi_n, x_b, A, c, print_steps: bool = False):
        xi_n = np.append(xi_n, len(c))

        A = np.insert(A, len(c), -1, axis=1)

        c = np.append(np.zeros_like(c), -1)

        out_idx = np.argmin(x_b)
        in_idx = len(xi_n) - 1
        xi_b[out_idx], xi_n[in_idx] = xi_n[in_idx], xi_b[out_idx]

        x_in_val = -x_b[out_idx]
        x_b += x_in_val
        x_b[out_idx] = x_in_val

        iteration = 0
        ins = np.full_like(xi_n, 1)
        while np.max(ins) > 0:
            if print_steps:
                print("phase1 iteration", iteration)
            iteration += 1

            A_b = A[:, xi_b]
            A_n = A[:, xi_n]

            c_b = c[xi_b]
            c_n = c[xi_n]

            y = np.linalg.solve(np.matrix.transpose(A_b), c_b)

            ins = np.subtract(c_n, np.dot(y, A_n))

            if print_steps:
                print("Ins:", ins)
            if np.max(ins) <= 0:
                if np.max(xi_n) > np.max(xi_b):
                    del_idx = np.argmax(xi_n)
                    xi_n = np.delete(xi_n, del_idx)
                else:
                    del_idx = np.argmax(xi_b)
                    xi_b = np.delete(xi_b, del_idx)
                    x_b = np.delete(x_b, del_idx)
                return "SOLVED", (xi_b, xi_n, x_b)
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
                return "UNBOUNDED", solution
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

    def __iteration(self, xi_b, xi_n, x_b, A, c, print_steps: bool = False) -> ProblemSolution:
        if np.min(x_b) < 0:
            A_restore, c_restore = A.copy(), c.copy()

            status_, data_ = self.__phase_1(xi_b, xi_n, x_b, A, c, print_steps)  # todo impl.
            if status_ == "UNBOUNDED":
                return data_
            elif status_ == "SOLVED":
                xi_b, xi_n, x_b = data_

            A, c = A_restore, c_restore

        iteration = 0
        ins = np.full_like(xi_n, 1)
        while np.max(ins) > 0:
            if print_steps:
                print("phase2 iteration", iteration)
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
