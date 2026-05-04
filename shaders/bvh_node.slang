import interval;
import utility;
import ray;
import hittable;
import material;
import aabb;

struct bvh_node : hittable
{
    aabb bbox;
    int left, right;

    bool hit(in ray r, interval ray_t, inout hit_record rec)
    {
        return bbox.hit(r, ray_t);
    }
}