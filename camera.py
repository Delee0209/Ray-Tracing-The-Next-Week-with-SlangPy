import slangpy as spy
import math
from app import App
from hittable_list import hittable_list
from utility import *

class camera:
    def __init__(self,
                 aspect_ratio: float = 1.0,
                 image_width: int = 100,
                 max_depth: int = 10,
                 vfov: float = 90,
                 lookfrom   = spy.float3(0, 0, 0),
                 lookat     = spy.float3(0, 0, -1),
                 vup        = spy.float3(0, 1, 0),
                 defocus_angle: float = 0,
                 focus_dist: float = 10,
                 background = spy.float3(1.0, 1.0, 1.0)):
        self.aspect_ratio = aspect_ratio    # Ratio of image width over height
        self.image_width = image_width      # Rendered image width in pixel count
        self.max_depth = max_depth          # Maximum number of ray bounces into scene
        self.frame_number = 0               # Current frame number, basically equals to sample_per_pixel in the original book
        self.vfov = vfov                    # Vertical view angle (field of view)
        self.lookfrom = lookfrom            # Point camera is looking from
        self.lookat = lookat                # POint camera is looking at
        self.vup = vup                      # Camera-relative "up" direction
        self.defocus_angle = defocus_angle  # Variation angle of rays through each pixel
        self.focus_dist = focus_dist        # Distance from camera lookfrom point to plane of perfect focus
        self.background = background
    
    def initialize(self):
        # Calculate the image height, and ensure that it's at least 1.
        self.image_height = max(int(self.image_width / self.aspect_ratio), 1)

        self.center = self.lookfrom

        # Determine viewport dimensions
        theta = degree_to_radians(self.vfov)
        h = math.tan(theta / 2)
        viewport_height = 2.0 * h * self.focus_dist
        viewport_width = viewport_height * (float(self.image_width) / float(self.image_height))

        # Calculate the u,v,w unit basis vectors for the camera coordinate frame
        w = spy.math.normalize(self.lookfrom - self.lookat)
        u = spy.math.normalize(spy.math.cross(self.vup, w))
        v = spy.math.cross(w, u)

        # Calculate the vectors across the horizontal and down the vertical viewport edges.
        viewport_u = viewport_width * u     # Vector across viewport horizontal edge
        viewport_v = viewport_height * -v   # Vector across viewport vertical edge

        # Calculate the horizontal and vertical delta vectors from pixel to pixel.
        self.pixel_delta_u = viewport_u / self.image_width
        self.pixel_delta_v = viewport_v / self.image_height

        # Calculate the location of the upper left pixel.
        viewport_upper_left = self.center - (self.focus_dist * w) - viewport_u / 2.0 - viewport_v / 2.0
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)

        # Calculate the camera defocus disk basis vectors.
        defocus_radius = self.focus_dist * math.tan(degree_to_radians(self.defocus_angle / 2.0))
        self.defocus_disk_u = u * defocus_radius
        self.defocus_disk_v = v * defocus_radius

    def bind(self, cursor: spy.ShaderCursor):
        cursor["image_height"]      = self.image_height
        cursor["image_width"]       = self.image_width
        cursor["max_depth"]         = self.max_depth
        cursor["frame_number"]      = self.frame_number
        cursor["background"]        = self.background
        cursor["center"]            = self.center
        cursor["pixel00_loc"]       = self.pixel00_loc
        cursor["pixel_delta_u"]     = self.pixel_delta_u
        cursor["pixel_delta_v"]     = self.pixel_delta_v
        cursor["defocus_disk_u"]    = self.defocus_disk_u
        cursor["defocus_disk_v"]    = self.defocus_disk_v
        cursor["defocus_angle"]     = self.defocus_angle

    def render(self, world: hittable_list):
        self.initialize()

        # setup app - display window
        app = App(title = 'SlangPy RTTNW', 
                width = self.image_width, height = self.image_height, 
                gui = False, resizable = False,
                frame_format = spy.Format.rgba32_float, display_format = spy.Format.rgba8_unorm)
        device = app.device
        
        # prepare hittable list data
        world.prepare(device)
        
        # setup render function - load shader, shader dispatch
        program = device.load_program(module_name="shaders/kernel.slang", entry_point_names=["render"])
        pipeline = device.create_compute_pipeline(program)
        def render(app: App):
            with app.command_encoder.begin_compute_pass() as pass_encoder:
                shader_object = pass_encoder.bind_pipeline(pipeline)
                cursor = spy.ShaderCursor(shader_object)
                self.bind(cursor.cam)
                world.bind(cursor.world)
                world.bind_perlin(cursor.noise)
                cursor.images = world.image_buffer
                cursor.sampler = world.sampler
                cursor.image = app.frame
                pass_encoder.dispatch(thread_count = [self.image_width, self.image_height, 1])
            self.frame_number += 1
        app.render = render # hooking render function to app's render function

        # launch app
        app.run()