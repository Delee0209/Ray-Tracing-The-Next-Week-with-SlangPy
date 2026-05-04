import interval;
import perlin;

interface texture
{
    float3 value(float u, float v, in float3 p);
}

struct solid_color : texture
{
    float3 albedo;
    __init(float3 color)
    {
        albedo = color;
    }
    __init(float red, float green, float blue)
    {
        albedo = float3(red, green, blue);
    }

    float3 value(float u, float v, in float3 p)
    {
        return albedo;
    }
}

// Due to the limitation recursive functions in shader, checker_texture is currently hardcoded to only take solid_color as input.
// This may be extended in the future...
struct checker_texture : texture
{
    float inv_scale;
    solid_color even;
    solid_color odd;
    __init(float scale, solid_color t1, solid_color t2)
    {
        inv_scale = 1.f / scale;
        even = t1;
        odd = t2;
    }
    __init(float scale, float3 c1, float3 c2)
    {
        inv_scale = 1.f / scale;
        even = solid_color(c1);
        odd = solid_color(c2);
    }

    float3 value(float u, float v, in float3 p)
    {
        var xInteger = int(floor(inv_scale * p.x));
        var yInteger = int(floor(inv_scale * p.y));
        var zInteger = int(floor(inv_scale * p.z));

        bool isEven = (xInteger + yInteger + zInteger) % 2 == 0;

        return isEven? even.value(u, v, p): odd.value(u, v, p);
    }
}

StructuredBuffer<DescriptorHandle<Texture2D>> images;
SamplerState sampler;

struct image_texture : texture
{
    uint img;
    
    float3 value(float u, float v, in float3 p)
    {
        // Clamp input texture coordinates to [0, 1] x [0, 1]
        u = interval(0.f, 1.f).clamp(u);
        v = 1.f - interval(0.f, 1.f).clamp(v); // Filp V to image coordinates

        // Shader handles texture interpolation internally.
        return images[img].Sample(sampler, float2(u, v), uint2(0, 0)).xyz;
    }
}

perlin noise;

struct noise_texture : texture
{
    float scale;

    float3 value(float u, float v, in float3 p)
    {
        return float3(0.5f, 0.5f, 0.5f) * (1.f + sin(scale * p.z + 10.f * noise.turb(p, 7)));
    }
}