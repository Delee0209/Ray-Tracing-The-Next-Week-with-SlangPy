// this shader contain the content of rtweekend.h and some of the helper function in vec3.h from the first book

static float infinity = 999999.f;
static float pi = 3.141592653589f;

// shader does not have native random number functions
// therefore, we have to implement one
// this implementation is directly taken from the SlangPy Path Tracer example
struct RNG
{
    uint state;

    __init(uint seed)
    {
        state = seed;
    }

    __init(uint2 pixel, uint sample_index)
    {
        state = (pixel.x * 100591) ^ (pixel.y * 102191) ^ (sample_index * 103643);
    }

    [mutating]
    uint next()
    {
        const uint A = 1664525u;
        const uint C = 1013904223u;
        state = (A * state + C);
        return state;
    }

    [mutating]
    float sample_1d()
    {
        return (next() >> 8) * 0x1p-24;
    }
}

// since we don't have a vec3.slang -> moving some of the helper function here
float length_squared(float3 e)
{
    return e.x * e.x + e.y * e.y + e.z * e.z;
}

float random_float(inout RNG rng)
{
    return rng.sample_1d();
}

float random_float(float min, float max, inout RNG rng)
{
    return min + (max - min) * random_float(rng);
}

float3 random_float3(inout RNG rng)
{
    return float3(random_float(rng), random_float(rng), random_float(rng));
}

float3 random_float3(float min, float max, inout RNG rng)
{
    return float3(random_float(min, max, rng), random_float(min, max, rng), random_float(min, max, rng));
}

float3 random_unit_vector(inout RNG rng)
{
    while (true)
    {
        var p = random_float3(-1.f, 1.f, rng);
        var lensq = length_squared(p);
        if (0.f < lensq && lensq <= 1.f)
        {
            return p / sqrt(lensq);
        }
    }
}

float3 random_on_hemisphere(in float3 normal, inout RNG rng)
{
    float3 on_unit_sphere = random_unit_vector(rng);
    if (dot(on_unit_sphere, normal) > 0.f)
    {
        return on_unit_sphere;
    }
    else
    {
        return -on_unit_sphere;
    }
}

float linear_to_gamma(float linear_component)
{
    if (linear_component > 0.f)
    {
        return sqrt(linear_component);
    }
    return 0.f;
}

float3 linear_to_gamma(float3 linear_component)
{
    return float3(linear_to_gamma(linear_component.x), linear_to_gamma(linear_component.y), linear_to_gamma(linear_component.z));
}

bool near_zero(float3 in)
{
    // Return true if the vector is close to zero in all dimension
    var s = 1e-8;
    return all(fabs(in) < s);
}

float3 random_in_unit_disk(inout RNG rng)
{
    while (true)
    {
        var p = float3(random_float(-1.f, 1.f, rng), random_float(-1.f, 1.f, rng), 0.f);
        if (length_squared(p) < 1.f)
        {
            return p;
        }
    }
}