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

// "Good" random number generator
//#define good_rng(x) ((x * (x * x * 15731 + 789221) + 1376312589) % 0x100000000)
#define good_rng(x) (x)

// interpolation
#define lerp(a,b,x) (a*(1-x)+b*x)
#define coserp(a, b, x) a*(1-(1-cos(x*3.1415927))*.5) + b*(1-cos(x*3.1415927))*.5
#define INTERPOLATOR coserp


