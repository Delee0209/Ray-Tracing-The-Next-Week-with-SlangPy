import hittable;
import aabb;
import ray;
import interval;

struct quad : hittable
{
    float3 Q;
    float3 u, v, w;
    float3 normal;
    float D;
    uint mat;
    __init(in float3 in_Q, in float3 in_u, in float3 in_v, uint m)
    {
        Q = in_Q;
        u = in_u;
        v = in_v;
        mat = m;

        var n = cross(u, v);
        normal = normalize(n);
        D = dot(normal, Q);
        w = n / dot(n, n);
    }

    bool is_interior(float a, float b, inout hit_record rec)
    {
        interval unit_interval = interval(0.f, 1.f);
        // Given the hit point in plane coordinates, return false if it is outside the 
        // primitive, otherwise set the hit record UV coordinates and return true.

        if (!unit_interval.contains(a) || !unit_interval.contains(b))
        {
            return false;
        }

        rec.u = a;
        rec.v = b;
        return true;
    }

    bool hit(in ray r, interval ray_t, inout hit_record rec)
    {
        var denom = dot(normal, r.direction());

        // No hit if the ray is parallel to the plane.
        if (fabs(denom) < 1e-8f)
        {
            return false;
        }

        // Return false if the hit point parameter t is outside the ray interval.
        var t = (D - dot(normal, r.origin())) / denom;
        if (!ray_t.contains(t))
        {
            return false;
        }

        // Determine if the hit point lies within the planar shape using its plane coordinates.
        var intersection = r.at(t);
        float3 planar_hitp_vector = intersection - Q;
        var alpha = dot(w, cross(planar_hitp_vector, v));
        var beta = dot(w, cross(u, planar_hitp_vector));

        if (!is_interior(alpha, beta, rec))
        {
            return false;
        }

        // Ray hits the 2D shape; set the rest of the hit record and return true.
        rec.t = t;
        rec.p = intersection;
        rec.mat = mat;
        rec.set_face_normal(r, normal);

        return true;
    }
}