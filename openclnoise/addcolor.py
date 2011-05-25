from basefilter import *

class AddColor(BaseFilter):
    _filename = "addcolor.cl"
    def __init__(self, color=(0.25,0.25,0.25,0)):
        BaseFilter.__init__(self)
        self.color = color
    
    def get_name(self):
        return "AddColor"
    
    def get_number_of_inputs(self):
        return 1
    
    @property
    def color(self): 
        return self._defines['COLOR']
    
    @color.setter
    def color(self,value):
        self._defines['COLOR'] = value
        self.on_code_dirty(self)

    def __repr__(self):
        return "AddColor(color={0})".format(self.color)
