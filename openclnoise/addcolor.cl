#ifndef /*id*/COLOR
#define /*id*/COLOR (.25,.25,.25,0)
#endif

PointColor /*id*/AddColor(PointColor input) {  
    input.color += (float4)/*id*/COLOR;
    input.color = clamp(input.color,0.0,1.0);
    return input;
}

