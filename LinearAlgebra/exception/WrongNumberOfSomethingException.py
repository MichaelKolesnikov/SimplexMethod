from LinearAlgebra.exception.LinearAlgebraException import LinearAlgebraException


class WrongNumberOfSomethingException(LinearAlgebraException):
    def __init__(self, number: int, right_number: int):
        self.name_of_subject = "something"
        self.number = number
        self.right_number = right_number
        super().__init__(f"Wrong number of {self.name_of_subject}, excepted {self.right_number}, got {self.number}")