import warnings

import numpy as np
from scipy.sparse.linalg import splu

from problem import Problem
from problem_solution import ProblemSolution

warnings.filterwarnings('ignore', message='splu requires CSC matrix format')
np.set_printoptions(suppress=True)


class RevisedSimplex(object):
    def solve(self, problem: Problem, eta_factorisation: bool = True, eta_reset: int = 10, bland: bool = False,
              print_steps: bool = False, print_iteration: bool = False) -> ProblemSolution:
        xi_b = np.arange(problem.A.shape[1], problem.A.shape[1] + problem.b.size)
        xi_n = np.arange(0, problem.A.shape[1])

        x_b = problem.b

        A_b = np.eye(x_b.size)
        A_n = problem.A
        A = np.concatenate((A_n, A_b), axis=1)

        c_b = np.zeros(x_b.size)
        c_n = problem.c
        c = np.concatenate((c_n, c_b))

        b_factors = []

        return self.__phase2(xi_b, xi_n, x_b, A, c, b_factors,
                             eta_factorisation, eta_reset, bland,
                             print_steps, print_iteration)

    def __phase1(self, xi_b, xi_n, x_b, A, c, b_factors,
                 eta_factorisation, eta_reset, bland,
                 print_steps, print_iteration):
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
            if print_iteration:
                print("phase1 iteration", iteration)
            iteration += 1

            A_b = A[:, xi_b]
            A_n = A[:, xi_n]

            c_b = c[xi_b]
            c_n = c[xi_n]

            if eta_factorisation:
                if len(b_factors) >= eta_reset:
                    current_value = np.matmul(b_factors[0], b_factors[1])
                    for b_factor in b_factors[2:]:
                        current_value = np.matmul(current_value, b_factor)
                    A_LU = splu(current_value, permc_spec="NATURAL", diag_pivot_thresh=0,
                                options={"SymmetricMode": True})
                    b_factors.clear()
                    b_factors.append(A_LU.L.toarray())
                    b_factors.append(A_LU.U.toarray())
                elif len(b_factors) == 0:
                    A_LU = splu(A_b, permc_spec="NATURAL", diag_pivot_thresh=0, options={"SymmetricMode": True})
                    b_factors.append(A_LU.L.toarray())
                    b_factors.append(A_LU.U.toarray())

                # BTran
                last_solve = np.linalg.solve(np.matrix.transpose(b_factors[-1]), c_b)
                for b_factor in reversed(b_factors[:-1]):
                    last_solve = np.linalg.solve(np.matrix.transpose(b_factor), last_solve)

                y = last_solve
            else:
                # solve (y * A_b = c_b) for y directly
                y = np.linalg.solve(np.matrix.transpose(A_b), c_b)

            ins = np.subtract(c_n, np.dot(y, A_n))

            if print_steps:
                print("Ins:", ins)
            if np.max(ins) <= 0:
                if np.max(xi_n) > np.max(xi_b):
                    del_idx = np.argmax(xi_n)
                    xi_n = np.delete(xi_n, del_idx)
                else:
                    solution = ProblemSolution("/ (NO SOLUTION)", None, None)
                    if print_steps:
                        print()
                        solution.print_full_info()
                    return "UNSOLVED", solution
                if print_steps:
                    print()
                return "SOLVED", (xi_b, xi_n, x_b)
            if bland:
                valid_in_idx = np.where((ins > 0) & (np.isfinite(ins)))[0]
                in_idx = min(valid_in_idx)
            else:
                in_idx = np.argmax(ins)
            if print_steps:
                print("> In x", xi_n[in_idx])
            a = A_n[:, in_idx]

            # FTran
            if eta_factorisation:
                last_solve = np.linalg.solve(b_factors[0], a)
                for b_factor in b_factors[1:]:
                    last_solve = np.linalg.solve(b_factor, last_solve)

                d = last_solve
            else:
                # solve A_b*d = a for d directly
                d = np.linalg.solve(A_b, a)

            # divide by 0 would give inf, what we can accept here
            with np.errstate(divide='ignore'):
                outs = np.divide(x_b, d)
                outs[np.isnan(outs)] = 0

            if print_steps:
                print("Outs:", outs)
            valid_out_idx = np.where((outs > 0) & (np.isfinite(outs)))[0]
            if len(valid_out_idx) == 0:
                x_solution = np.array([xi_b, x_b], dtype=np.float64)
                solution = ProblemSolution("/ (NO SOLUTION)", None, None)
                if print_steps:
                    print()
                    solution.print_full_info()
                return "UNSOLVED", solution
            out_idx = valid_out_idx[outs[valid_out_idx].argmin()]
            t = outs[out_idx]
            if print_steps:
                print("> Out x", xi_b[out_idx])

            xi_b[out_idx], xi_n[in_idx] = xi_n[in_idx], xi_b[out_idx]

            x_b = np.subtract(x_b, np.multiply(t, d))
            x_b[out_idx] = t

            if eta_factorisation:
                new_b_factor = np.eye(len(A_b))
                new_b_factor[:, out_idx] = d
                b_factors.append(new_b_factor)

            if print_steps:
                print()

    def __phase2(self, xi_b, xi_n, x_b, A, c, b_factors,
                 eta_factorisation, eta_reset, bland,
                 print_steps, print_iteration) -> ProblemSolution:
        if np.min(x_b) < 0:
            A_restore, c_restore = A.copy(), c.copy()

            status_, data_ = self.__phase1(xi_b, xi_n, x_b, A, c, b_factors,
                                           eta_factorisation, eta_reset, bland,
                                           print_steps, print_iteration)
            if status_ == "UNSOLVED":
                return data_
            elif status_ == "SOLVED":
                xi_b, xi_n, x_b = data_
            elif status_ == "SOLVED_FINAL":
                return data_

            A, c = A_restore, c_restore
            b_factors.clear()

        iteration = 0
        ins = np.full_like(xi_n, 1)
        while np.max(ins) > 0:
            if print_iteration:
                print("phase2 iteration", iteration)
            iteration += 1

            A_b = A[:, xi_b]
            A_n = A[:, xi_n]

            c_b = c[xi_b]
            c_n = c[xi_n]

            if eta_factorisation:
                if len(b_factors) >= eta_reset:
                    current_value = np.matmul(b_factors[0], b_factors[1])
                    for b_factor in b_factors[2:]:
                        current_value = np.matmul(current_value, b_factor)
                    A_LU = splu(current_value, permc_spec="NATURAL", diag_pivot_thresh=0,
                                options={"SymmetricMode": True})
                    b_factors.clear()
                    b_factors.append(A_LU.L.toarray())
                    b_factors.append(A_LU.U.toarray())
                elif len(b_factors) == 0:
                    A_LU = splu(A_b, permc_spec="NATURAL", diag_pivot_thresh=0, options={"SymmetricMode": True})
                    b_factors.append(A_LU.L.toarray())
                    b_factors.append(A_LU.U.toarray())

                # BTran
                last_solve = np.linalg.solve(np.matrix.transpose(b_factors[-1]), c_b)
                for b_factor in reversed(b_factors[:-1]):
                    last_solve = np.linalg.solve(np.matrix.transpose(b_factor), last_solve)

                y = last_solve
            else:
                # solve (y * A_b = c_b) for y directly
                y = np.linalg.solve(np.matrix.transpose(A_b), c_b)

            # c_n - y * A_n
            ins = np.subtract(c_n, np.dot(y, A_n))
            if print_steps:
                print("Ins:", ins)
            if np.max(ins) <= 0:
                full_x_solution = np.array([xi_b, x_b], dtype=np.float64)
                full_x_solution = np.column_stack((full_x_solution, np.row_stack((xi_n, np.zeros_like(xi_n)))))
                full_x_solution = full_x_solution[:, full_x_solution[0].argsort()]
                x_solution, slack = full_x_solution[:, :len(xi_n)], full_x_solution[:, len(xi_n):]
                solution = ProblemSolution(np.dot(c_b, x_b), x_solution, slack)
                if print_steps:
                    print("> DONE")
                    print()
                    solution.print_full_info()
                return solution
            if bland:
                valid_in_idx = np.where((ins > 0) & (np.isfinite(ins)))[0]
                in_idx = min(valid_in_idx)
            else:
                in_idx = np.argmax(ins)
            if print_steps:
                print("> In x", xi_n[in_idx])
            a = A_n[:, in_idx]

            if eta_factorisation:
                # FTran
                last_solve = np.linalg.solve(b_factors[0], a)
                for b_factor in b_factors[1:]:
                    last_solve = np.linalg.solve(b_factor, last_solve)

                d = last_solve
            else:
                # solve A_b*d = a for d directly
                d = np.linalg.solve(A_b, a)

            # divide by 0 would give inf, what we can accept here
            with np.errstate(divide='ignore'):
                outs = np.divide(x_b, d)

            valid_out_idx = np.where((outs > 0) & (np.isfinite(outs)))[0]
            if print_steps:
                print("Outs:", outs)
            if len(valid_out_idx) == 0:
                x_solution = np.array([xi_b, x_b], dtype=np.float64)
                solution = ProblemSolution("UNBOUNDED", None, None)
                if print_steps:
                    print("> DONE")
                    print()
                    solution.print_full_info()
                return solution
            out_idx = valid_out_idx[outs[valid_out_idx].argmin()]
            t = outs[out_idx]
            if print_steps:
                print("> Out x", xi_b[out_idx])

            xi_b[out_idx], xi_n[in_idx] = xi_n[in_idx], xi_b[out_idx]

            x_b = np.subtract(x_b, np.multiply(t, d))
            x_b[out_idx] = t

            if eta_factorisation:
                new_b_factor = np.eye(len(A_b))
                new_b_factor[:, out_idx] = d
                b_factors.append(new_b_factor)

            if print_steps:
                print()
