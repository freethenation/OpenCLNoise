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
