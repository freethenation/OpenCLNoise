from basefilter import *

class Clear(BaseFilter):
    _filename = "clear.cl"
    def __init__(self):
        BaseFilter.__init__(self)
    
    def get_name(self):
        return "clear"
    
    def get_number_of_inputs(self):
        return 0

    def __repr__(self):
        return 'Clear()'
