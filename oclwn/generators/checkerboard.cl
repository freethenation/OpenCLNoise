#define CHECKERBOARD_BLACK_COLOR (float4)(0.0,0.0,0.0,1.0)
#define CHECKERBOARD_WHITE_COLOR (float4)(1.0,1.0,1.0,1.0)

PointColor filter_checkerboard(PointColor input) {
    int4 point = convert_int4(input.point);
    if((point.x + point.y + point.z) % 2 == 0)
        input.color = CHECKERBOARD_BLACK_COLOR;
    else
        input.color = CHECKERBOARD_WHITE_COLOR;
    return input;
}

