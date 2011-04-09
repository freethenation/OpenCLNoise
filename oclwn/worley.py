DISTANCES = {
	'euclidian': 0,
	'manhattan': 1,
	'chebyshev': 2,
	'chessboard': 2,
}

import re

def Property(func): return property(**func())
class FilterWorley(object):
	__FILENAME = 'worley.cl'
	__INPUTS = 1
	__FLOATARGS = 0
	__INTARGS = 1
	__FLOAT4ARGS = 0
	__INT4ARGS = 0
	
	def __init__(self,function='F1',distance='euclidian'):
		self.__function = ''
		self.__distance = ''
		self.__defines = {}
		self.distance = distance
		self.function = function
		
	@Property
	def function():
		def fget(self):
			return self.__function
		def fset(self,value):
			self.__function = value
			self.__setDefinesFromFunction()
		return locals()
		
	@Property
	def distance():
		def fget(self):
			return self.__distance
		def fset(self,value):
			if not value in DISTANCES and value not in DISTANCES.values(): raise ValueError("Invalid distance. Valid options are: {0}".format(DISTANCES.keys()))
			self.__distance = value
			self.__defines['WORLEY_DISTANCE'] = DISTANCES[value]
		return locals()
			
	def __setDefinesFromFunction(self):
		self.__defines['WORLEY_NUMVALUES'] = max([int(m.group(1)) for m in re.finditer(r'F(\d*)',self.function)]) # Calculate how many values we must find
		self.__defines['WORLEY_FUNCTION'] = self.__function 
		for i in xrange(self.__defines['WORLEY_NUMVALUES']):
			self.__defines['WORLEY_FUNCTION'] = self.__defines['WORLEY_FUNCTION'].replace('F{0}'.format(i+1),'F[{0}]'.format(i))
		
	def __loadCode(self):
		code = ''
		for k,v in self.__defines.iteritems():
			code += '#define {0} {1}\n'.format(k,v)
		with open(self.__FILENAME,'r') as inp: code += inp.read()
		code += '\n'
		return code
		
	def __repr__(self):
		return "Worley: noise f = {0}; distance f = {1}".format(self.function,self.distance)
		
	def build_source(self):
		return self.__loadCode()
	
	def build_invocation_string(self):
		return 'v = filter_worley(v);'
