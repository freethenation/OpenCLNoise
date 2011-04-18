PointColor /*id*/over(PointColor input2, PointColor input1) {
	//ColorR = ColorS + (1-AlphaS)*ColorD
	//AlphaR = AlphaS + (1-AlphaS)*AlphaD
	float alpha1 = input1.color.w;
	float alpha2 = input2.color.w;
	input1.color = (input1.color*alpha1) + (1-alpha1)*(input2.color*alpha2);
	input1.color.w = alpha1 + (1-alpha1)*alpha2;
	return input1;
}

