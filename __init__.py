import numpy as np
from ray import Ray
from math import pow
from hitable import Hitable, hit_record
from sphere import Sphere
from hitable_list import hitable_list
from camera import Camera
from random import random, seed
from time import time_ns
import sys


# def color(r: ray) -> np.ndarray:
#     t = hit_sphere(np.array((0, 0, -1), float), 0.5, r)
#     if t > 0:
#         N = r.point_at_parameter(t) - np.array((0, 0, -1))
#         N = N / np.linalg.norm(N)
#         return 0.5 * (N + 1)
#     direction = r.direction()
#     unit_direction = direction / np.linalg.norm(direction)
#     t = 0.5 * (unit_direction[1] + 1)
#     return (1 - t) * np.array((1, 1, 1), float) + t * np.array((0.5, 0.7, 1), float)


# def color(r: ray, world: Hitable):
#     has_hit, rec = world.hit(r, 0.001, np.inf)
#
#     if has_hit:
#         target = rec.p + rec.normal + random_in_unit_sphere()
#         # TODO hacer iterativo
#         return 0.5 * color(ray.Ray(rec.p, target - rec.p), world)
#     else:
#
#         direction = r.direction()
#         unit_direction = direction / np.linalg.norm(direction)
#         t = 0.5 * (unit_direction[1] + 1)
#         return (1 - t) * np.array((1, 1, 1), float) + t * np.array((0.5, 0.7, 1), float)


def color(r: Ray, world: Hitable):
    has_hit, rec = world.hit(r, 0.001, np.inf)
    count = 0
    while has_hit:
        target = rec.p + rec.normal + random_in_unit_sphere()
        r = Ray(rec.p, target - rec.p)
        has_hit, rec = world.hit(r, 0.001, np.inf)
        count += 1

    direction = r.direction()
    unit_direction = direction / np.linalg.norm(direction)
    t = 0.5 * (unit_direction[1] + 1)
    return pow(0.5, count) * ((1 - t) * np.array((1, 1, 1), float) + t * np.array((0.5, 0.7, 1), float))


# def hit_sphere(center: np.ndarray, radius: float, r: ray) -> float:
#     oc = r.origin() - center
#     a = np.dot(r.direction(), r.direction())
#     b = 2 * np.dot(oc, r.direction())
#     c = np.dot(oc, oc) - radius * radius
#     discriminant = b * b - 4 * a * c
#     if discriminant < 0:
#         return -1
#     else:
#         return (-b - math.sqrt(discriminant)) / (2 * a)

def random_in_unit_sphere():
    norm = 2
    while (norm * norm) >= 1:
        p = 2.0 * np.array((random(), random(), random())) - np.array((1, 1, 1))
        norm = np.linalg.norm(p)
    return p


if __name__ == '__main__':

    # sys.setrecursionlimit(99999)

    f = open("pr.ppm", "w+")
    nx: int = 400
    ny: int = 100
    ns: int = 100

    f.write("P3\n{} {}\n255".format(nx, ny))

    cam = Camera()
    h_list = list()
    h_list.append(Sphere(np.array((0, 0, -1)), 0.5))
    h_list.append(Sphere(np.array((0, -100.5, -1)), 100))
    h_list.append(Sphere(np.array((10, 2, -10)), 2))
    world: Hitable = hitable_list(h_list)
    seed(time_ns())
    t_init = time_ns()
    for j in range(ny, 0, -1):
        for i in range(0, nx):
            col = np.array((0, 0, 0), float)
            for s in range(0, ns):
                u = (i + random()) / nx
                v = (j + random()) / ny
                r = cam.get_ray(u, v)
                p = r.point_at_parameter(2)
                col += color(r, world)

            col = np.sqrt(col / ns) * 255.99
            ir = int(col[0])
            ig = int(col[1])
            ib = int(col[2])

            f.write("\n{} {} {}".format(ir, ig, ib))

    t_end = time_ns()
    total = t_end - t_init
    print("Tiempo total: {}s".format(total * 10 ** -9))
