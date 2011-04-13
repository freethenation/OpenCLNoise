import inspect
from os import path
from event import Event

class NotYetImplemented(Exception) : pass

class ArgumentTypes:
    FLOAT4 = "FLOAT4"
    INT4 = "INT4"
    INT = "INT"
    FLOAT = "FLOAT"

class FilterArgument(object) :
    def __init__(self, argument_type, argument_index, fget, fset=None, fdel=None):
        self.type = argument_type
        self.index = argument_index
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
    def __get__(self, instance, owner_type):
        if self.fget: return self.fget(instance)
    def __set__(self, instance, value):
        if self.fset: self.fset(instance, value)
    def __delete__(self, instance):
        if self.fdel: self.fdel(instance)        
        
def filter_argument(argument_type, argument_index):
    def _filter_argument(func):
        fget, fset, fdel = func()
        return FilterArgument(argument_type, argument_index, fget, fset, fdel)
    return _filter_argument

class BaseFilter(object):
    _filename = None
    def __init__(self):
        self.on_code_dirty = Event()      
    
    def get_number_of_inputs(self):
        raise NotYetImplemented()
        
    def generate_code(self):
        if not self._filename:
            path = path.join(path.dirname(inspect.getfile(self.__class__)), _filename)
            with open(path) as file:
                return file.read()
        else: raise NotYetImplemented()
        
#class TestFilter(BaseFilter):
#    def __init__(self):
#        self._value = None
#        def changed(old, new):
#            print old, new
#        self.s = SimpleFilterArgument(ArgumentTypes.INT, 0, changed)
#    
#    @filter_argument(ArgumentTypes.INT, 0)
#    def value():
#        def fget(self):
#            return self._value
#        def fset(self, value):
#            self._value = value
#        return fget, fset, None
