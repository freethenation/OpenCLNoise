__kernel void sumreduce(__global float *arr, const uint stride) {
    ulong idx = get_global_id(0) * stride;
    if(idx > get_global_size(0) || idx + stride/2 > get_global_size(0))
	return;
    arr[idx] += arr[idx+stride/2];
}
