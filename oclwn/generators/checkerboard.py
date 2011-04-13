import basefilter

class CheckerBoard(BaseFilter):
    _filename = "checkerboard.cl"
    def __init__(self):
        BaseFilter.__init__(self)
        self._black_color = (0.0,0.0,0.0,1.0)
        self._white_color = (1.0,1.0,1.0,1.0)
    
    def get_name(self):
        return "checkerboard"
    
    def get_number_of_inputs(self):
        return 0
    
    @filter_argument(ArgumentTypes.FLOAT4, 0)
    def black_color():
        def fget(self):
            return self._black_color
        def fset(self, value):
            self._black_color = value
        return fget, fset, None
        
    @filter_argument(ArgumentTypes.FLOAT4, 1)
    def black_color():
        def fget(self):
            return self._white_color
        def fset(self, value):
            self._white_color = value
        return fget, fset, None
