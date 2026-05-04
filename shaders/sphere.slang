import interval;
import utility;
import ray;
import hittable;
import material;

struct sphere : hittable
{
    ray center;
    float radius;
    uint mat;
    // Stationary Sphere
    __init(in float3 static_center, float r, uint m)
    {
        center = ray(static_center, float3(0.f, 0.f, 0.f));
        radius = fmax(0.f, r);
        mat = m;
    }

    // Moving Sphere
    __init(in float3 center1, in float3 center2, float r, uint m)
    {
        center = ray(center1, center2 - center1);
        radius = fmax(0.f, r);
        mat = m;
    }

    void get_sphere_uv(in float3 p, inout float u, inout float v)
    {
        // p: a given point on the sphere of radius one, centered at the origin.
        // u: returned value [0, 1] of angle around the Y axis from X = -1
        // v: returned value [0, 1] of angle from Y = -1 to Y = +1.
        //      <1 0 0> yields <0.50 0.50>      <-1  0  0> yields <0.00 0.50>
        //      <0 1 0> yields <0.50 1.00>      < 0 -1  0> yields <0.50 0.00>
        //      <0 0 1> yields <0.25 0.50>      < 0  0 -1> yields <0.75 0.50>

        var theta = acos(-p.y);
        var phi = atan2(-p.z, p.x) + pi;

        u = phi / (2.f * pi);
        v = theta / pi;
    }

    bool hit(in ray r, interval ray_t, inout hit_record rec)
    {
        float3 currnet_center = center.at(r.time());
        float3 oc = currnet_center - r.origin();
        var a = length_squared(r.direction());
        var h = dot(r.direction(), oc);
        var c = length_squared(oc) - radius * radius;

        var discriminant = h * h - a * c;
        if (discriminant < 0.f)
        {
            return false;
        }

        var sqrtd = sqrt(discriminant);

        // Find the nearest root that lies in the acceptance range.
        var root = (h - sqrtd) / a;
        if (!ray_t.surrounds(root))
        {
            root = (h + sqrtd) / a;
            if (!ray_t.surrounds(root))
            {
                return false;
            }
        }

        rec.t = root;
        rec.p = r.at(rec.t);
        float3 outward_normal = (rec.p - currnet_center) / radius;
        rec.set_face_normal(r, outward_normal);
        get_sphere_uv(outward_normal, rec.u, rec.v);
        rec.mat = mat;

        return true;
    }
}