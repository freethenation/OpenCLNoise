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

// interpolation
#define lerp(a,b,x) (a-a*x+b*x)
