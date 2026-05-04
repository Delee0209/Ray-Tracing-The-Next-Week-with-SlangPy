import slangpy as spy
import struct
from utility import *
from aabb import *

class hittable:
    def __init__(self, mat: int = 0):
        self.mat = mat
        self.padding = 0
        self.bbox = None

    def bounding_box(self):
        return self.bbox

    def pack(self):
        pass

class sphere(hittable):
    def __init__(self, 
                 center1 = spy.float3(0.0, 0.0, 0.0),
                 center2 = spy.float3(0.0, 0.0, 0.0),
                 radius: float = 1.0,
                 mat: int = 0,
                 bbox = aabb()):
        super().__init__(mat)
        self.center1 = center1
        self.center2 = center2
        self.radius = radius
        self.bbox = bbox

    @classmethod
    def moving(cls,
               center1 = spy.float3(0.0, 0.0, 0.0),
               center2 = spy.float3(0.0, 0.0, 0.0),
               radius: float = 1.0,
               mat: int = 0):
        rvec = spy.float3(radius, radius, radius)
        box1 = aabb.from_points(center1 - rvec, center1 + rvec)
        box2 = aabb.from_points(center2 - rvec, center2 + rvec)
        bbox = aabb.from_aabbs(box1, box2)
        return cls(center1, center2, radius, mat, bbox)
    
    @classmethod
    def stationary(cls,
                   center = spy.float3(0.0, 0.0, 0.0),
                   radius: float = 1.0,
                   mat: int = 0):
        rvec = spy.float3(radius, radius, radius)
        bbox = aabb.from_points(center - rvec, center + rvec)
        return cls(center, center, radius, mat, bbox)

    def pack(self):
        return struct.pack("Iffffffffffii",
                           1,
                           self.center1[0], self.center1[1], self.center1[2],
                           self.center2[0], self.center2[1], self.center2[2],
                           self.padding, self.padding, self.padding,
                           self.radius,
                           self.mat, self.padding)
    
class quad(hittable):
    def __init__(self, 
                 Q: spy.float3,
                 u: spy.float3,
                 v: spy.float3,
                 mat = 0):
        super().__init__(mat)
        self.Q = Q
        self.u = u
        self.v = v
        self.bbox = aabb()
        self.set_bounding_box()

    def set_bounding_box(self):
        # Compute the bounding box of all four vertices.
        bbox_diagonal1 = aabb.from_points(self.Q, self.Q + self.u + self.v)
        bbox_diagonal2 = aabb.from_points(self.Q + self.u, self.Q + self.v)
        self.bbox = aabb.from_aabbs(bbox_diagonal1, bbox_diagonal2)

    def pack(self):
        return struct.pack("Iffffffffffii",
                           2,
                           self.Q[0], self.Q[1], self.Q[2],
                           self.u[0], self.u[1], self.u[2],
                           self.v[0], self.v[1], self.v[2],
                           self.padding,
                           self.mat, self.padding)
    
class bvh_node(hittable):
    def __init__(self,
                 left: int = -1,
                 right: int = -1,
                 bbox = aabb(), 
                 mat = 0):
        super().__init__(mat)
        self.left = left
        self.right = right
        self.bbox = bbox

    # another changes required for c++ to python
    def box_compare(self, 
                    a: hittable, 
                    axis_index: int):
        a_axis_interval = a.bounding_box().axis_interval(axis_index)
        return a_axis_interval.min
    
    def box_x_compare(self, a):
        return self.box_compare(a, 0)
    
    def box_y_compare(self, a):
        return self.box_compare(a, 1)
    
    def box_z_compare(self, a):
        return self.box_compare(a, 2)

    @classmethod
    def construct(cls, world, start, end):
        cur = cls()
        
        for i in range(start, end):
            cur.bbox = aabb.from_aabbs(cur.bbox, world.objects[i].bounding_box())
            
        axis = cur.bbox.longest_axis()

        comparator = None
        if axis == 0:
            comparator = cur.box_x_compare
        if axis == 1:
            comparator = cur.box_y_compare
        if axis == 2:
            comparator = cur.box_z_compare

        object_span = end - start

        if object_span == 1:
            cur.right = start
            cur.left = start
        elif object_span == 2:
            cur.left = start
            cur.right = start + 1
        else:
            objects = world.objects[start : end]
            objects.sort(key = comparator)

            mid = start + int(object_span / 2)
            cur.left = world.add_node(cls.construct(world, start, mid))
            cur.right = world.add_node(cls.construct(world, mid, end))

        return cur

    def pack(self):
        return struct.pack("Iffffffffffii",
                           0,
                           self.bbox.x.min, self.bbox.y.min, self.bbox.z.min,
                           self.bbox.x.max, self.bbox.y.max, self.bbox.z.max,
                           self.padding, self.padding, self.padding,
                           self.padding,
                           self.left, self.right)

    

    