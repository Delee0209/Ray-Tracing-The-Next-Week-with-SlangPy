import slangpy as spy
import numpy as np
import struct
from aabb import *
from hittable import *
from material import *
from texture import *
from perlin import *

class hittable_list:
    def __init__(self):
        self.objects = []
        self.object_count = 0
        self.appearances = []
        self.colors = []
        self.images = []
        self.use_bvh = False
        self.perlin = perlin()
        self.bbox = aabb()

        self.add_material(lambertian.from_albedo(self, spy.float3(1.0)))

    def add_material(self, appearance):
        mat = len(self.appearances)
        self.appearances.append(appearance)
        return mat

    def add_hittable(self, object):
        self.objects.append(object)
        self.bbox = aabb.from_aabbs(self.bbox, object.bounding_box())
        self.object_count += 1

    def add_texture(self, color):
        tex = len(self.colors)
        self.colors.append(color)
        return tex
    
    def add_image(self, image):
        img = len(self.images)
        self.images.append(image)
        return img

    def add_node(self, node):
        node_id = len(self.objects)
        self.objects.append(node)
        return node_id

    def bounding_box(self):
        return self.bbox
    
    def construct_bvh(self):
        self.use_bvh = True
        self.add_node(bvh_node.construct(self, 0, self.object_count))


    def prepare(self, device: spy.Device):
        # Prepare hittable data
        object_data = np.frombuffer(b"".join(object.pack() for object in self.objects), dtype = np.uint8).flatten()
        self.object_buffer = device.create_buffer(usage = spy.BufferUsage.shader_resource,
                                                  label = "object_buffer",
                                                  data = object_data)
        # Prepare material data
        appearance_data = np.frombuffer(b"".join(appearance.pack() for appearance in self.appearances), dtype = np.uint8).flatten()
        self.appearance_buffer = device.create_buffer(usage = spy.BufferUsage.shader_resource,
                                                      label = "appearance_buffer",
                                                      data = appearance_data)
        
        # Prepare texture data
        color_data = np.frombuffer(b"".join(color.pack() for color in self.colors), dtype = np.uint8).flatten()
        self.color_buffer = device.create_buffer(usage = spy.BufferUsage.shader_resource,
                                                 label = "color_buffer",
                                                 data = color_data)
        
        # Prepare image data
        loader = spy.TextureLoader(device)
        for i in range(len(self.images)):
            filename = self.images[i]
            self.images[i] = loader.load_texture(filename)
        if len(self.images) == 0:
            img = np.ones(shape = (2, 2, 4), dtype = np.float32)
            image = device.create_texture(width = 2,
                                            height = 2,
                                            format = spy.Format.rgba32_float,
                                            usage = spy.TextureUsage.shader_resource,
                                            data = img)
            self.images.append(image)
        image_data = np.asarray([image.create_view().descriptor_handle_ro.value for image in self.images], dtype = np.uint64)
        self.image_buffer = device.create_buffer(usage = spy.BufferUsage.shader_resource,
                                                   label = "image_buffer",
                                                   data = image_data)
        
        # setup sampler
        self.sampler = device.create_sampler(min_filter = spy.TextureFilteringMode.linear,
                                             mag_filter = spy.TextureFilteringMode.linear,
                                             address_u = spy.TextureAddressingMode.wrap,
                                             address_v = spy.TextureAddressingMode.wrap)
        
        perlin_data = np.frombuffer(b"".join(struct.pack("fff", i.x, i.y, i.z) for i in self.perlin.randvec), dtype = np.uint8).flatten()
        self.perlin_buffer = device.create_buffer(usage = spy.BufferUsage.shader_resource,
                                                  label = "perlin_buffer",
                                                  data = perlin_data)
        
    def bind(self, cursor: spy.ShaderCursor):
        cursor["use_bvh"]       = self.use_bvh
        cursor["bvh_root"]      = len(self.objects) - 1
        cursor["object_count"]  = self.object_count
        cursor["objects"]       = self.object_buffer
        cursor["appearances"]   = self.appearance_buffer
        cursor["colors"]        = self.color_buffer

    def bind_perlin(self, cursor: spy.ShaderCursor):
        cursor["randvec"]       = self.perlin_buffer
        cursor["perm_x"]        = np.array(self.perlin.perm_x, dtype = np.int32)
        cursor["perm_y"]        = np.array(self.perlin.perm_y, dtype = np.int32)
        cursor["perm_z"]        = np.array(self.perlin.perm_z, dtype = np.int32)