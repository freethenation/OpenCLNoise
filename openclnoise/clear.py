from basefilter import *

class Clear(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
    
    def get_name(self):
        return "clear"
    
    def get_number_of_inputs(self):
        return 0

    def generate_code(self):
        raise Exception("Code for Clear() found in kernel.")

    def __repr__(self):
        return 'Clear()'
