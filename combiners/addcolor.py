class FilterAddColor(object):
	__FILENAME = 'addcolor.cl'
	
	def __init__(self,color=(0,0,0,0)):
		self.__defines = {}
		self.color = color
				
	def __loadCode(self):
		code = ''
		for k,v in self.__defines.iteritems():
			code += '#define {0} {1}\n'.format(k,v)
		with open(self.__FILENAME,'r') as inp: code += inp.read()
		code += '\n'
		return code
		
	def __repr__(self):
		return "Add Colo filter: color: {0}".format(self.color)
		
	def build_source(self):
		self.__defines['ADDCOLOR_COLOR'] = '({0:d},{1:d},{2:d},{3:d})'.format(*self.color)
		return self.__loadCode()
	
	def build_invocation_string(self):
		return 'v = filter_addcolor(v);'
