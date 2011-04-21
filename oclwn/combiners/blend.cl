#ifndef BlendMacros
	#define BlendMacros
	#define ChannelBlend_Normal(B,L)     (B)
	#define ChannelBlend_Lighten(B,L)    ((L > B) ? L:B)
	#define ChannelBlend_Darken(B,L)     ((L > B) ? B:L)
	#define ChannelBlend_Multiply(B,L)   ((B * L) / 1.0)
	#define ChannelBlend_Average(B,L)    ((B + L) / 2)
	#define ChannelBlend_Add(B,L)        (B + L)
	#define ChannelBlend_Subtract(B,L)   (B + L - 1.0)
	#define ChannelBlend_Difference(B,L) (abs(B - L))
	#define ChannelBlend_Negation(B,L)   (1.0 - abs(1.0 - B - L))
	#define ChannelBlend_Screen(B,L)     (1.0 - ((1.0 - B) * (1.0 - L)))
	#define ChannelBlend_Exclusion(B,L)  (B + L - 2 * B * L / 1.0)
	#define ChannelBlend_Overlay(B,L)    ((L < 0.5) ? (2 * B * L):(1.0 - 2 * (B - 0.5) * (1.0 - L)))
	//#define ChannelBlend_SoftLight(B,L)  ((L < 0.5)?(2*((B>>1)+64))*((float)L/1.0):(1.0-(2*(1.0-((B>>1)+64))*(float)(1.0-L)/1.0)))
	#define ChannelBlend_SoftLight(B,L)  (((1.0-L)*B*L)+ (L*ChannelBlend_Screen(B,L)))
	#define ChannelBlend_HardLight(B,L)  (ChannelBlend_Overlay(L,B))
	#define ChannelBlend_ColorDodge(B,L) (B/(1.0-L))
	#define ChannelBlend_ColorBurn(B,L)  (1-(1.0-B)/L)
	#define ChannelBlend_LinearDodge(B,L)(ChannelBlend_Add(B,L))
	#define ChannelBlend_LinearBurn(B,L) (ChannelBlend_Subtract(B,L))
	#define ChannelBlend_LinearLight(B,L)((L < 0.5)?ChannelBlend_LinearBurn(B,(2 * L)):ChannelBlend_LinearDodge(B,(2 * (L - 0.5))))
	#define ChannelBlend_VividLight(B,L) ((L < 0.5)?ChannelBlend_ColorBurn(B,(2 * L)):ChannelBlend_ColorDodge(B,(2 * (L - 0.5))))
	#define ChannelBlend_PinLight(B,L)   ((L < 0.5)?ChannelBlend_Darken(B,(2 * L)):ChannelBlend_Lighten(B,(2 * (L - 0.5))))
	#define ChannelBlend_HardMix(B,L)    ((ChannelBlend_VividLight(B,L) < 0.5) ? 0:1.0)
	#define ChannelBlend_Reflect(B,L)    ((L == 1.0) ? L:min(1.0, (B * B / (1.0 - L))))
	#define ChannelBlend_Glow(B,L)       (ChannelBlend_Reflect(L,B))
	#define ChannelBlend_Phoenix(B,L)    (min(B,L) - max(B,L) + 1.0)
	#define ChannelBlend_Alpha(B,L,O)    (B + (1.0 - O) * L)
	#define ChannelBlend_AlphaF(B,L,F,O) (ChannelBlend_Alpha(F(B,L),B,O))
#endif

#ifndef /*id*/CHANNEL_BLEND_FUNC
	#define /*id*/CHANNEL_BLEND_FUNC = ChannelBlend_Normal
#endif

PointColor /*id*/blend(PointColor input2, PointColor input1) {
	//Get Alphas
	float alpha1 = input1.color.w;
	float alpha2 = input2.color.w;
	//Pre multiply by Alphas
	input1.color *= alpha1;
	input2.color *= alpha2;
	//Apply blend
	input1.color = ChannelBlend_AlphaF(input1.color, input2.color, /*id*/CHANNEL_BLEND_FUNC, alpha1);
	input1.color.w = alpha1 + (1-alpha1)*alpha2;
	return input1;
}

