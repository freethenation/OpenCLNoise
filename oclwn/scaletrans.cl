#ifndef SCALETRANS_SCALE
#define SCALETRANS_SCALE (10.0,10.0,1.0,0)
#endif
#ifndef SCALETRANS_TRANSLATE
#define SCALETRANS_TRANSLATE (0.0,0.0,0.0,0)
#endif

PointColor filter_scaletrans(PointColor input) {  
    input.point = input.point * (float4)SCALETRANS_SCALE + (float4)SCALETRANS_TRANSLATE;
    return input;
}

