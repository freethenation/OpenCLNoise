from basefilter import *

DISTANCES = {
    'euclidian': 0,
    'manhattan': 1,
    'chebyshev': 2,
    'chessboard': 2,
}

import re

#def Property(func): return property(**func())
class Worley(BaseFilter):
    _filename = 'worley.cl'
    
    def __init__(self,function='F1',distance='euclidian',seed=0):
        super(type(self),self).__init__()
        self.__function = ''
        self.__distance = ''
        self.__seed = 0
        self.__defines = {}
        self.distance = distance
        self.function = function
        self.seed = seed
    
    def get_number_of_inputs(self):
        return 1
    
    @property
    def function(self):
        return self.__function
    
    @function.setter
    def function(self,value):
        self.__function = value
        self.__defines['NUMVALUES'] = max([int(m.group(1)) for m in re.finditer(r'F(\d*)',self.function)]) # Calculate how many values we must find
        self.__defines['FUNCTION'] = self.__function 
        for i in xrange(self.__defines['NUMVALUES']):
            self.__defines['FUNCTION'] = self.__defines['FUNCTION'].replace('F{0}'.format(i+1),'F[{0}]'.format(i))
        self.on_code_dirty(self)
        
    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self,value):
        if not value in DISTANCES and value not in DISTANCES.values(): raise ValueError("Invalid distance. Valid options are: {0}".format(DISTANCES.keys()))
        self.__distance = value
        self.__defines['DISTANCE'] = DISTANCES[value]
        self.on_code_dirty(self)
    
    @filter_argument(ArgumentTypes.INT, 0)
    def seed():
        def fget(self):
            return self._seed
        def fset(self, value):
            self._seed = int(value)
        return fget, fset, None
    
    def generate_code(self):
        code = ''
        for k,v in self.__defines.iteritems():
            code += '#define /*id*/{0} {1}\n'.format(k,v)
        code += super(type(self),self).generate_code()
        return code
        
    def get_name(self):
        return 'worley'
        
    def __repr__(self):
        return "Worley(function={0},distance='{1}',seed={2})".format(self.function,self.distance,self.seed)
    
