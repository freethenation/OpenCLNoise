#ifndef ADDCOLOR_COLOR
#define ADDCOLOR_COLOR (float4)(.25,.25,.25,0)
#endif

PointColor filter_addcolor(PointColor input) {  
    input.color += ADDCOLOR_COLOR;
    input.color = clamp(input.color,0.0,1.0);
    return input;
}

