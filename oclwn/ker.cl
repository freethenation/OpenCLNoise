#define N 5

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


#define BIGNUM 888

//~ FLOAT_T our_distance(Point p1, Point p2) {
    //~ Point d = fabs(p1-p2);
    //~ if(d.x > d.y && d.x > d.z)
	//~ return d.x;
    //~ if(d.y > d.z)
	//~ return d.y;
    //~ return d.z;
//~ }

// Return the square of the distance between points p1 and p2
FLOAT_T our_distance(Point p1, Point p2) {
  return (p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y) + (p1.z-p2.z)*(p1.z-p2.z);
}

void insert(FLOAT_T *arr, FLOAT_T value) {
  // Ugly hack to prevent duplicate values
  for(int i=0; i < N; ++i)
    if(arr[i] == value)
  	return;

  float temp;
  for(int i=N-1; i>=0; i--) {
    if(value > arr[i]) break;
    temp = arr[i];
    arr[i] = value;
    if(i+1<N) arr[i+1] = temp;
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

void findDistancesForCube(FLOAT_T *distanceArray, Point p, IntPoint cube) {

}

PointColor filter_worley(PointColor input) {
    FLOAT_T darr[N];
    for(int i=0; i<N; ++i)
	darr[i] = BIGNUM;
    
    IntPoint cube;
    uint rngLast,numFPoints;
    Point randomDiff,featurePoint;
    
    for(int i=-1; i < 2; ++i) {
	for(int j=-1; j < 2; ++j) {
	    for(int k=-1; k < 2; ++k) {
		cube.x = input.point.x + i;
		cube.y = input.point.y + j;
		cube.z = input.point.z + k;
		rngLast = rng( hash(cube.x, cube.y, cube.z) );
		
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

		    insert(darr, our_distance(input.point,featurePoint));
		}
	    }
	}
    }
    
    input.color.xyz = darr[1] - darr[0];
    input.color.w = 1;
    
    return input;
}

__kernel void WorleyNoise(__global float4 *input, __global float4 *output) {
    uint id = get_global_id(0);
    uint len = get_global_size(0);

    // Shall we do work?
    if(id < len) {
	PointColor inp;
	inp.point = input[id];
	output[id] = filter_worley(inp).color;
    }
} 
