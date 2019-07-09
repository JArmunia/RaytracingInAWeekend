import numpy as np


class Vec3:
    e = np.ndarray(shape=3, dtype=float)

    def __init__(self, e0: float, e1: float, e2: float):
        self.e[0] = e0
        self.e[1] = e1
        self.e[2] = e2

    def __str__(self):
        return str(self.e)

    def x(self):
        return self.e[0]

    def y(self):
        return self.e[1]

    def z(self):
        return self.e[2]

    def r(self):
        return self.e[0]

    def g(self):
        return self.e[1]

    def b(self):
        return self.e[2]

    def length(self):
        return np.linalg.norm(self.e)

    def make_unit_vector(self):
        self.e = self.e / self.length()


a = Vec3(2, 3, 4)

print(a.e)

a.make_unit_vector()
print(a)
print(a.length())
