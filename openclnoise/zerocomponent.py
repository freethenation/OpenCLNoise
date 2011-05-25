from basefilter import *

class ZeroComponent(BaseFilter):
    _filename = "zerocomponent.cl"
    def __init__(self, component='y'):
        BaseFilter.__init__(self)
        self.component = component
    
    def get_name(self):
        return "zerocomponent"
    
    def get_number_of_inputs(self):
        return 1
    
    @property
    def component(self): 
        return self._defines['COMPONENT']
    
    @component.setter
    def component(self,value):
        self._defines['COMPONENT'] = value
        self.on_code_dirty(self)

    def __repr__(self):
        return "ZeroComponent(component=\"{0}\")".format(self.component)
