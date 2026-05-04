import utility;

struct interval
{
    float min = infinity, max = -infinity;

    float size()
    {
        return max - min;
    }

    bool contains(float x)
    {
        return min <= x && x <= max;
    }

    bool surrounds(float x)
    {
        return min < x && x < max;
    }

    float clamp(float x)
    {
        if (x < min)
        {
            return min;
        }
        if (x > max)
        {
            return max;
        }
        return x;
    }

    float3 clamp(float3 x)
    {
        return float3(clamp(x.x), clamp(x.y), clamp(x.z));
    }
}

static interval empty = interval(infinity, -infinity);
static interval universe = interval(-infinity, infinity);