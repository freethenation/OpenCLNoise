from basefilter import *

class CheckerBoard(BaseFilter):
    _filename = "checkerboard.cl"
    def __init__(self, black_color=(0.0,0.0,0.0,1.0), white_color=(1.0,1.0,1.0,1.0), constant_color=None):
        BaseFilter.__init__(self)
        self._black_color = black_color
        self._white_color = white_color
        if constant_color is not None: 
            self.constant_color = constant_color
        
    
    def get_name(self):
        return "checkerboard"
    
    def get_number_of_inputs(self):
        return 1
    
    @property
    def constant_color(self):
        return self.black_color
        
    @constant_color.setter
    def constant_color(self,color):
        if isinstance(color,float) or isinstance(color,int) or isinstance(color,long): 
            color = (color,color,color,1.0)
        self.black_color = float4(color)
        self.white_color = float4(color)
    
    @filter_argument(ArgumentTypes.FLOAT4, 0)
    def black_color():
        def fget(self):
            return self._black_color
        def fset(self, value):
            self._black_color = float4(value)
        return fget, fset, None
        
    @filter_argument(ArgumentTypes.FLOAT4, 1)
    def white_color():
        def fget(self):
            return self._white_color
        def fset(self, value):
            self._white_color = float4(value)
        return fget, fset, None

    def __repr__(self):
        return "CheckerBoard(black_color={0},white_color={1})".format(self.black_color, self.white_color)
        
Constant = CheckerBoard
