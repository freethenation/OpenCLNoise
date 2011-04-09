def Property(func): return property(**func())
class FilterScaleTrans(object):
	__FILENAME = 'scaletrans.cl'
	
	def __init__(self,scale=(1.0,1.0,1.0),translate=(0.0,0.0,0.0)):
		self.__defines = {}
		self.scale = scale
		self.translate = translate
				
	def __loadCode(self):
		code = ''
		for k,v in self.__defines.iteritems():
			code += '#define {0} {1}\n'.format(k,v)
		with open(self.__FILENAME,'r') as inp: code += inp.read()
		code += '\n'
		return code
		
	def __repr__(self):
		return "Scale/Translate: scale: {0}; translate: {1}".format(self.scale,self.translate)
		
	def build_source(self):
		self.__defines['SCALETRANS_SCALE'] = '({0:f},{1:f},{2:f},0)'.format(*self.scale)
		self.__defines['SCALETRANS_TRANSLATE'] = '({0:f},{1:f},{2:f},0)'.format(*self.translate)
		return self.__loadCode()
	
	def build_invocation_string(self):
		return 'v = filter_scaletrans(v);'
