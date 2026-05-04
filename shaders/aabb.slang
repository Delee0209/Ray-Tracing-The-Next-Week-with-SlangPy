import interval;
import utility;
import ray;

struct aabb
{
    interval x, y, z;
    __init(float3 a, float3 b)
    {
        x = interval(a.x, b.x);
        y = interval(a.y, b.y);
        z = interval(a.z, b.z);
    }

    interval axis_interval(int n)
    {
        if (n == 1) return y;
        if (n == 2) return z;
        return x;
    }

    bool hit(in ray r, interval ray_t)
    {
        float3 ray_orig = r.origin();
        float3 ray_dir = r.direction();

        for (int axis = 0; axis < 3; axis++)
        {
            interval ax = axis_interval(axis);
            float adinv = 1.f / ray_dir[axis];

            var t0 = (ax.min - ray_orig[axis]) * adinv;
            var t1 = (ax.max - ray_orig[axis]) * adinv;

            if (t0 < t1)
            {
                if (t0 > ray_t.min) ray_t.min = t0;
                if (t1 < ray_t.max) ray_t.max = t1;
            }
            else
            {
                if (t1 > ray_t.min) ray_t.min = t1;
                if (t0 < ray_t.max) ray_t.max = t0;
            }

            if (ray_t.max <= ray_t.min) return false;
        }
        return true;
    }
}