from LinearAlgebra import PointVector, Matrix
from SimplexMethod import SimplexMethod


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


def main():
    find_max = 0
    try:
        n_input, c_input, m_input, x_input, b_input = read_data_from_file("input2.txt")
    except FileNotFoundError as exception:
        print(exception)
        return 0
    except BaseException as exception:
        print("Wrong format of data")
        print(exception)
        return 0
    if not find_max:
        c_input = -c_input

    s = SimplexMethod(
        *SimplexMethod.transform_initial_conditions_into_operating_conditions(
            n_input, c_input, m_input, x_input, b_input
        )
    )
    while True:
        s.go_to_next_step()

    return 0


if __name__ == "__main__":
    main()
