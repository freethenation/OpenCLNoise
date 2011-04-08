#define __CLKERNEL

#ifdef __CLKERNEL
#else
#include <stdio.h>
#define uint unsigned int
#endif

#define OFFSET_BASIS 2166136261
#define FNV_PRIME 16777619
#define FLOAT_T float
#define HASH_T uint
#define N 5

typedef float4 Point;
typedef int4 IntPoint;

// FNV hash: http://isthe.com/chongo/tech/comp/fnv/#FNV-source
HASH_T hash(HASH_T i, HASH_T j, HASH_T k) {
  return (HASH_T)((((((OFFSET_BASIS ^ (HASH_T)i) * FNV_PRIME) ^ (HASH_T)j) * FNV_PRIME) ^ (HASH_T)k) * FNV_PRIME);
}

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

// LCG Random Number Generator
uint rng(uint last) {
  return ((1103515245 * last + 12345) % 0x100000000);
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

void findDistancesForCube(FLOAT_T *distanceArray, Point p, IntPoint c) {
  uint rngLast = rng( hash(c.x, c.y, c.z) );
  uint rng1,rng2,rng3;
  Point randomDiff,featurePoint;
  uint numFPoints = prob_lookup( rngLast );

  for(uint i = 0; i < numFPoints; ++i) {
	rng1 = rng(rngLast);
	rng2 = rng(rng1);
	rng3 = rng(rng2);
	rngLast = rng3;

	randomDiff.x = (float)rng1 / 0x100000000;
	randomDiff.y = (float)rng2 / 0x100000000;
	randomDiff.z = (float)rng3 / 0x100000000;
	featurePoint = randomDiff + convert_float4(c);

	insert(distanceArray, our_distance(p,featurePoint));
  }
}

void forAll(FLOAT_T *distanceArray, Point p) {
    for(int i=-1; i < 2; ++i) {
	for(int j=-1; j < 2; ++j) {
	    for(int k=-1; k < 2; ++k) {
		IntPoint cube;
		cube.x = p.x + i;
		cube.y = p.y + j;
		cube.z = p.z + k;
		findDistancesForCube(distanceArray, p, cube);
	    }
	}
    }
}

__kernel void WorleyNoise(__global FLOAT_T *arrX, __global FLOAT_T *arrY, __global FLOAT_T *arrZ, __global FLOAT_T *output) {//, int width, int height, int depth) {
    uint idX = get_global_id(0);
    uint idY = get_global_id(1);
    uint idZ = get_global_id(2);
    uint width = get_global_size(0);
    uint height = get_global_size(1);
    uint depth = get_global_size(2);

  // Shall we do work?
  if(idX < width && idY < height && idZ < depth) {
	// Initalize array
	FLOAT_T darr[N];
	for(int i=0; i<N; ++i)
	  darr[i] = 888;
	
	Point p;
	p.x = arrX[idX];
	p.y = arrY[idY];
	p.z = arrZ[idZ];
	forAll(darr,p);
	//findDistancesForCube(darr, p, convert_int4(p));

	output[depth*height*idX + depth*idY + idZ] = darr[1] - darr[0]; 
  }
} 
