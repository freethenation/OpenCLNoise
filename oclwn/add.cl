#define PARAM_RED_ADD .25
#define PARAM_GREEN_ADD .25
#define PARAM_BLUE_ADD .25
#define PARAM_ALPHA_ADD 0

PointColor filter_add(PointColor input) {  
    input.color.x += PARAM_RED_ADD;
    input.color.y += PARAM_GREEN_ADD;
    input.color.z += PARAM_BLUE_ADD;
    input.color.w += PARAM_ALPHA_ADD;
    input.color = clamp(input.color,0.0,1.0);
    return input;
}

