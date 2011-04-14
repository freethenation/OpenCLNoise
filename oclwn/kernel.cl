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

PointColor n1scaletrans(PointColor input, float4 scale, float4 translate) {  
    input.point = input.point * scale + translate;
    return input;
}

#define n2WORLEY_NUMVALUES 1
#define n2WORLEY_FUNCTION F[0]
#define n2WORLEY_DISTANCE 0
#define n2BIGNUM 888

// Defaults for arguments
#ifndef n2NUMVALUES
#define n2NUMVALUES 2 // Number of distances to calculate
#endif
#ifndef n2DISTANCE
#define n2DISTANCE 0 // Euclidian distance
#endif
#ifndef n2FUNCTION
#define n2FUNCTION F[1] - F[0] // Worley noise function - indicies start at 0
#endif

// Pick the correct distance formula
#if n2DISTANCE == 0 // Euclidian
#define our_distance(p1,p2) (p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y) + (p1.z-p2.z)*(p1.z-p2.z)
#elif n2DISTANCE == 1 // Manhattan
#define our_distance(p1,p2) fabs(p1.x-p2.x) + fabs(p1.y-p2.y) + fabs(p1.z-p2.z)
#elif n2DISTANCE == 2 // Chebyshev
#define our_distance(p1,p2) max(max(fabs(p1-p2).x,fabs(p1-p2).y),fabs(p1-p2).z)
#endif

void insert(FLOAT_T *arr, FLOAT_T value) {
  float temp;
  for(int i=n2NUMVALUES-1; i>=0; i--) {
    if(value > arr[i]) break;
    temp = arr[i];
    arr[i] = value;
    if(i+1<n2NUMVALUES) arr[i+1] = temp;
  }
}

// Generated with "AccountingForm[N[Table[CDF[PoissonDistribution[4], i], {i, 1, 9}], 20]*2^32]" //"N[Table[CDF[PoissonDistribution[4], i], {i, 1, 9}], 20]"
uint prob_lookup(uint value)
{
    if(value < 393325350) return 1;
    if(value < 1022645910) return 2;
    if(value < 1861739990) return 3;
    if(value < 2700834071) return 4;
    if(value < 3372109335) return 5;
    if(value < 3819626178) return 6;
    if(value < 4075350088) return 7;
    if(value < 4203212043) return 8;
    return 9;
}

PointColor n2worley(PointColor input, int seed) {
    FLOAT_T F[n2NUMVALUES];
    for(int i=0; i<n2NUMVALUES; ++i)
        F[i] = n2BIGNUM;
    
    IntPoint cube;
    uint rngLast,numFPoints;
    Point randomDiff,featurePoint;
    
    for(int i=-1; i < 2; ++i) {
        for(int j=-1; j < 2; ++j) {
            for(int k=-1; k < 2; ++k) {
                cube = convert_int4_rtn(input.point) + (int4)(i,j,k,0);
                rngLast = rng( hash(cube.x + seed, cube.y, cube.z) );
                
                // Find the number of feature points in the cube
                numFPoints = prob_lookup( rngLast );
                  
                for(uint i = 0; i < numFPoints; ++i) {
                    rngLast = rng(rngLast);
                    randomDiff.x = (float)rngLast / 0x100000000;
                    
                    rngLast = rng(rngLast);
                    randomDiff.y = (float)rngLast / 0x100000000;
                    
                    rngLast = rng(rngLast);
                    randomDiff.z = (float)rngLast / 0x100000000;
                    
                    featurePoint = randomDiff + convert_float4(cube);

                    insert(F, our_distance(input.point,featurePoint));
                }
            }
        }
    }
    
    input.color.xyz = n2FUNCTION;
    input.color.w = 1;
    
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
    o0 = n1scaletrans(o0, args_float4[0], args_float4[1]);
    o0 = n2worley(o0, args_int[0]);

    output[arrIdx] = o0.color;
}