//#include <stdio.h>

#define FLOAT_T float
#define HASH_T int
#define N 5
//#define uint unsigned int

HASH_T hash(HASH_T i, HASH_T j, HASH_T k) {
  return (541 * i + 79 * j + 31 * k) % 0x100000000;
}

FLOAT_T distanceSq(FLOAT_T x, FLOAT_T y, FLOAT_T z, FLOAT_T px, FLOAT_T py, FLOAT_T pz) {
  return (x-px)*(x-px) + (y-py)*(y-py) + (z-pz)*(z-pz);
}

void insert(FLOAT_T *arr, FLOAT_T value) {
  float temp;
  for (int i=N-1; i>=0; i--){
	if(value > arr[i]) return;
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

void findDistancesForCube(FLOAT_T *distanceArray, FLOAT_T x, FLOAT_T y, FLOAT_T z, int cx, int cy, int cz) {
  uint rngLast = rng( hash(cx, cy, cz) );
  uint numFPoints = prob_lookup( (float)rngLast/0x100000000 );

  FLOAT_T fPointX,fPointY,fPointZ;
  for(uint i = 0; i < numFPoints; ++i) {
	rngLast = rng(rngLast);
	fPointX = (float)rngLast / 0x100000000 + cx;
	
	rngLast = rng(rngLast);
	fPointY = (float)rngLast / 0x100000000 + cy;

	rngLast = rng(rngLast);
	fPointZ = (float)rngLast / 0x100000000 + cz;
	
	//printf("Comparing (%.2f,%.2f,%.2f) to (%.2f,%.2f,%.2f)\n",x,y,z,fPointX,fPointY,fPointZ);

	insert(distanceArray, distanceSq(x,y,z,fPointX,fPointY,fPointZ));
  }
}

void forAll(FLOAT_T *distanceArray, FLOAT_T x, FLOAT_T y, FLOAT_T z) {
  for(int i=-1; i < 2; ++i)
	for(int j=-1; j < 2; ++j)
	  for(int k=-1; k < 2; ++k)
		findDistancesForCube(distanceArray, x,y,z, x+i,y+j,z+k);
}

/* void printArr(FLOAT_T *arr) { */
/*   for(int i = 0; i < N; ++i) */
/* 	printf("i = %d: v = %f\n",i,arr[i]); */
/*   printf("\n"); */
/* } */

/* int main() { */
/*   FLOAT_T distanceArr[N]; */
/*   for(int i=0; i < N; ++i) */
/* 	distanceArr[i] = 666; */
/*   FLOAT_T x = 5.2, y = 3.3, z = 9.1; */
/*   forAll(distanceArr,x,y,z); */
/*   printArr(distanceArr); */
/*   return 0; */
/* } */

__kernel void WorleyNoise(__global FLOAT_T *arrX, __global FLOAT_T *arrY, __global FLOAT_T *arrZ, __global FLOAT_T *output, int width) {
  uint idX = get_global_id(0);
  uint idY = get_global_id(1);
  uint idZ = get_global_id(2);

  // Shall we do work?
  if(idX < width && idY < width && idZ < width) {
	// Initalize array
	FLOAT_T darr[N];
	for(int i=0; i<N; ++i)
	  darr[i] = 666;
	
	forAll(darr,arrX[idX],arrY[idY],arrZ[idZ]);

	output[width*width*idX + width*idY + idZ] = darr[1] - darr[0]; 
  }
} 
