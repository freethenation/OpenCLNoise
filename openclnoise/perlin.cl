//#pragma OPENCL EXTENSION cl_amd_printf : enable

float InterpolatedNoise(float4 finput) {
    float4 frac,junk;
    int4 iinput;
    frac = modf(finput,&junk);
    iinput = convert_int4_rtn(finput);
    //iinput = convert_int4(junk);
    
    frac.x = frac.x >= 0 ? frac.x : frac.x + 1;
    frac.y = frac.y >= 0 ? frac.y : frac.y + 1;
    frac.z = frac.z >= 0 ? frac.z : frac.z + 1;
    
    /*if(iinput.x < 0) iinput.x -= 1;
    if(iinput.y < 0) iinput.y -= 1;
    if(iinput.z < 0) iinput.z -= 1;*/
    
    //finput = -5.3
    //frac = -0.3
    //iinput = -5
    
    //iinput = convert_int4_rtn(finput);
    //frac = finput - convert_float4(convert_int4((finput)));
    
    //if(finput.x < 0 || finput.y < 0 || finput.z < 0)
    //    printf("i = %d,%d,%d   f = %f,%f,%f\n",iinput.x,iinput.y,iinput.z,frac.x,frac.y,frac.z);
    //~ frac = modf(finput,&junk);
    //~ int4 iinput = convert_int4(junk);
    
    //printf("%f,%f,%f : %d,%d,%d , %f,%f,%f\n",finput.x,finput.y,finput.z,iinput.x,iinput.y,iinput.z,frac.x,frac.y,frac.z);
    
    float v1,v2,v3,v4,v5,v6,v7,v8;
    float i1,i2,i3,i4;
    float j1,j2;
    
    v1 = good_rng(hash(iinput.x+0,iinput.y+0,iinput.z+0)) / (float)0x100000000;
    v2 = good_rng(hash(iinput.x+1,iinput.y+0,iinput.z+0)) / (float)0x100000000;
    v3 = good_rng(hash(iinput.x+0,iinput.y+1,iinput.z+0)) / (float)0x100000000;
    v4 = good_rng(hash(iinput.x+1,iinput.y+1,iinput.z+0)) / (float)0x100000000;
    v5 = good_rng(hash(iinput.x+0,iinput.y+0,iinput.z+1)) / (float)0x100000000;
    v6 = good_rng(hash(iinput.x+1,iinput.y+0,iinput.z+1)) / (float)0x100000000;
    v7 = good_rng(hash(iinput.x+0,iinput.y+1,iinput.z+1)) / (float)0x100000000;
    v8 = good_rng(hash(iinput.x+1,iinput.y+1,iinput.z+1)) / (float)0x100000000;
    
    //if(get_global_id(0) == 0) 
    //    printf("%f,%f,%f -> %f,%f,%f AND %d,%d,%d\n",v1,v2,v3,v4,v5,v6);
    
    i1 = INTERPOLATOR(v1,v2,frac.x);
    i2 = INTERPOLATOR(v3,v4,frac.x);
    i3 = INTERPOLATOR(v5,v6,frac.x);
    i4 = INTERPOLATOR(v7,v8,frac.x);
    
    j1 = INTERPOLATOR(i1,i2,frac.y);
    j2 = INTERPOLATOR(i3,i4,frac.y);
    
    return INTERPOLATOR(j1,j2,frac.z);
}

PointColor /*id*/perlin(PointColor input, float persistence, int maxdepth, int seed) {   
    FLOAT_T total = 0;
    uint frequency = 1;
    float amplitude = 0.25;
      
    for(int i=0; i < maxdepth; ++i) {
        total += InterpolatedNoise(input.point*frequency) * amplitude;
        frequency *= 2;
        amplitude *= persistence;
    }
    
    input.color.xyz = total;
    input.color.w = 1;
    
    input.color = clamp(input.color,0.0f,1.0f);
    
    return input;
}

