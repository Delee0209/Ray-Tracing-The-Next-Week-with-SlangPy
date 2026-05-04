import slangpy as spy
import struct

class texture:
    def __init__(self):
        self.padding = 0

    def pack(self):
        pass

class solid_color(texture):
    def __init__(self, albedo = spy.float3(1.0)):
        super().__init__()
        self.albedo = albedo

    def pack(self):
        return struct.pack("Ifffii",
                           0,
                           self.albedo[0], self.albedo[1], self.albedo[2],
                           self.padding, self.padding)
    
class checker_texture(texture):
    def __init__(self, scale: float, t1: int, t2: int):
        super().__init__()
        self.scale = scale
        self.t1 = t1
        self.t2 = t2

    @classmethod
    def from_colors(cls,
                    world,
                    scale: float, 
                    c1: spy.float3, 
                    c2: spy.float3):
        t1 = world.add_texture(solid_color(c1))
        t2 = world.add_texture(solid_color(c2))
        return cls(scale, t1, t2)
    
    def pack(self):
        return struct.pack("Ifffii",
                           1,
                           self.scale, self.padding, self.padding,
                           self.t1, self.t2)
    
class image_texture(texture):
    def __init__(self, img: int):
        super().__init__()
        self.img = img

    @classmethod
    def from_file(cls, world, filename: str):
        img = world.add_image(filename)
        return cls(img)
    
    def pack(self):
        return struct.pack("Ifffii",
                           2,
                           self.padding, self.padding, self.padding,
                           self.img, self.padding)
    
class noise_texture(texture):
    def __init__(self, scale: float):
        super().__init__()
        self.scale = scale
        
    def pack(self):
        return struct.pack("Ifffii",
                           3,
                           self.scale, self.padding, self.padding,
                           self.padding, self.padding)