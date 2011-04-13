import inspect
import os
from event import Event

class NotYetImplemented(Exception) : pass

class ArgumentTypes:
    FLOAT = "FLOAT"
    INT = "INT"
    FLOAT4 = "FLOAT4"
    INT4 = "INT4"

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
    
def float4(value):
    ret = tuple(value)
    if len(value) != 4: raise ValueError()
    
def int4(value):
    ret = tuple(value)
    if len(value) != 4: raise ValueError()

class BaseFilter(object):
    _filename = None
    def __init__(self):
        self.on_code_dirty = Event()      
    
    def get_name(self):
        raise NotYetImplemented()
    
    def get_number_of_inputs(self):
        raise NotYetImplemented()
        
    def generate_code(self):
        if self._filename:
            path = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), self._filename)
            with open(path) as file:
                return file.read()
        else: raise NotYetImplemented()
