#define WORLEY_BIGNUM 888

// Defaults for arguments
#ifndef WORLEY_NUMVALUES
#define WORLEY_NUMVALUES 2 // Number of distances to calculate
#endif
#ifndef WORLEY_DISTANCE
#define WORLEY_DISTANCE 0 // Euclidian distance
#endif
#ifndef WORLEY_FUNCTION
#define WORLEY_FUNCTION F[1] - F[0] // Worley noise function - indicies start at 0
#endif

// Pick the correct distance formula
#if WORLEY_DISTANCE == 0 // Euclidian
#define our_distance(p1,p2) (p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y) + (p1.z-p2.z)*(p1.z-p2.z)
#elif WORLEY_DISTANCE == 1 // Manhattan
#define our_distance(p1,p2) fabs(p1.x-p2.x) + fabs(p1.y-p2.y) + fabs(p1.z-p2.z)
#elif WORLEY_DISTANCE == 2 // Chebyshev
#define our_distance(p1,p2) max(max(fabs(p1-p2).x,fabs(p1-p2).y),fabs(p1-p2).z)
#endif

void insert(FLOAT_T *arr, FLOAT_T value) {
  // Ugly hack to prevent duplicate values
  //~ for(int i=0; i < WORLEY_NUMVALUES; ++i)
    //~ if(arr[i] == value)
  	//~ return;

  float temp;
  for(int i=WORLEY_NUMVALUES-1; i>=0; i--) {
    if(value > arr[i]) break;
    temp = arr[i];
    arr[i] = value;
    if(i+1<WORLEY_NUMVALUES) arr[i+1] = temp;
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

PointColor filter_worley(PointColor input) {
    FLOAT_T F[WORLEY_NUMVALUES];
    for(int i=0; i<WORLEY_NUMVALUES; ++i)
	F[i] = WORLEY_BIGNUM;
    
    IntPoint cube;
    uint rngLast,numFPoints;
    Point randomDiff,featurePoint;
    
    for(int i=-1; i < 2; ++i) {
	for(int j=-1; j < 2; ++j) {
	    for(int k=-1; k < 2; ++k) {
		cube.x = input.point.x + i;
		cube.y = input.point.y + j;
		cube.z = input.point.z + k;
		rngLast = rng( hash(cube.x + (int)input.point.w, cube.y, cube.z) );
		
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
    
    input.color.xyz = WORLEY_FUNCTION;
    input.color.w = 1;
    
    return input;
}

