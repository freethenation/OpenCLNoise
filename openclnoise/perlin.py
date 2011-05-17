from basefilter import *

#~ DISTANCES = {
    #~ 'euclidian': 0,
    #~ 'manhattan': 1,
    #~ 'chebyshev': 2,
    #~ 'chessboard': 2,
#~ }

#import re

class Perlin(BaseFilter):
    _filename = 'perlin.cl'
    
    def __init__(self,seed=0,maxdepth=8,persistence=0.9,initial_amplitude=1.0,initial_frequency=1.0): # function='F1',distance='euclidian',
        super(type(self),self).__init__()
        self._seed = seed
        self._maxdepth = maxdepth
        self._persistence = persistence
    
    @filter_argument(ArgumentTypes.FLOAT, 0)
    def persistence():
        def fget(self):
            return self._persistence
        def fset(self, value):
            self._persistence = float(value)
        return fget, fset, None
    
    @filter_argument(ArgumentTypes.INT, 1)
    def maxdepth():
        def fget(self):
            return self._maxdepth
        def fset(self, value):
            self._maxdepth = int(value)
        return fget, fset, None
    
    @filter_argument(ArgumentTypes.INT, 2)
    def seed():
        def fget(self):
            return self._seed
        def fset(self, value):
            self._seed = int(value)
        return fget, fset, None
    
    def get_number_of_inputs(self):
        return 1
    
    #~ @property
    #~ def function(self):
        #~ return self.__function
    #~ 
    #~ @function.setter
    #~ def function(self,value):
        #~ self.__function = value
        #~ self.__defines['WORLEY_NUMVALUES'] = max([int(m.group(1)) for m in re.finditer(r'F(\d*)',self.function)]) # Calculate how many values we must find
        #~ self.__defines['WORLEY_FUNCTION'] = self.__function 
        #~ for i in xrange(self.__defines['WORLEY_NUMVALUES']):
            #~ self.__defines['WORLEY_FUNCTION'] = self.__defines['WORLEY_FUNCTION'].replace('F{0}'.format(i+1),'F[{0}]'.format(i))
        #~ 
    #~ @property
    #~ def distance(self):
        #~ return self.__distance
#~ 
    #~ @distance.setter
    #~ def distance(self,value):
        #~ if not value in DISTANCES and value not in DISTANCES.values(): raise ValueError("Invalid distance. Valid options are: {0}".format(DISTANCES.keys()))
        #~ self.__distance = value
        #~ self.__defines['WORLEY_DISTANCE'] = DISTANCES[value]
    
    #~ def generate_code(self):
        #~ code = ''
        #~ for k,v in self.__defines.iteritems():
            #~ code += '#define /*id*/{0} {1}\n'.format(k,v)
        #~ code += super(type(self),self).generate_code()
        #~ return code
        
    def get_name(self):
        return 'perlin'
        
    def __repr__(self):
        return "Perlin()"
    
