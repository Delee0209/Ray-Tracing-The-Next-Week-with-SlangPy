from interval import *
import slangpy as spy

class aabb:
    def __init__(self,
                 x = interval(),
                 y = interval(),
                 z = interval()):
        self.x = x
        self.y = y
        self.z = z

        self.pad_to_minimus()

    @classmethod
    def from_points(cls,
                    a = spy.float3(0.0),
                    b = spy.float3(0.0)):
        x = interval(a.x, b.x) if a.x <= b.x else interval(b.x, a.x)
        y = interval(a.y, b.y) if a.y <= b.y else interval(b.y, a.y)
        z = interval(a.z, b.z) if a.z <= b.z else interval(b.z, a.z)
        return cls(x, y, z)
    
    @classmethod
    def from_aabbs(cls, box0, box1):
        x = interval.merge(box0.x, box1.x)
        y = interval.merge(box0.y, box1.y)
        z = interval.merge(box0.z, box1.z)
        return cls(x, y, z)
    
    def axis_interval(self, n: int):
        if n == 1:
            return self.y
        if n == 2:
            return self.z
        return self.x
    
    def pad_to_minimus(self):
        # Adjust the AABB so that no side is narrower than some delta, padding if necessary

        delta = 0.0001
        if self.x.size() < delta:
            self.x.expand(delta)
        if self.y.size() < delta:
            self.y.expand(delta)
        if self.z.size() < delta:
            self.z.expand(delta)
    
    def longest_axis(self):
        # Return the index of the longest axis of the bounding box.
        
        if self.x.size() > self.y.size():
            return 0 if self.x.size() > self.z.size() else 2
        else:
            return 1 if self.y.size() > self.z.size() else 2