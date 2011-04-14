PointColor /*id*/select(PointColor input1, PointColor input2, PointColor selector) {
	if((selector.color.x+selector.color.y+selector.color.z)/3.0 <= 0.5) return input1;
	else return input2;
}