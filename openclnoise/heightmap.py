from basefilter import *

class HeightMap(BaseFilter):
    _filename = "heightmap.cl"
    def __init__(self,min_height=0,max_height=128):
        BaseFilter.__init__(self)
        self.min_height = min_height
        self.max_height = max_height
    
    def get_name(self):
        return "heightmap"
    
    def get_number_of_inputs(self):
        return 3
        
    @filter_argument(ArgumentTypes.FLOAT, 0)
    def min_height():
        def fget(self):
            return self._min_height
        def fset(self, value):
            self._min_height = float(value)
        return fget, fset, None
        
    @filter_argument(ArgumentTypes.FLOAT, 1)
    def max_height():
        def fget(self):
            return self._max_height
        def fset(self, value):
            self._max_height = float(value)
        return fget, fset, None

    def __repr__(self):
        return "HeightMap(min_height={0}, max_height={1})".format(self._min_height,self._max_height)
