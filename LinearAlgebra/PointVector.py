import math
from typing import Union
from fractions import Fraction

class PointVector[T = float]:
    def __init__(self, *coordinates: T):
        self.coordinates: list[T] = list(coordinates)

    def __str__(self) -> str:
        return f"PointVector{self.coordinates}"

    def __repr__(self) -> str:
        return f"PointVector{self.coordinates}"

    def __len__(self) -> int:
        return len(self.coordinates)

    def __getitem__(self, index: int) -> T:
        return self.coordinates[index]

    def __setitem__(self, key, value) -> "PointVector[T]":
        self.coordinates[key] = value
        return self

    def __add__(self, other: "PointVector[T]") -> "PointVector[T]":
        if len(self) != len(other):
            raise ValueError("Dimensions of vectors do not match")
        return PointVector(*(x + y for x, y in zip(self.coordinates, other.coordinates)))

    def __sub__(self, other: "PointVector") -> "PointVector":
        if len(self) != len(other):
            raise ValueError("Dimensions of vectors do not match")
        return PointVector(*(x - y for x, y in zip(self.coordinates, other.coordinates)))

    def __mul__(self, factor: Union[T, "PointVector"]) -> Union[T, "PointVector"]:
        if isinstance(factor, float) or isinstance(factor, int):
            return PointVector(*(x * factor for x in self.coordinates))
        return sum([i * j for i, j in zip(self.coordinates, factor.coordinates)])

    def __rmul__(self, scalar: T) -> "PointVector":
        return self.__mul__(scalar)

    def __truediv__(self, scalar: T) -> "PointVector":
        return PointVector(*(x / scalar for x in self.coordinates))

    def __eq__(self, other: "PointVector[T]") -> bool:
        return self.coordinates == other.coordinates

    def __ne__(self, other: "PointVector[T]") -> bool:
        return not self.__eq__(other)

    def __getattr__(self, name: str) -> T:
        if name in ('x', 'y', 'z'):
            index = ord(name) - ord('x')
            if index >= len(self.coordinates):
                raise AttributeError(f"Point has no attribute '{name}'")
            return self.coordinates[index]
        elif name == "coordinates":
            return self.__dict__["coordinates"]
        raise AttributeError(f"Point has no attribute '{name}'")

    def __setattr__(self, name: str, value: T) -> T:
        if name in ('x', 'y', 'z'):
            index = ord(name) - ord('x')
            if index >= len(self.coordinates):
                raise AttributeError(f"Point has no attribute '{name}'")
            self.coordinates[index] = value
            return self.coordinates[index]
        elif name == "coordinates":
            self.__dict__["coordinates"] = value
            return self.__dict__["coordinates"]
        raise AttributeError(f"Point has no attribute '{name}'")

    def __hash__(self) -> int:
        return hash(tuple(self.coordinates))

    def __neg__(self):
        return PointVector(*(-x for x in self.coordinates))

    def get_min(self) -> T:
        return min(self.coordinates)

    def get_max(self) -> T:
        return max(self.coordinates)

    def magnitude(self) -> float:
        return math.sqrt(sum(x ** 2 for x in self.coordinates))

    def normalize(self) -> "PointVector[T]":
        mag = self.magnitude()
        return PointVector(*(x / mag for x in self.coordinates))

    def dot_product(self, other: "PointVector") -> T:
        if len(self) != len(other):
            raise ValueError("Dimensions of vectors do not match")
        return sum(x * y for x, y in zip(self.coordinates, other.coordinates))

    def cross_product(self, other: "PointVector") -> "PointVector":
        if len(self) != 3 or len(other) != 3:
            raise ValueError("Cross product is defined only for 3-dimensional vectors")
        x = self.coordinates[1] * other.coordinates[2] - self.coordinates[2] * other.coordinates[1]
        y = self.coordinates[2] * other.coordinates[0] - self.coordinates[0] * other.coordinates[2]
        z = self.coordinates[0] * other.coordinates[1] - self.coordinates[1] * other.coordinates[0]
        return PointVector(x, y, z)

    def distance(self, other: "PointVector[T]") -> T:
        return (self - other).magnitude()

    def get_rotated(self, angle: float) -> "PointVector":
        assert len(self.coordinates) > 1
        x = self.coordinates[0]
        y = self.coordinates[1]
        cos_ = math.cos(angle)
        sin_ = math.sin(angle)
        return PointVector(x * cos_ - y * sin_, x * sin_ + y + cos_)

    def get_index_of_min(self, min_need_value: float = -float("inf")) -> int:
        ind: int = 0
        while ind < len(self):
            if self.coordinates[ind] >= min_need_value:
                break
            ind += 1
        else:
            return -1
        for i in range(1, len(self.coordinates)):
            if self.coordinates[ind] > self.coordinates[i] >= min_need_value:
                ind = i
        return ind

    def get_index_of_max(self) -> int:
        ind: int = 0
        for i in range(1, len(self.coordinates)):
            if self.coordinates[i] > self.coordinates[ind]:
                ind = i
        return ind
