import slangpy as spy
import numpy as np
from utility import *

class perlin:
    def __init__(self):
        self.point_count = 256 # This is currently hardcoded to be 256.
        self.randvec = []
        self.perm_x = []
        self.perm_y = []
        self.perm_z = []
        for i in range(self.point_count):
            self.randvec.append(spy.math.normalize(random_float3(-1, 1)))
            self.perm_x.append(0)
            self.perm_y.append(0)
            self.perm_z.append(0)
        self.perlin_generate_perm(self.perm_x)
        self.perlin_generate_perm(self.perm_y)
        self.perlin_generate_perm(self.perm_z)

    def perlin_generate_perm(self, p: list):
        for i in range(self.point_count):
            p[i] = i

        self.permute(p, self.point_count)

    def permute(self, p: list, n: int):
        for i in range(n - 1, 0, -1):
            target = random_int(0, i)
            tmp = p[i]
            p[i] = p[target]
            p[target] = tmp