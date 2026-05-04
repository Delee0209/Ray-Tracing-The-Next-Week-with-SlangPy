import interval;
import hittable;
import material;
import texture;
import aabb;
import bvh_node;
import sphere;
import quad;
import ray;

struct object // struct for packing hittable data from CPU
{                       // bvh_node     // sphere
    uint type;          // 0            // 1
    float3 vector1;     // aabb min     // center1
    float3 vector2;     // aabb max     // center2
    float3 vector3;     // padding      // padding
    float parameter;    // padding      // radius
    int id1;            // left         // mat
    int id2;            // right        // padding
}       

struct appearance // struct for packing material data from CPU
{                       // lambertian   // metal        // dielectric
    uint type;          // 0            // 1            // 2
    int tex;            // tex          // tex          // padding
    float parameter;    // padding      // fuzz         // ior
}

struct color
{
    uint type;
    float3 albedo;
    int t1;
    int t2;
}

struct hittable_list
{
    bool use_bvh;
    uint bvh_root;
    uint object_count;
    StructuredBuffer<object> objects;
    StructuredBuffer<appearance> appearances;
    StructuredBuffer<color> colors;

    hittable get_hittable(int id)
    {
        switch (objects[id].type)
        {
            case 0:
                return bvh_node(aabb(objects[id].vector1, objects[id].vector2), objects[id].id1, objects[id].id2);
            case 1:
                return sphere(objects[id].vector1, objects[id].vector2, objects[id].parameter, objects[id].id1);
            case 2:
                return quad(objects[id].vector1, objects[id].vector2, objects[id].vector3, objects[id].id1);
            default:
                return sphere(objects[id].vector1, objects[id].vector2, objects[id].parameter, objects[id].id1);
        }
    }

    bvh_node get_node(int id)
    {
        return bvh_node(aabb(objects[id].vector1, objects[id].vector2), objects[id].id1, objects[id].id2);
    }

    material get_material(int id)
    {
        switch (appearances[id].type)
        {
            case 0:
                return lambertian(get_texture(appearances[id].tex));
            case 1:
                return metal(get_texture(appearances[id].tex), appearances[id].parameter);
            case 2:
                return dielectric(appearances[id].parameter);
            case 3:
                return diffuse_light(appearances[id].tex);
            default:
                return lambertian(get_texture(appearances[id].tex));
        }
    }

    // Due to the limitation recursive functions in shader, checker_texture is currently hardcoded to only take solid_color as input.
    // This may be extended in the future...
    solid_color get_nested_texture(int id)
    {
        return solid_color(colors[id].albedo);
    }
    texture get_texture(int id)
    {
        switch (colors[id].type)
        {
            case 0:
                return solid_color(colors[id].albedo);
            case 1:
                return checker_texture(colors[id].albedo.x, get_nested_texture(colors[id].t1), get_nested_texture(colors[id].t2));
            case 2:
                return image_texture(colors[id].t1);
            case 3:
                return noise_texture(colors[id].albedo.x);
            default:
                return solid_color(colors[id].albedo);
        }
    }

    // brute-force scene traversal
    bool native_hit(in ray r, interval ray_t, inout hit_record rec)
    {
        hit_record temp_rec;
        bool hit_anything = false;
        var closest_so_far = ray_t.max;

        for (int id = 0; id < object_count; id++)
        {
            hittable object = get_hittable(id);
            if (object.hit(r, interval(ray_t.min, closest_so_far), temp_rec))
            {
                hit_anything = true;
                closest_so_far = temp_rec.t;
                rec = temp_rec;
            }
        }

        return hit_anything;
    }

    // bvh scene traversal
    bool bvh_hit(in ray r, interval ray_t, inout hit_record rec)
    {
        hit_record temp_rec;
        bool hit_anything = false;
        var closest_so_far = ray_t.max;

        // stack tree traversal
        int stack[32];
        int stack_ptr = 0;

        stack[stack_ptr++] = bvh_root;

        while (stack_ptr > 0)
        {
            int id = stack[--stack_ptr];
            if (id < object_count) // leaf node
            {
                hittable object = get_hittable(id);
                if (object.hit(r, interval(ray_t.min, closest_so_far), temp_rec))
                {
                    hit_anything = true;
                    closest_so_far = temp_rec.t;
                    rec = temp_rec;
                }
            }
            else // bvh_node
            {
                bvh_node node = get_node(id);
                if (node.hit(r, interval(ray_t.min, closest_so_far), temp_rec))
                {
                    stack[stack_ptr++] = node.left;
                    stack[stack_ptr++] = node.right;
                }
            }
        }
        return hit_anything;
    }

    bool hit(in ray r, interval ray_t, inout hit_record rec)
    {
        if (use_bvh) return bvh_hit(r, ray_t, rec);
        else return native_hit(r, ray_t, rec);
    }
}