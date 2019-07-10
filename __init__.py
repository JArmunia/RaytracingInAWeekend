import numpy as np
from ray import Ray
from math import pow
from hitable import Hitable, hit_record
from sphere import Sphere
from hitable_list import hitable_list
from camera import Camera
from random import random, seed
from time import time_ns
import material
import sys


def color(r: Ray, world: Hitable):
    has_hit, rec = world.hit(r, 0.001, np.inf)
    depth = 0
    attenuation = 1
    while has_hit:

        has_scattered, attenuation, scattered = rec.material.scatter(r, rec)
        if (depth < 50) and has_scattered:
            has_hit, rec = world.hit(scattered, 0.001, np.inf)
        else:
            return np.array((0, 0, 0))

        depth += 1

    direction = r.direction()
    unit_direction = direction / np.linalg.norm(direction)
    t = 0.5 * (unit_direction[1] + 1)
    return np.power(attenuation, depth) * ((1 - t) * np.array((1, 1, 1), float) + t * np.array((0.5, 0.7, 1), float))


def color(r: Ray, world: Hitable, depth: int):
    has_hit, rec = world.hit(r, 0.001, np.inf)
    if has_hit:
        has_scattered, attenuation, scattered = rec.material.scatter(r, rec)
        if (depth < 50) and has_scattered:
            return attenuation * color(scattered, world, depth + 1)
        else:
            return np.array((0, 0, 0), float)

    else:
        direction = r.direction()
        unit_direction = direction / np.linalg.norm(direction)
        t = 0.5 * (unit_direction[1] + 1)
        return (1 - t) * np.array((1, 1, 1), float) + t * np.array((0.5, 0.7, 1.0))


if __name__ == '__main__':

    # sys.setrecursionlimit(99999)
    args = sys.argv
    f = open(args[1], "w+")
    nx: int = 200
    ny: int = 100
    ns: int = 20

    f.write("P3\n{} {}\n255".format(nx, ny))

    cam = Camera()
    h_list = list()
    h_list.append(Sphere(np.array((0, 0, -1)), 0.5, material.lambertian(np.array((0.1, 0.2, 0.5)))))
    h_list.append(Sphere(np.array((0, -100.5, -1)), 100, material.lambertian(np.array((0.8, 0.8, 0)))))
    h_list.append(Sphere(np.array((1, 0, -1)), 0.5, material.metal(np.array((0.8, 0.6, 0.2)), 0.3)))
    h_list.append(Sphere(np.array((-1, 0, -1)), 0.5, material.dielectric(1.5)))
    h_list.append(Sphere(np.array((-5, 2.5, -5)), 2, material.lambertian(np.array((0.1, 0.2, 0.5)))))
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
                col += color(r, world, 0)

            col = np.sqrt(col / ns) * 255.99
            ir = int(col[0])
            ig = int(col[1])
            ib = int(col[2])

            f.write("\n{} {} {}".format(ir, ig, ib))
        print("{}% ({}/{})".format(100 * (ny - j) / ny, ny - j, ny))

    t_end = time_ns()
    total = t_end - t_init
    print("Tiempo total: {}s".format(total * 10 ** -9))
