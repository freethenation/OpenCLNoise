__kernel void FilterChain(__global float4 *input, __global float4 *output) {
    uint id = get_global_id(0);
    uint len = get_global_size(0);

    // Shall we do work?
    if(id < len) {
	PointColor v;
	v.point = input[id];
	
	v = filter_worley(v);
//	v = filter_saltandpepper(v);
//	v = filter_add(v);
	
	output[id] = v.color;
    }
} 
