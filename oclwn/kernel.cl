__kernel void FilterChain(__global float4 *input, __global float4 *output) {
    uint id = get_global_id(0);
    uint len = get_global_size(0);

    // Shall we do work?
    if(id < len) {
	PointColor v;
	v.point = input[id];
	
	<< FILTERS HERE >>
	
	output[id] = v.color;
    }
} 

__kernel void ZeroToOneKernel(__global float4 *output, const float seed) {
    uint idX = get_global_id(0);
    uint idY = get_global_id(1);
    uint idZ = get_global_id(2);
    uint width = get_global_size(0);
    uint height = get_global_size(1);
    uint depth = get_global_size(2);

    uint arrIdx = idX + idY * width + idZ * width * height;

    PointColor v;
    v.point.x = (float)idX/width;
    v.point.y = (float)idY/height;
    v.point.z = (float)idZ/depth;
    v.point.w = seed;
    
    << FILTERS HERE >>
    
    output[arrIdx] = v.color;
} 
