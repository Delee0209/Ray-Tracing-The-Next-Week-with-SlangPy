import hittable_list;
import camera;
import ray;
import interval;
import utility;

// binding
camera cam;
hittable_list world;
RWTexture2D<float4> image;

// Main kernel for rendering
[shader("compute")]
[numthreads(16, 16, 1)]
void render(
    uint3 thread_id: SV_DispatchThreadID)
{
    uint i = thread_id.x, j = thread_id.y;
    // Shader housekeeping... make sure we are not exceeding the dispatch dimension.
    if (any(uint2(i, j) >= uint2(cam.image_width, cam.image_height)))
    {
        return;
    }
    // Initialize random number generator.
    RNG rng = RNG(uint2(i, j), cam.frame_number);

    ray r = cam.get_ray(i, j, rng);

    float3 pixel_color = cam.ray_color(r, world, rng);
    pixel_color = linear_to_gamma(pixel_color);

    interval intensity = interval(0.f, 1.f);
    pixel_color = intensity.clamp(pixel_color);

    // Streaming average - equals to sum / frame_number.
    image[uint2(i, j)] = float4(image[uint2(i, j)].xyz + (pixel_color - image[uint2(i, j)].xyz) / (cam.frame_number + 1), 1.0);
}