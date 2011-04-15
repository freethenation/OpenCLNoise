from basefilter import *

class Over(BaseFilter):
    _filename = "over.cl"
    def __init__(self):
        BaseFilter.__init__(self)
    
    def get_name(self):
        return "over"
    
    def get_number_of_inputs(self):
        return 2
