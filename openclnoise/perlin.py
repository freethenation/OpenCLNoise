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
    
    def __init__(self,seed=0,maxdepth=8,persistence=0.8,initial_amplitude=0.4,initial_frequency=1.0):
        super(type(self),self).__init__()
        self._seed = seed
        self._maxdepth = maxdepth
        self._persistence = persistence
        self._initial_amplitude = initial_amplitude
    
    @filter_argument(ArgumentTypes.FLOAT, 0)
    def persistence():
        def fget(self):
            return self._persistence
        def fset(self, value):
            self._persistence = float(value)
        return fget, fset, None
    
    @filter_argument(ArgumentTypes.FLOAT, 1)
    def initial_amplitude():
        def fget(self):
            return self._initial_amplitude
        def fset(self, value):
            self._initial_amplitude = float(value)
        return fget, fset, None
        
    @filter_argument(ArgumentTypes.INT, 2)
    def maxdepth():
        def fget(self):
            return self._maxdepth
        def fset(self, value):
            self._maxdepth = int(value)
        return fget, fset, None
    
    @filter_argument(ArgumentTypes.INT, 3)
    def seed():
        def fget(self):
            return self._seed
        def fset(self, value):
            self._seed = int(value)
        return fget, fset, None
    
    def get_number_of_inputs(self):
        return 1
        
    def get_name(self):
        return 'perlin'
        
    def __repr__(self):
        return "Perlin(seed={0},maxdepth={1},persistence={2},initial_amplitude={3})".format(self._seed, self._maxdepth, self._persistence, self._initial_amplitude)
    
