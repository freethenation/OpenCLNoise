PointColor scaletrans(PointColor input, float4 scale, float4 translate) {  
    input.point = input.point * scale + translate;
    return input;
}

