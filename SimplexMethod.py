from tabulate import tabulate
import copy
from LinearAlgebra import PointVector, Matrix


class SimplexMethod[T]:
    @staticmethod
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
        self.is_solved()

        self.pivot_column_index: int = 0
        self.pivots_string_index: int = 0
        self.pivot_element: T = 0

    def change_x(self):
        self.x = Matrix([
            [self.x[i][j] - self.x[i][self.pivot_column_index] * self.x[self.pivots_string_index][
                j] / self.pivot_element for j in range(self.n)]
            if i != self.pivots_string_index else
            [self.x[self.pivots_string_index][j] / self.pivot_element for j in range(self.n)]
            for i in range(self.m)
        ])

    def change_b(self):
        for i in range(self.m):
            if i == self.pivots_string_index:
                continue
            self.b[i] = self.b[i] - self.x[i][self.pivot_column_index] * self.b[self.pivots_string_index] / self.pivot_element
        self.b[self.pivots_string_index] /= self.pivot_element

    def go_to_next_step(self):
        self.calculate_all_pivots()
        self.draw()
        self.change_b()
        self.change_x()
        self.basic_elements_numbers[self.pivots_string_index] = self.pivot_column_index
        self.calculate_delta()
        self.is_solved()

    def is_solved(self):
        if self.delta.get_max() <= 0:
            print("This is it")
            self.draw()
            input()
        else: # exists delta[j] > 0 in this case
            for j in range(self.n):
                if self.delta[j] > 0 and all(self.x[i][j] <= 0 for i in range(self.m)):
                    self.draw()
                    print("""target no function limited from above in ODR""")
                    input()

    def calculate_all_pivots(self):
        self.pivot_column_index = self.delta.get_index_of_max()
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
            self.delta[j] = self.c[j] - sum(self.c[e] * full_column[i] for i, e in enumerate(self.basic_elements_numbers))


    def draw(self):
        headers = ["Basis"] + ["C base"] + [f"x{i}" for i in range(self.n)] + ["B"] + ["reduced_cost"]

        rows = []
        for i in range(self.m):
            a = self.basic_elements_numbers[i]
            rows.append([f"A{a}", self.c[a]] + self.x.matrix[i] + [self.b[i], self.reduced_cost[i]])

        rows.append(["", "delta"] + self.delta.coordinates + [self.F])
        rows.append(["", "c"] + self.c.coordinates)

        print(tabulate(rows, headers=headers, tablefmt="grid"))
