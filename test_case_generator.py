import numpy as np


class TestCaseGenerator:

    def generate_test(self,
                      A_min=0, A_max=100, A_height=100, A_width=100,
                      x_min=0, x_max=100,
                      c_min=0, c_max=10,
                      file_name="auto_test.csv"):
        # Ax=b
        A = np.random.randint(A_min, A_max, size=(A_width, A_height))
        print(A)
        print()

        x = np.random.randint(x_min, x_max, size=A_height)
        print(x)
        print()

        b = np.dot(A, x)
        print(b)
        print()

        c = np.random.randint(c_min, c_max, size=A_width)
        print(c)
        print()

        # Only for specific tests, can cause recursion overflow
        # if np.min(b) < 0:
        #     self.generate_test(min, max, height, width)

        file = open(file_name, "w")
        for x in range(A_width):
            file.write(f"{c[x]},")
        file.write("1\n")
        for y in range(A_height):
            for x in range(A_width):
                file.write(f"{A[x, y]},")
            file.write(f"{b[y]}\n")
        file.close()


if __name__ == '__main__':
    test = TestCaseGenerator()
    size = 1000
    test.generate_test(A_height=size, A_width=size,
                       file_name="test1000.csv")
