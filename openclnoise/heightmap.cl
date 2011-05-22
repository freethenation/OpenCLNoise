PointColor /*id*/heightmap(PointColor air, PointColor ground, PointColor selector, float min_height, float max_height) {
	float y = air.point.y;
	if(y < min_height) {
	  ground.color.w = 0;
	  return ground;
	} else if(y > max_height) {
	  air.color.w = 1;
	  return air;
	} else {
		  float scaled_y = (y - min_height) / (max_height - min_height);
		  float avg_color = (selector.color.x+selector.color.y+selector.color.z) / 3.0;
		  //printf("point: %f,%f,%f s: %f c: %f\n",air.point.x,air.point.y,air.point.z,scaled_y, avg_color);
		  
		  if(scaled_y > avg_color) {
				air.color.w = (avg_color - scaled_y + 1) / 2;
				return air;
		  } 
		  else {
				ground.color.w = (avg_color - scaled_y + 1) / 2;
				return ground;
		  }	  
	}
}
