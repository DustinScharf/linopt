import numpy as np
import pandas as pd

from problem import Problem


class ProblemReader(object):
    def __init__(self, directory: str = "HERE"):
        if directory != "HERE":
            raise NotImplementedError("Custom directory location is not implemented yet, "
                                      "use 'HERE' for same directory as this file") # todo
        self.directory: str = directory

    def read_problem(self, csv_file_name: str) -> Problem:
        data = pd.read_csv(csv_file_name)

        pre_c = data[data['type'].str.match('z')]
        if pre_c.shape[0] != 1:
            print("No Z-function or more then 1 Z-function in CSV, exit...")
            exit(1)

        max_min = 1 if pre_c.iloc[0][-1] == 'max' else -1
        c = np.multiply(
            pd.DataFrame.to_numpy(pre_c.drop(pre_c.columns[[-1, -2]], axis=1), dtype=np.float64),
            max_min
        ).flatten()

        pre_u = data[data['b'].str.match('u')]
        if pre_u.shape[0] > 1:
            print("More then 1 upper bounds per variable in CSV, exit...")
            exit(1)
        elif pre_u.shape[0] == 0:
            u = np.full(len(data.index), np.inf, dtype=np.float64)
        else:
            u = pd.DataFrame.to_numpy(pre_u.drop(pre_u.columns[[-1, -2]], axis=1), dtype=np.float64).flatten()

        pre_l = data[data['b'].str.match('l')]
        if pre_l.shape[0] > 1:
            print("No lower bounds or more then 1 lower bounds per variable in CSV, exit...")
            exit(1)
        elif pre_l.shape[0] == 0:
            l = np.zeros(len(data.index), dtype=np.float64)
        else:
            l = pd.DataFrame.to_numpy(pre_l.drop(pre_l.columns[[-1, -2]], axis=1), dtype=np.float64).flatten()

        le_pre = data[data['type'].str.match('<=')]
        A_le = pd.DataFrame.to_numpy(le_pre.drop(le_pre.columns[[-1, -2]], axis=1), dtype=np.float64)
        b_le = pd.Series.to_numpy(le_pre['b'], dtype=np.float64).flatten()

        ge_pre = data[data['type'].str.match('>=')]
        A_ge = pd.DataFrame.to_numpy(ge_pre.drop(ge_pre.columns[[-1, -2]], axis=1), dtype=np.float64)
        b_ge = pd.Series.to_numpy(ge_pre['b'], dtype=np.float64).flatten()

        A_le = np.row_stack((A_le, A_ge * -1))
        b_le = np.append(b_le, b_ge * -1)

        e_pre = data[data['type'].str.match('=')]  # todo add ==
        A_e = pd.DataFrame.to_numpy(e_pre.drop(e_pre.columns[[-1, -2]], axis=1), dtype=np.float64)
        b_e = pd.Series.to_numpy(e_pre['b'], dtype=np.float64).flatten()

        A_le = np.row_stack((A_le, A_e, A_e * -1)) # todo causes Ab to be not squared
        b_le = np.append(b_le, np.append(b_e, b_e * -1))

        return Problem(c, A_le, b_le)
