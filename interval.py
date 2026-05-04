# a python copy of the interval class, for BVH implementation
import slangpy as spy
import numpy as np
import math

class interval:
    def __init__(self, min: float = math.inf, max: float = -math.inf):
        self.min = min
        self.max = max

    @classmethod
    def merge(cls, a, b):
        min = a.min if a.min <= b.min else b.min
        max = a.max if a.max >= b.max else b.max
        return cls(min, max)

    def size(self):
        return self.max - self.min
    
    def contains(self, x: float):
        return self.min <= x <= self.max
    
    def surrounds(self, x: float):
        return self.min < x < self.max
    
    def clamp(self, x: float):
        if x < self.min:
            return self.min
        if x > self.max:
            return self.max
        return x
    
    def clamp(self, x: spy.float3):
        return spy.float3(self.clamp(x.x), self.clamp(x.y), self.clamp(x.z))
    
    def expand(self, delta: float):
        padding = float(delta / 2.0)
        return interval(self.min - padding, self.max + padding)

empty = interval(math.inf, -math.inf)
universe = interval(-math.inf, math.inf)