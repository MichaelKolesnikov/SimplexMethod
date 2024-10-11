from LinearAlgebra.exception.LinearAlgebraException import LinearAlgebraException


class WrongNumberOfStringsException(LinearAlgebraException):
    def __init__(self, number_of_columns: int, right_number_of_columns: int):
        self.number_of_columns = number_of_columns
        self.right_number_of_columns = right_number_of_columns
        super().__init__(f"Wrong number of columns, got {self.number_of_columns}, excepted {self.right_number_of_columns}")