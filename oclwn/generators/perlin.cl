//#pragma OPENCL EXTENSION cl_amd_printf : enable

float InterpolatedNoise(float4 finput) {
    int4 iinput = convert_int4(finput);
    float4 frac,junk;
    frac = modf(finput,&junk);
    
    //printf("%f,%f,%f : %d,%d,%d , %f,%f,%f\n",finput.x,finput.y,finput.z,iinput.x,iinput.y,iinput.z,frac.x,frac.y,frac.z);
    
    float v1,v2,v3,v4,v5,v6,v7,v8;
    float i1,i2,i3,i4;
    float j1,j2;
    
    v1 = rng(hash(iinput.x+0,iinput.y+0,iinput.z+0)) / (float)0x100000000;
    v2 = rng(hash(iinput.x+1,iinput.y+0,iinput.z+0)) / (float)0x100000000;
    v3 = rng(hash(iinput.x+0,iinput.y+1,iinput.z+0)) / (float)0x100000000;
    v4 = rng(hash(iinput.x+1,iinput.y+1,iinput.z+0)) / (float)0x100000000;
    v5 = rng(hash(iinput.x+0,iinput.y+0,iinput.z+1)) / (float)0x100000000;
    v6 = rng(hash(iinput.x+1,iinput.y+0,iinput.z+1)) / (float)0x100000000;
    v7 = rng(hash(iinput.x+0,iinput.y+1,iinput.z+1)) / (float)0x100000000;
    v8 = rng(hash(iinput.x+1,iinput.y+1,iinput.z+1)) / (float)0x100000000;
    
    i1 = lerp(v1,v2,frac.x);
    i2 = lerp(v3,v4,frac.x);
    i3 = lerp(v5,v6,frac.x);
    i4 = lerp(v7,v8,frac.x);
    
    j1 = lerp(i1,i2,frac.y);
    j2 = lerp(i3,i4,frac.y);
    
    return lerp(j1,j2,frac.z);
}

PointColor /*id*/perlin(PointColor input, float persistence, int maxdepth, int seed) {   
    FLOAT_T total = 0;
    uint frequency = 1;
    float amplitude = 1;
  
//    printf("%f\n",input.point.x*100.0);
//    printf("%d,%f,%f,%f\n",get_global_id(0),input.point.x,input.point.y,input.point.z);
    
    for(int i=0; i < maxdepth; ++i) {
	frequency *= 2;
	amplitude *= persistence;
	total += InterpolatedNoise(input.point*frequency) * amplitude;
    }
    
    input.color.xyz = total;
    input.color.w = 1;
    
    input.color = clamp(input.color,0.0f,1.0f);
    
    return input;
}

