PointColor /*id*/clear(int4 totalChunks, int4 currentChunk) {
    uint idX = get_global_id(0);
    uint idY = get_global_id(1);
    uint idZ = get_global_id(2);
    uint width = get_global_size(0);
    uint height = get_global_size(1);
    uint depth = get_global_size(2);
	
    //uint arrIdx = idX + idY * width + idZ * width * height;

    PointColor v;
    v.point.x = (float)idX / width / totalChunks.x + currentChunk.x / totalChunks.x;
    v.point.y = (float)idY / height / totalChunks.y + currentChunk.y / totalChunks.y;
    v.point.z = (float)idZ / depth / totalChunks.z + currentChunk.z / totalChunks.z;
    
    v.color.xyzw = 1;
    return v;
}
