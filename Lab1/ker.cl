//~ __kernel void reducesum(__global const float *input, __global float *output, __global float *shared, const uint len)
//~ {
    //~ uint gpidA = 0; //get_global_id(0);
    //~ uint featA = get_local_id(0);
    //~ uint numGroups = get_num_groups(0);
	//~ int stride = numGroups * 2 * BLOCK_SIZE;
	//~ uint i = gpidA * 2 * BLOCK_SIZE + featA;
	//~ int cgs;
	//~ 
	//~ shared[featA] = 0;
	//~ 
	//~ while(i < len) {
		//~ shared[featA] += input[i];
		//~ shared[featA] += input[i + BLOCK_SIZE];
		//~ i += stride;
		//~ barrier(CLK_LOCAL_MEM_FENCE);
	//~ }
	//~ 
	//~ for(cgs=512; cgs > 1; cgs /= 2) {
        //~ if(BLOCK_SIZE >= cgs) {
            //~ if(featA < cgs/2)
                //~ shared[featA] += shared[featA + cgs/2];
            //~ barrier(CLK_LOCAL_MEM_FENCE);
        //~ }
	//~ }
//~ 
	//~ if(featA == 0)
		//~ output[gpidA] = shared[0];
//~ }

//~ __kernel void vad (__global const float* src_a, __global const float* src_b, __global float* res, const int num) {
   //~ /* get_global_id(0) returns the ID of the thread in execution.
   //~ As many threads are launched at the same time, executing the same kernel,
   //~ each one will receive a different ID, and consequently perform a different computation.*/
   //~ const int idx = get_global_id(0);
//~ 
   //~ /* Now each work-item asks itself: "is my ID inside the vector's range?"
   //~ If the answer is YES, the work-item performs the corresponding computation*/
   //~ if (idx < num)
      //~ res[idx] = src_a[idx] + src_b[idx];
//~ }

__kernel void matmult(__global const float *A, __global const float *B, __global float *output, const uint width) {
    uint threadIDx = get_global_id(0);
    uint threadIDy = get_global_id(1);
    
    if(threadIDx >= width || threadIDy >= width)
	return;
    
    for(uint i = 0; i < width; ++i)
	output[threadIDx * width + threadIDy] += A[threadIDx * width + i] * B[i * width + threadIDy];
}
