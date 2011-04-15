#ifndef
#define LVL(a,b,start,end) else if(avg < end){return lerp((float4)a,(float4)b,(start - avg)/(start - end));}
#endif

PointColor /*id*/lut(PointColor input) {
	float4 avg = (input.color.x+input.color.y+input.color.z)/3.0;
	if(false){}
	#ifndef /*id*/CODE
	LVL((0.0,0.0,0.0,1.0),(1.0,0.0,0.0,1.0), 0.0, .4)
	LVL((1.0,0.0,0.0,1.0),(0.0,1.0,0.0,1.0), .4, .8)
	LVL((0.0,1.0,0.0,1.0),(1.0,1.0,1.0,1.0), .8, 1.0)
	#endif
	return input;
}