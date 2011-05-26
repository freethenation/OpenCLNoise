from basefilter import *

class ScaleTrans(BaseFilter):
    _filename = "scaletrans.cl"
    def __init__(self,scale=(1.0,1.0,1.0),translate=(0.0,0.0,0.0)):
        super(type(self),self).__init__()
        self._scale = scale
        self._translate = translate
    
    def get_name(self):
        return "scaletrans"
    
    def get_number_of_inputs(self):
        return 1
    
    def __mul__(self,other):
        if type(other) in (int,float,long):
            return ScaleTrans(scale=map(lambda x: other*x,self.scale),translate=self.translate)
        return NotImplemented

    def __div__(self,other):
        return self * (1.0/other)

    @filter_argument(ArgumentTypes.FLOAT4, 0)
    def scale():
        def fget(self):
            return float4(self._scale)
        def fset(self, value):
            self._scale = float4(value)
        return fget, fset, None
        
    @filter_argument(ArgumentTypes.FLOAT4, 1)
    def translate():
        def fget(self):
            return float4(self._translate)
        def fset(self, value):
            self._translate = float4(value)
        return fget, fset, None

    def __repr__(self):
        return "ScaleTrans(scale=(%.2f,%.2f,%.2f), translate=(%.2f,%.2f,%.2f))" % (self.scale[0],self.scale[1],self.scale[2],self.translate[0],self.translate[1],self.translate[2])
