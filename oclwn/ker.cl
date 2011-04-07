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

#ifdef __CLKERNEL
typedef float4 Point;
typedef int4 IntPoint;
#else
typedef struct Point {
  FLOAT_T x;
  FLOAT_T y;
  FLOAT_T z;
} Point;

typedef struct IntPoint {
  int x;
  int y;
  int z;
} IntPoint;
#endif

// FNV hash: http://isthe.com/chongo/tech/comp/fnv/#FNV-source
HASH_T hash(HASH_T i, HASH_T j, HASH_T k) {
  return (HASH_T)((((((OFFSET_BASIS ^ (HASH_T)i) * FNV_PRIME) ^ (HASH_T)j) * FNV_PRIME) ^ (HASH_T)k) * FNV_PRIME);
}

// Return the square of the distance between points p1 and p2
FLOAT_T our_distance(Point p1, Point p2) {
  Point pz = p1-p2;
  return dot(pz,pz);
  //return (p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y) + (p1.z-p2.z)*(p1.z-p2.z);
}

#ifdef __CLKERNEL
#else
void printArr(FLOAT_T *arr) {
  for(uint i = 0; i < N; ++i) {
	printf("%u = %f\n",i,arr[i]);
  }
}
#endif

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

uint rng(uint last) {
  return ((1103515245 * last + 12345) % 0x100000000);
}

//Generated with "N[Table[CDF[PoissonDistribution[4], i], {i, 1, 9}], 20]"
uint prob_lookup(float value)
{
 if(value < 0.091578194443670901469) return 1;
 else if(value < 0.23810330555354434382) return 2;
 else if(value < 0.43347012036670893362) return 3;
 else if(value < 0.62883693517987352342) return 4;
 else if(value < 0.78513038703040519526) return 5;
 else if(value < 0.88932602159742630982) return 6;
 else if(value < 0.94886638420715266099) return 7;
 else if(value < 0.97863656551201583658) return 8;
 else return 9; 
}

void findDistancesForCube(FLOAT_T *distanceArray, Point p, IntPoint c) {
  uint rngLast = rng( hash(c.x, c.y, c.z) );
  uint numFPoints = prob_lookup( (float)rngLast/0x100000000 );
#ifdef __CLKERNEL
#else
  printf("We'll have %d feature points in (%d,%d,%d).\n",numFPoints,c.x,c.y,c.z);
#endif
  Point featurePoint;
  for(uint i = 0; i < numFPoints; ++i) {
	rngLast = rng(rngLast);
	featurePoint.x = (float)rngLast / 0x100000000 + c.x;
	
	rngLast = rng(rngLast);
	featurePoint.y = (float)rngLast / 0x100000000 + c.y;

	rngLast = rng(rngLast);
	featurePoint.z = (float)rngLast / 0x100000000 + c.z;
	
	FLOAT_T dist = our_distance(p,featurePoint);

#ifdef __CLKERNEL	
#else
	printf("Found a feature point (%.2f,%.2f,%.2f) in chunk (%d,%d,%d).\n",featurePoint.x,featurePoint.y,featurePoint.z,c.x,c.y,c.z);

	printf("Square distance from (%.2f,%.2f,%.2f) to (%.2f,%.2f,%.2f): %.3f\n",featurePoint.x,featurePoint.y,featurePoint.z,p.x,p.y,p.z,dist);
#endif

	insert(distanceArray, dist);
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

#ifdef __CLKERNEL
__kernel void WorleyNoise(__global FLOAT_T *arrX, __global FLOAT_T *arrY, __global FLOAT_T *arrZ, __global FLOAT_T *output, int width, int height, int depth) {
  uint idX = get_global_id(0);
  uint idY = get_global_id(1);
  uint idZ = get_global_id(2);

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

	output[depth*height*idX + depth*idY + idZ] = darr[0]; 
  }
} 
#else
void somePoint(Point p) {
	// Initalize array
	FLOAT_T darr[N];
	for(int i=0; i<N; ++i)
	  darr[i] = 666;
	
	forAll(darr,p);

	printf("[%.2f,%.2f,%.2f]:\n",p.x,p.y,p.z);
	for(uint i=0; i<N; ++i)
	  printf("%u = %f\n",i,darr[i]);
}

int main() {
  Point p;
  p.x = 0.62;
  p.y = 1.5;
  p.z = 2.0;
  somePoint(p);
  /* for(int i=-5; i < 5; ++i) */
  /* 	for(int j=-5; j < 5; ++j) */
  /* 	  for(int k=-5; k < 5; ++k) */
  /* 		somePoint(i,j,k, (float)i/2,(float)j/2,(float)k/2); */
}
#endif
