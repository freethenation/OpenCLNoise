PointColor /*id*/select(PointColor input1, PointColor input2, PointColor selector) {
	if(selector.color.x+selector.color.y+selector.color.z <= 0.5*3.0) return input1;
	else return input2;
}