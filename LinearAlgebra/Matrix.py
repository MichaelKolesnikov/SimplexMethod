import copy
from .PointVector import PointVector
from .exception.WrongNumberOfColumnsException import WrongNumberOfColumnsException
from .exception.WrongNumberOfStringsException import WrongNumberOfStringsException


class Matrix[T]:
    def __init__(self, matrix: list[list[T]]):
        self.m = len(matrix) # count of strings
        self.n = 0 # count of columns
        if self.m == 0:
            self.n = 0
            return
        self.n = len(matrix[0])
        self.matrix = matrix

    def swap_strings(self, i, j):
        self.matrix[i], self.matrix[j] = self.matrix[j], self.matrix[i]

    def __str__(self):
        s = ""
        for i in self.matrix:
            s += " ".join(str(j) for j in i) + '\n'
        return s

    def subtract_rows(self, i1, i2, k):
        for i in range(self.m):
            self.matrix[i1][i] -= self.matrix[i2][i] * k

    def det(self):
        if self.m == 1:
            return self.matrix[0][0]
        i = 0
        if self.matrix[0][0] == 0:
            while i < self.m and not self.matrix[i][0]:
                print(self.matrix[i][0])
                i += 1
            if i == self.m:
                return 0
            self.swap_strings(0, i)
        i += 1
        for j in range(i, self.m):
            if self.matrix[j][0]:
                k = self.matrix[j][0] / self.matrix[0][0]
                self.subtract_rows(j, 0, k)
        matrix_ = Matrix([self.matrix[i1][1:] for i1 in range(1, self.m)])
        return self.matrix[0][0] * matrix_.det()

    def dot(self, other):
        if isinstance(other, Matrix):
            c2 = list(zip(*other.matrix))
            l_list: list = [[0 for _c in range(self.n)] for _s in range(self.m)]
            for i in range(self.m):
                for j in range(other.n):
                    l_list[i][j] = sum(map(lambda x: x[0] * x[1], list(zip(self.matrix[i], c2[j]))))

            result = Matrix(l_list)
            return result
        if isinstance(other, int):
            result = Matrix(self.matrix)
            for i in range(self.m):
                for j in range(self.n):
                    result.matrix[i][j] *= other
            return result

    def __mul__(self, other):
        return Matrix([[self.matrix[i][j] * other.matrix[i][j] for j in range(self.n)] for i in range(self.m)])

    def scalar_mul(self, other):
        m = self.__mul__(other).matrix
        return sum([sum(i) for i in m])

    def transport(self):
        return Matrix([[self.matrix[j][i] for j in range(self.m)] for i in range(self.n)])

    def __getitem__(self, item) -> PointVector[T]:
        return PointVector(*copy.deepcopy(self.matrix[item]))

    def to_vector_or_none(self) -> PointVector[T] | None:
        if self.m == 1:
            return PointVector(self.matrix[0])
        elif self.n == 1:
            return PointVector([self.matrix[0][i] for i in range(self.m)])
        return None

    def add_string(self, string: list[T]):
        if len(string) != self.n:
            raise WrongNumberOfColumnsException(len(string), self.n)
        self.matrix.append(string)
        self.m += 1

    def add_column(self, column: list[T]):
        if len(column) != self.m:
            raise WrongNumberOfStringsException(len(column), self.m)
        for i in range(self.m):
            self.matrix[i].append(column[i])
        self.n += 1

    def get_column(self, column_number) -> PointVector[T]:
        if not (0 <= column_number < self.n):
            raise Exception(f"Wrong index {column_number}, count of columns={self.n}")
        return PointVector(*[self.matrix[i][column_number] for i in range(self.m)])

def bin_exp(x: int | float | Matrix, degree: int) -> int | float | Matrix:
    if degree == 0:
        if isinstance(x, Matrix):
            return Matrix([[1 if i == j else 0 for j in range(x.n)] for i in range(x.m)])
        return 1
    elif degree == 1:
        return x
    x_ = bin_exp(x, degree // 2)
    return x_ * x_ * bin_exp(x, degree % 2)


def get_fib_num(n: int):
    matrix = bin_exp(Matrix([[0, 1], [1, 1]]), n).dot(Matrix([[0], [1]]))
    return matrix.matrix[0][0]


def getter_fib_numbers(ind=1):
    while True:
        yield get_fib_num(ind)
        ind += 1


def get_gram_matrix(a: Matrix, b: Matrix):
    a = a.transport()
    b = b.transport()
    n = a.m
    return Matrix([[a[i].scalar_mul(a[j]) if j < n else a[i].scalar_mul(b) for j in range(n + 1)] for i in range(n)])
