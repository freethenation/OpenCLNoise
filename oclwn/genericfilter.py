class GenericFilter(object):
	def __init__(self,filename,invocation,defines={}):
		self.__defines = defines
		self.__FILENAME = filename
		self.invocation = invocation
				
	def __loadCode(self):
		code = ''
		for k,v in self.__defines.iteritems():
			code += '#define {0} {1}\n'.format(k,v)
		with open(self.__FILENAME,'r') as inp: code += inp.read()
		code += '\n'
		return code
		
	def __repr__(self):
		return 'Generic Filter: file: {0}; inv: "{1}"'.format(self.__FILENAME,self.invocation)
		
	def build_source(self):
		return self.__loadCode()
	
	def build_invocation_string(self):
		return self.invocation
