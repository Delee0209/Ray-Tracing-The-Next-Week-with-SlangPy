import interval;
import ray;

struct hit_record
{
    float3 p;
    float3 normal;
    uint mat;
    float t;
    float u;
    float v;
    bool front_face;

    [mutating]
    void set_face_normal(in ray r, in float3 outward_normal)
    {
        // Sets the hit record normal vector
        // NOTE: the parameter `outward_normal` is assumed to have unit length.

        front_face = dot(r.direction(), outward_normal) < 0.f;
        normal = front_face ? outward_normal : -outward_normal;
    }
}

interface hittable
{
    bool hit(in ray r, interval ray_t, inout hit_record rec);
}