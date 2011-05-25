from basefilter import *

class HeightMap(BaseFilter):
    _filename = "heightmap.cl"
    def __init__(self,min_height=0,max_height=128,component='y'):
        BaseFilter.__init__(self)
        self.min_height = min_height
        self.max_height = max_height
        self.component = component
    
    def get_name(self):
        return "heightmap"
    
    def get_number_of_inputs(self):
        return 3
        
    @property
    def component(self):
        return self._defines['COMPONENT']
        
    @component.setter
    def component(self,value):
        self._defines['COMPONENT'] = value
        self.on_code_dirty(self)
        
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
        return "HeightMap(min_height={0}, max_height={1}, component=\"{2}\")".format(self._min_height,self._max_height,self.component)
