import re

WORLEY_DISTANCES_EUCLIDIAN = 0
WORLEY_DISTANCES_MANHATTAN = 1
WORLEY_DISTANCES_CHESSBOARD = 2

def Property(func): return property(**func())

class FilterWorley(object):
	__defines = {}
	__function = __distance = ''
	def __init__(self,function='F1',distance=WORLEY_DISTANCES_EUCLIDIAN):
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
			self.__distance = value
			if self.__distance in ('euclidian',WORLEY_DISTANCES_EUCLIDIAN):
				self.__defines['our_distance(p1,p2)'] = '(p1.x-p2.x)*(p1.x-p2.x) + (p1.y-p2.y)*(p1.y-p2.y) + (p1.z-p2.z)*(p1.z-p2.z)'
			elif self.__distance in ('manhatten',WORLEY_DISTANCES_MANHATTAN):
				self.__defines['our_distance(p1,p2)'] = 'fabs(p1.x-p2.x) + fabs(p1.y-p2.y) + fabs(p1.z-p2.z)'
			elif self.__distance in ('chessboard',WORLEY_DISTANCES_CHESSBOARD):
				self.__defines['our_distance(p1,p2)'] = 'max(max(fabs(p1-p2).x,fabs(p1-p2).y),fabs(p1-p2).z)'
			else: raise ValueError("Unknown distance types. Valid values: 'euclidian', 'manhatten', 'chessboard'")
		return locals()
			
	def __setDefinesFromFunction(self):
		self.__defines['WORLEY_N'] = max([int(m.group(1)) for m in re.finditer(r'F(\d*)',self.function)])
		self.__defines['WORLEY_FUNCTION'] = self.__function
		for i in xrange(self.__defines['WORLEY_N']):
			self.__defines['WORLEY_FUNCTION'] = self.__defines['WORLEY_FUNCTION'].replace('F{0}'.format(i+1),'darr[{0}]'.format(i))
		
	def __loadCode(self):
		code = ''
		for k,v in self.__defines.iteritems():
			code += '#define {0} {1}\n'.format(k,v)
		with open('worley.cl','r') as inp: code += inp.read()
		code += '\n'
		return code
		
	def __repr__(self):
		return "Worley filter: noise f = {0}; distance f = {1}".format(self.function,self.distance)
		
	def build_source(self):
		return self.__loadCode()
	
	def build_invocation_string(self):
		return 'v = filter_worley(v);'
