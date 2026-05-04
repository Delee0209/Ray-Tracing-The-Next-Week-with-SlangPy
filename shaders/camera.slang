import utility;
import interval;
import ray;
import hittable;
import material;
import hittable_list;


struct camera
{
    uint image_height;
    uint image_width;
    uint max_depth;
    uint frame_number;
    float3 background;
    float3 center;
    float3 pixel00_loc;
    float3 pixel_delta_u;
    float3 pixel_delta_v;
    float3 defocus_disk_u;
    float3 defocus_disk_v;
    float defocus_angle;

    float3 sample_square(inout RNG rng)
    {
        return float3(random_float(rng) - 0.5, random_float(rng) - 0.5, 0.f);
    }

    float3 defocus_disk_sample(inout RNG rng)
    {
        // Return a random point in the camera defocus disk.
        var p = random_in_unit_disk(rng);
        return center + (p.x * defocus_disk_u) + (p.y * defocus_disk_v);
    }

    ray get_ray(uint i, uint j, inout RNG rng)
    {
        // Construct a camera ray originating from the defocus disk and directed at randomly sampled point around the pixel location i, j.
        var offset = sample_square(rng);
        var pixel_sample = pixel00_loc + ((i + offset.x) * pixel_delta_u) + ((j + offset.y) * pixel_delta_v);

        var ray_origin = (defocus_angle <= 0.f)? center : defocus_disk_sample(rng);
        var ray_direction = pixel_sample - ray_origin;
        var ray_time = random_float(rng);

        return ray(ray_origin, ray_direction, ray_time);
    }

    // Note that most shader / GPU programming does not support recursion!
    // Therefore, we have to alter the original ray_color function into using for loop.
    float3 ray_color(ray r, in hittable_list world, inout RNG rng)
    {
        float3 pixel_color = float3(1.f);
        for (int i = 0; i < max_depth; i++)
        {
            hit_record rec;

            if (world.hit(r, interval(0.001, infinity), rec))
            {
                ray scattered;
                float3 attenuation;
                material mat = world.get_material(rec.mat);
                if (mat.scatter(r, rec, attenuation, scattered, rng))
                {
                    pixel_color *= attenuation;
                    r = scattered;
                }
                else return pixel_color * mat.emitted(rec.u, rec.v, rec.p);
            }
            else
            {
                return pixel_color * background;
            }
        }
        return float3(0.f);
    }
}