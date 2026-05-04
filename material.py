import struct
from texture import *

class material:
    def __init__(self):
        self.padding = 0
    
    def pack(self):
        pass

class lambertian(material):
    def __init__(self, tex):
        super().__init__()
        self.tex = tex

    @classmethod
    def from_albedo(cls, world, albedo):
        tex = world.add_texture(solid_color(albedo))
        return cls(tex)

    def pack(self):
        return struct.pack("Iif",
                           0, # material type == 0
                           self.tex,
                           self.padding)

class metal(material):
    def __init__(self, tex, fuzz):
        super().__init__()
        self.tex = tex
        self.fuzz = fuzz

    @classmethod
    def from_albedo(cls, world, albedo, fuzz):
        tex = world.add_texture(solid_color(albedo))
        return cls(tex, fuzz)

    def pack(self):
        return struct.pack("Iif",
                           1, # material type == 1
                           self.tex,
                           self.fuzz)

class dielectric(material):
    def __init__(self, refraction_index):
        super().__init__()
        self.refraction_index = refraction_index

    def pack(self):
        return struct.pack("Iif",
                           2, # material type == 2
                           self.padding,
                           self.refraction_index)
    
class diffuse_light(material):
    def __init__(self, tex):
        super().__init__()
        self.tex = tex

    @classmethod
    def from_albedo(cls, world, albedo):
        tex = world.add_texture(solid_color(albedo))
        return cls(tex)
    
    def pack(self):
        return struct.pack("Iif",
                           3, # material type == 3
                           self.tex,
                           self.padding)