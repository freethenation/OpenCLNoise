from basefilter import *

class ScaleTrans(BaseFilter):
    _filename = "scaletrans.cl"
    def __init__(self,scale=(1.0,1.0,1.0,1.0),translate=(0.0,0.0,0.0,0.0)):
        super(type(self),self).__init__()
        self._scale = scale
        self._translate = translate
    
    def get_name(self):
        return "scaletrans"
    
    def get_number_of_inputs(self):
        return 1
    
    @filter_argument(ArgumentTypes.FLOAT4, 0)
    def scale():
        def fget(self):
            return self._scale
        def fset(self, value):
            self._scale = float4(value)
        return fget, fset, None
        
    @filter_argument(ArgumentTypes.FLOAT4, 1)
    def translate():
        def fget(self):
            return self._translate
        def fset(self, value):
            self._translate = float4(value)
        return fget, fset, None
