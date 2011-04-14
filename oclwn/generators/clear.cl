PointColor /*id*/clear() {
    uint idX = get_global_id(0);
    uint idY = get_global_id(1);
    uint idZ = get_global_id(2);
    uint width = get_global_size(0);
    uint height = get_global_size(1);
    uint depth = get_global_size(2);
	
    //uint arrIdx = idX + idY * width + idZ * width * height;

    PointColor v;
    v.point.x = (float)idX/width;
    v.point.y = (float)idY/height;
    v.point.z = (float)idZ/depth;
	v.color.xyzw = 1;
	return v;
}