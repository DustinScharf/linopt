import numpy as np

from problem import Problem


class ProblemReader(object):
    def __init__(self, directory: str = "HERE"):
        if directory != "HERE":
            raise NotImplementedError("Custom directory location is not implemented yet, "
                                      "use 'HERE' for same directory as this file")
        self.directory: str = directory

    def read_problem(self, csv_file_name: str) -> Problem:
        data = np.genfromtxt(csv_file_name, delimiter=',')

        # can be 1 (for max) or -1 (for min) so c is directly converted to a max problem
        max_min = np.array(data[0][-1])
        c = np.multiply(np.array(data[0][:-1]), max_min)

        A = np.array(data[1:data.shape[0], 0:data.shape[1] - 1])

        b = np.array(data[1:, -1])

        return Problem(c, A, b)
