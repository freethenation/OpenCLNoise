// Start utility.cl
#define FLOAT_T float
typedef float4 Point;
typedef int4 IntPoint;

typedef struct PointColor {
    Point point;
    Point color;
} PointColor;

#define OFFSET_BASIS 2166136261
#define FNV_PRIME 16777619

// FNV hash: http://isthe.com/chongo/tech/comp/fnv/#FNV-source
uint hash(uint i, uint j, uint k) {
  return (uint)((((((OFFSET_BASIS ^ (uint)i) * FNV_PRIME) ^ (uint)j) * FNV_PRIME) ^ (uint)k) * FNV_PRIME);
}

// LCG Random Number Generator
#define rng(last) ((1103515245 * last + 12345) % 0x100000000)
// End utility.cl

PointColor n0clear() {
    uint idX = get_global_id(0);
    uint idY = get_global_id(1);
    uint idZ = get_global_id(2);
    uint width = get_global_size(0);
    uint height = get_global_size(1);
    uint depth = get_global_size(2);
	
    //uint arrIdx = idX + idY * width + idZ * width * height;

    PointColor v;
    v.point.x = (float)idX/width;
    v.point.y = (float)idY/height;
    v.point.z = (float)idZ/depth;
	v.color.xyzw = 1;
	return v;
}

PointColor n1checkerboard(PointColor input, float4 blackColor, float4 whiteColor) {
    int4 point = convert_int4(input.point);
    if((point.x + point.y + point.z) % 2 == 0)
        input.color = blackColor;
    else
        input.color = whiteColor;
    return input;
}

__kernel void ZeroToOneKernel(__global float4 *output, __global float *args_float, __global int *args_int, __global float4 *args_float4, __global int4 *args_int4) {
    uint idX = get_global_id(0);
    uint idY = get_global_id(1);
    uint idZ = get_global_id(2);
    uint width = get_global_size(0);
    uint height = get_global_size(1);
    uint depth = get_global_size(2);

    uint arrIdx = idX + idY * width + idZ * width * height;

    PointColor o0;
    o0 = n0clear();
    o0 = n1checkerboard(o0, args_float4[0], args_float4[1]);

    output[arrIdx] = o0.color;
}