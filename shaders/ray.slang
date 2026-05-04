struct ray
{
    float3 orig, dir;
    float tm;
    __init(in float3 origin, in float3 direction, in float time)
    {
        orig = origin;
        dir = direction;
        tm = time;
    }

    __init(in float3 origin, in float3 direction)
    {
        orig = origin;
        dir = direction;
        tm = 0.f;
    }

    float3 origin()
    {
        return orig;
    }
    float3 direction()
    {
        return dir;
    }

    float time()
    {
        return tm;
    }

    float3 at(float t)
    {
        return orig + t * dir;
    }
}