struct perlin
{
    StructuredBuffer<float3> randvec;
    int perm_x[256];
    int perm_y[256];
    int perm_z[256];

    float noise(in float3 p)
    {
        var u = p.x - floor(p.x);
        var v = p.y - floor(p.y);
        var w = p.z - floor(p.z);

        var i = int(floor(p.x));
        var j = int(floor(p.y));
        var k = int(floor(p.z));
        float3 c[2][2][2];

        for (int di = 0; di < 2; di ++)
        {
            for (int dj = 0; dj < 2; dj ++)
            {
                for (int dk = 0; dk < 2; dk++)
                {
                    c[di][dj][dk] = randvec[perm_x[(i + di) & 255] ^ perm_y[(j + dj) & 255] ^ perm_z[(k + dk) & 255]];
                }
            }
        }

        return perlin_interp(c, u, v, w);
    }

    float turb(in float3 p, int depth)
    {
        var accum = 0.f;
        var temp_p = p;
        var weight = 1.f;

        for (int i = 0; i < depth; i++)
        {
            accum += weight * noise(temp_p);
            weight *= 0.5f;
            temp_p *= 2.f;
        }

        return fabs(accum);
    }

    float perlin_interp(in float3 c[2][2][2], float u, float v, float w)
    {
        var uu = u * u * (3 - 2 * u);
        var vv = v * v * (3 - 2 * v);
        var ww = w * w * (3 - 2 * w);
        var accum = 0.f;

        for (int i = 0; i < 2; i++)
        {
            for (int j = 0; j < 2; j++)
            {
                for (int k = 0; k < 2; k++)
                {
                    float3 weight_v = float3(u - i, v - j, w - k);
                    accum += (i * uu + (1 - i) * (1 - uu)) * (j * vv + (1 - j) * (1 - vv)) * (k * ww + (1 - k) * (1 - ww)) * dot(c[i][j][k], weight_v);
                }
            }
        }

        return accum;
    }
}