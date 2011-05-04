PointColor /*id*/clear(float4 point) {
    PointColor v;
    v.point = point;
    v.color.xyzw = 1;
    return v;
}
