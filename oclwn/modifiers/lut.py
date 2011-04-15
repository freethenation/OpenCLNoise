from basefilter import *

class Lut(BaseFilter):
    _filename = "lut.cl"
    def __init__(self):
        BaseFilter.__init__(self)
    
    def get_name(self):
        return "lut"
    
    def get_number_of_inputs(self):
        return 1
