import ray;
import hittable;
import texture;
import utility;

interface material
{
    float3 emitted(float u, float v, in float3 p)
    {
        return float3(0.f, 0.f, 0.f);
    }
    
    bool scatter(in ray r_in, in hit_record rec, inout float3 attenuation, inout ray scattered, inout RNG rng);
}

struct lambertian : material    // material type == 0
{
    texture tex;
    __init(float3 color)
    {
        tex = solid_color(color);
    }
    __init(texture t)
    {
        tex = t;
    }

    bool scatter(in ray r_in, in hit_record rec, inout float3 attenuation, inout ray scattered, inout RNG rng)
    {
        var scattered_direction = rec.normal + random_unit_vector(rng);

        // Catch degenerate scatter direction
        if (near_zero(scattered_direction))
        {
            scattered_direction = rec.normal;
        }

        scattered = ray(rec.p, scattered_direction, r_in.time());
        attenuation = tex.value(rec.u, rec.v, rec.p);
        return true;
    }
}

struct metal : material         // material type == 1
{
    texture tex;
    float fuzz;
    __init(float3 color, float f)
    {
        tex = solid_color(color);
        fuzz = f;
    }
    __init(texture t, float f)
    {
        tex = t;
        fuzz = f;
    }
    
    bool scatter(in ray r_in, in hit_record rec, inout float3 attenuation, inout ray scattered, inout RNG rng)
    {
        float3 reflected = reflect(r_in.direction(), rec.normal);
        reflected = normalize(reflected) + (fuzz * random_unit_vector(rng));
        scattered = ray(rec.p, reflected, r_in.time());
        attenuation = tex.value(rec.u, rec.v, rec.p);
        return (dot(scattered.direction(), rec.normal) > 0.f);
    }
}

struct dielectric : material    // material type == 2
{
    // Refractive index in vacuum or air, or the ratio of the material's refractive index over the refractive index of the enclose media
    float refraction_index;

    float reflectance(float cosine, float refraction_index)
    {
        // Use Schlick's approximation for reflectance
        var r0 = (1.f - refraction_index) / (1.f + refraction_index);
        r0 = r0 * r0;
        return r0 + (1.f - r0) * pow((1.f - cosine), 5);
    }

    bool scatter(in ray r_in, in hit_record rec, inout float3 attenuation, inout ray scattered, inout RNG rng)
    {
        attenuation = float3(1.f);
        float ri = rec.front_face ? (1.f / refraction_index) : refraction_index;

        float3 unit_direction = normalize(r_in.direction());
        float cos_theta = fmin(dot(-unit_direction, rec.normal), 1.f);
        float sin_theta = sqrt(1.f - cos_theta * cos_theta);

        bool cannot_refract = ri * sin_theta > 1.f;
        float3 direction;

        if (cannot_refract || reflectance(cos_theta, ri) > random_float(rng))
        {
            direction = reflect(unit_direction, rec.normal);
        }
        else
        {
            direction = refract(unit_direction, rec.normal, ri);
        }

        scattered = ray(rec.p, direction, r_in.time());
        return true;
    }
}

struct diffuse_light : material
{
    texture tex;
    __init(float3 color)
    {
        tex = solid_color(color);
    }
    __init(texture t)
    {
        tex = t;
    }

    override float3 emitted(float u, float v, in float3 p)
    {
        return tex.value(u, v, p);
    }

    bool scatter(in ray r_in, in hit_record rec, inout float3 attenuation, inout ray scattered, inout RNG rng)
    {
        return false;
    }
}