import numpy as np
import ray


class Camera:
    def __init__(self, lower_left_corner: np.ndarray = np.array((-2, -1, -1)),
                 horizontal: np.ndarray = np.array((4, 0, 0)),
                 vertical: np.ndarray = np.array((0, 2, 0)),
                 origin: np.ndarray = np.array((0, 0, 0))):
        self.lower_left_corner = lower_left_corner
        self.horizontal = horizontal
        self.vertical = vertical
        self.origin = origin

    def get_ray(self, u: float, v: float) -> ray.Ray:
        return ray.Ray(self.origin, self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin)
