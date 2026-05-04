import slangpy as spy
import math
from utility import *
from camera import camera
from hittable_list import hittable_list
from hittable import *
from material import *


def bouncing_spheres():
    world = hittable_list()

    ground_material = world.add_material(lambertian.from_albedo(world, spy.float3(0.5, 0.5, 0.5)))
    world.add_hittable(sphere.stationary(spy.float3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random_float()
            center = spy.float3(a + 0.9 * random_float(), 0.2, b + 0.9 * random_float())

            if spy.math.length(center - spy.float3(4, 0.2, 0)) > 0.9:
                
                if choose_mat < 0.8:
                    # diffuse
                    albedo = random_float3() * random_float3()
                    sphere_material = world.add_material(lambertian.from_albedo(world, albedo))
                    center2 = center + spy.float3(0.0, random_float(0.0, 0.5), 0.0)
                    world.add_hittable(sphere.moving(center, center2, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo = random_float3(0.5, 1.0)
                    fuzz = random_float(0.0, 0.5)
                    sphere_material = world.add_material(metal.from_albedo(world, albedo, fuzz))
                    world.add_hittable(sphere.stationary(center, 0.2, sphere_material))
                else:
                    sphere_material = world.add_material(dielectric(1.5))
                    world.add_hittable(sphere.stationary(center, 0.2, sphere_material))

    material1 = world.add_material(dielectric(1.5))
    world.add_hittable(sphere.stationary(spy.float3(0, 1, 0), 1.0, material1))

    material2 = world.add_material(lambertian.from_albedo(world, spy.float3(0.4, 0.2, 0.1)))
    world.add_hittable(sphere.stationary(spy.float3(-4, 1, 0), 1.0, material2))

    material3 = world.add_material(metal.from_albedo(world, spy.float3(0.7, 0.6, 0.5), 0.0))
    world.add_hittable(sphere.stationary(spy.float3(4, 1, 0), 1.0, material3))

    world.construct_bvh()

    cam = camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 1600
    cam.max_depth = 50
    cam.background = spy.float3(0.7, 0.8, 1.0)

    cam.vfov = 20
    cam.lookfrom    = spy.float3(13, 2, 3)
    cam.lookat      = spy.float3(0, 0, 0)
    cam.vup         = spy.float3(0, 1, 0)

    cam.defocus_angle = 0.6
    cam.focus_dist = 10.0

    cam.render(world)

def checkered_spheres():
    world = hittable_list()

    checker = world.add_texture(checker_texture.from_colors(world, 0.32, spy.float3(0.2, 0.3, 0.1), spy.float3(0.9, 0.9, 0.9)))

    world.add_hittable(sphere.stationary(spy.float3(0, -10, 0), 10, world.add_material(lambertian(checker))))
    world.add_hittable(sphere.stationary(spy.float3(0, 10, 0), 10, world.add_material(lambertian(checker))))

    cam = camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 1600
    cam.max_depth = 50
    cam.background = spy.float3(0.7, 0.8, 1.0)

    cam.vfov = 20
    cam.lookfrom    = spy.float3(13, 2, 3)
    cam.lookat      = spy.float3(0, 0, 0)
    cam.vup         = spy.float3(0, 1, 0)

    cam.defocus_angle = 0.0

    cam.render(world)

def earth():
    world = hittable_list()

    earth_texture = world.add_texture(image_texture.from_file(world, 'earthmap.jpg'))
    earth_surface = world.add_material(lambertian(earth_texture))
    world.add_hittable(sphere.stationary(spy.float3(0, 0, 0), 2, earth_surface))

    cam = camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 1600
    cam.max_depth = 50
    cam.background = spy.float3(0.7, 0.8, 1.0)

    cam.vfov = 20
    cam.lookfrom    = spy.float3(0, 0, 12)
    cam.lookat      = spy.float3(0, 0, 0)
    cam.vup         = spy.float3(0, 1, 0)

    cam.defocus_angle = 0.0

    cam.render(world)

def perlin_sphere():
    world = hittable_list()

    pertext = world.add_texture(noise_texture(4))
    world.add_hittable(sphere.stationary(spy.float3(0, -1000, 0), 1000, world.add_material(lambertian(pertext))))
    world.add_hittable(sphere.stationary(spy.float3(0, 2, 0), 2, world.add_material(lambertian(pertext))))

    cam = camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 1600
    cam.max_depth = 50
    cam.background = spy.float3(0.7, 0.8, 1.0)

    cam.vfov = 20
    cam.lookfrom    = spy.float3(13, 2, 3)
    cam.lookat      = spy.float3(0, 0, 0)
    cam.vup         = spy.float3(0, 1, 0)

    cam.defocus_angle = 0.0

    cam.render(world)

def quads():
    world = hittable_list()
    
    # Materials
    left_red = world.add_material(lambertian.from_albedo(world, spy.float3(1.0, 0.2, 0.2)))
    back_green = world.add_material(lambertian.from_albedo(world, spy.float3(0.2, 1.0, 0.2)))
    right_blue = world.add_material(lambertian.from_albedo(world, spy.float3(0.2, 0.2, 1.0)))
    upper_orange = world.add_material(lambertian.from_albedo(world, spy.float3(1.0, 0.5, 0.0)))
    lower_teal = world.add_material(lambertian.from_albedo(world, spy.float3(0.2, 0.8, 0.8)))

    # Quads
    world.add_hittable(quad(spy.float3(-3, -2, 5), spy.float3(0, 0, -4), spy.float3(0, 4, 0), left_red))
    world.add_hittable(quad(spy.float3(-2, -2, 0), spy.float3(4, 0, 0), spy.float3(0, 4, 0), back_green))
    world.add_hittable(quad(spy.float3(3, -2, 1), spy.float3(0, 0, 4), spy.float3(0, 4, 0), right_blue))
    world.add_hittable(quad(spy.float3(-2, 3, 1), spy.float3(4, 0, 0), spy.float3(0, 0, 4), upper_orange))
    world.add_hittable(quad(spy.float3(-2, -3, 5), spy.float3(4, 0, 0), spy.float3(0, 0, -4), lower_teal))

    cam = camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 1600
    cam.max_depth = 50
    cam.background = spy.float3(0.7, 0.8, 1.0)

    cam.vfov = 80
    cam.lookfrom    = spy.float3(0, 0, 9)
    cam.lookat      = spy.float3(0, 0, 0)
    cam.vup         = spy.float3(0, 1, 0)

    cam.defocus_angle = 0.0

    cam.render(world)

def simple_light():
    world = hittable_list()

    pertext = world.add_texture(noise_texture(4))
    world.add_hittable(sphere.stationary(spy.float3(0, -1000, 0), 1000, world.add_material(lambertian(pertext))))
    world.add_hittable(sphere.stationary(spy.float3(0, 2, 0), 2, world.add_material(lambertian(pertext))))

    difflight = world.add_material(diffuse_light.from_albedo(world, spy.float3(4, 4, 4)))
    world.add_hittable(sphere.stationary(spy.float3(0, 7, 0), 2, difflight))
    world.add_hittable(quad(spy.float3(3, 1, -2), spy.float3(2, 0, 0), spy.float3(0, 2, 0), difflight))

    cam = camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.image_width = 1600
    cam.max_depth = 50
    cam.background = spy.float3(0, 0, 0)

    cam.vfov = 20
    cam.lookfrom    = spy.float3(26, 3, 6)
    cam.lookat      = spy.float3(0, 2, 0)
    cam.vup         = spy.float3(0, 1, 0)

    cam.defocus_angle = 0.0

    cam.render(world)

if __name__ == "__main__":
    scene = int(input('input scene number:'))
    match scene:
        case 1:
            bouncing_spheres()
        case 2:
            checkered_spheres()
        case 3: 
            earth()
        case 4:
            perlin_sphere()
        case 5:
            quads()
        case 6:
            simple_light()