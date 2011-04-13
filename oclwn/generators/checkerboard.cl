PointColor /*id*/checkerboard(PointColor input, float4 blackColor, float4 whiteColor) {
    int4 point = convert_int4(input.point);
    if((point.x + point.y + point.z) % 2 == 0)
        input.color = blackColor;
    else
        input.color = whiteColor;
    return input;
}

