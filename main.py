import copy
from fractions import Fraction

from tabulate import tabulate
from LinearAlgebra import PointVector, Matrix


def read_data_from_file(file_name: str):
    with open(file_name) as input_file:
        n_input = int(input_file.readline()) # count of variables
        c_input = PointVector(*list(map(float, input_file.readline().split())))
        assert n_input == len(c_input)
        m = int(input_file.readline()) # count of equations
        x_input = Matrix([list(map(float, input_file.readline().split())) for _ in range(m)])
        assert x_input .m == m and x_input.n == n_input
        b = PointVector(*list(map(float, input_file.readline().split()))) # constant term column
        assert len(b) == m
    return n_input, c_input, m, x_input, b


def transform_initial_conditions_into_operating_conditions(n_input, c_input, m_input, x_input, b_input):
    m = m_input
    n = n_input + m
    basis_elements_numbers = [i for i in range(n_input, n)]
    x = copy.deepcopy(x_input)
    for i in range(m):
        x.add_column([int(i_ == i) for i_ in range(m)])
    c = PointVector(*(c_input.coordinates + [0] * (m + 1)))
    b = b_input
    return n, m, basis_elements_numbers, c, x, b


class SimplexMethod[T = float]:
    def __init__(self, n: int, m: int, basic_elements_numbers: list[int], c: PointVector[T], x: Matrix[T], b: PointVector[T]):
        self.n = n
        self.m = m
        self.basic_elements_numbers = basic_elements_numbers
        self.c = c
        self.x = x
        self.b = b
        self.reduced_cost = PointVector(*([0] * self.m))

        self.delta: PointVector[T] = PointVector(*([0] * n))
        self.F: int = 0
        self.calculate_delta()

        self.pivot_column_index: int = 0
        self.pivots_string_index: int = 0
        self.pivot_element: T = 0


    def go_to_next_step(self, show: bool = True):
        self.calculate_all_pivots()
        if show:
            self.draw()
        for i in range(self.m):
            if i == self.pivots_string_index:
                continue
            self.b[i] = self.b[i] - self.x[i][self.pivot_column_index] * self.b[self.pivots_string_index] / self.pivot_element
        self.b[self.pivots_string_index] /= self.pivot_element

        self.x = Matrix([
            [self.x[i][j] - self.x[i][self.pivot_column_index] * self.x[self.pivots_string_index][j] / self.pivot_element for j in range(self.n)]
            if i != self.pivots_string_index else
            [self.x[self.pivots_string_index][j] / self.pivot_element for j in range(self.n)]
            for i in range(self.m)
        ])
        self.basic_elements_numbers[self.pivots_string_index] = self.pivot_column_index
        self.calculate_delta()
        if self.delta.get_min() >= 0 and show:
            print("This is it")
            self.draw()
            input()
        else:
            for j in range(self.n):
                if all(self.x[i][j] <= 0 for i in range(self.m)):
                    self.draw()
                    print("""target no function limited from above in ODR""")
                    input()


    def calculate_all_pivots(self):
        self.pivot_column_index = self.delta.get_index_of_min()
        full_column = self.x.get_column(self.pivot_column_index)
        self.reduced_cost = PointVector(*[
            self.b[i] / full_column[i] if full_column[i] else float("inf") for i in range(self.m)
        ])
        self.pivots_string_index = self.reduced_cost.get_index_of_min(0)
        self.pivot_element = self.x[self.pivots_string_index][self.pivot_column_index]


    def calculate_delta(self):
        self.F = sum(self.c[e] * self.b[i] for i, e in enumerate(self.basic_elements_numbers))
        for j in range(self.n):
            full_column = self.x.get_column(j)
            self.delta[j] = sum(self.c[e] * full_column[i] for i, e in enumerate(self.basic_elements_numbers)) - self.c[j]


    def draw(self):
        headers = ["Basis"] + ["C base"] + [f"x{i}" for i in range(self.n)] + ["B"] + ["reduced_cost"]

        rows = []
        for i in range(self.m):
            a = self.basic_elements_numbers[i]
            rows.append([f"A{a}", self.c[a]] + self.x.matrix[i] + [self.b[i], self.reduced_cost[i]])

        # rows.append(["", "F"] + self.c.coordinates)
        rows.append(["", "delta"] + self.delta.coordinates + [self.F])

        print(tabulate(rows, headers=headers, tablefmt="grid"))


def main():
    try:
        n_input, c_input, m_input, x_input, b_input = read_data_from_file("input4.txt")
    except FileNotFoundError as exception:
        print(exception)
        return 0
    except BaseException as exception:
        print("Wrong format of data")
        print(exception)
        return 0

    n, m, basis_elements_numbers, c, x, b = transform_initial_conditions_into_operating_conditions(
        n_input, c_input, m_input, x_input, b_input
    )
    s = SimplexMethod(n, m, basis_elements_numbers, c, x, b)
    while True:
        s.go_to_next_step()

    return 0


if __name__ == "__main__":
    main()
