PointColor /*id*/lut(PointColor input) {
	float4 avg = (input.color.x+input.color.y+input.color.z)/3.0f;
	if(false){}
	#else if(avg < END){return lerp((float4)A,(float4)B,(START - avg)/(START - END));}
	CODE_HERE
	return input;
}