import numpy as np

class Ray:

    def __init__(self, A: np.ndarray, B: np.ndarray):
        self.A = A
        self.B = B

    def __str__(self):
        return "A = {} B = {}".format(self.A, self.B)

    def origin(self):
        return self.A

    def direction(self):
        return self.B

    def point_at_parameter(self, t: float):
        return self.A + (t * self.B)
