from basefilter import *

class Select(BaseFilter):
    _filename = "select.cl"
    def __init__(self):
        BaseFilter.__init__(self)
    
    def get_name(self):
        return "select"
    
    def get_number_of_inputs(self):
        return 3
