#define PARAM_GRAIN_SIZE .025
#define PARAM_SALT_TARGET 214748360
#define PARAM_PEPPER_TARGET 429496720
#define PARAM_SALT_COLOR 0.85
#define PARAM_PEPPER_COLOR 0.05

PointColor filter_saltandpepper(PointColor input) {  
    IntPoint cube;
    
    Point white,black;
    white.x = PARAM_SALT_COLOR;
    white.y = PARAM_SALT_COLOR;
    white.z = PARAM_SALT_COLOR;
    black.x = PARAM_PEPPER_COLOR;
    black.y = PARAM_PEPPER_COLOR;
    black.z = PARAM_PEPPER_COLOR;
    
    cube.x = input.point.x / PARAM_GRAIN_SIZE;
    cube.y = input.point.y / PARAM_GRAIN_SIZE;
    cube.z = input.point.z / PARAM_GRAIN_SIZE;
    
    uint val = rng(hash(cube.x, cube.y, cube.z));
    if(val < PARAM_SALT_TARGET)
		input.color.xyz = white.xyz;
    else if(val > PARAM_SALT_TARGET && val < PARAM_PEPPER_TARGET)
		input.color.xyz = black.xyz;

	return input;
}

