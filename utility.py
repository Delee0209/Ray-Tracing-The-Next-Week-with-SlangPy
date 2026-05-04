import math
import slangpy as spy
import numpy as np

def degree_to_radians(degrees):
    return degrees * math.pi / 180.0

def random_float(min: float = 0.0, max: float = 1.0):
    return np.random.uniform(min, max)

def random_float3(min: float = 0.0, max: float = 1.0):
    return spy.float3(random_float(min, max), random_float(min, max), random_float(min, max))

def random_int(min: int, max: int):
    return int(random_float(min, max + 1))