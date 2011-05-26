import inspect
import string
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
    for t in (float,int,long):
        if isinstance(value,t):
            value = (t,t,t,1.0)

    ret = tuple(value)
    if len(ret) == 3: ret = (ret[0],ret[1],ret[2],1.0)
    if len(ret) != 4: raise ValueError()

    return ret

int4 = float4
    
# def int4(value):
#     for t in (float,int,long):
#         if isinstance(value,t):
#             value = (t,t,t,1)

#     ret = tuple(value)
#     if len(ret) == 3: ret = tuple(list(ret) + [0.0])
#     if len(ret) != 4: raise ValueError()
#     return ret

def SimpleFilterFactory(filter_name, file_name, num_inputs):
    class SimpleFilter(BaseFilter):
        _filename = file_name
        def __init__(self):
            BaseFilter.__init__(self)
        
        def get_name(self):
            return filter_name
        
        def get_number_of_inputs(self):
            return num_inputs
    return SimpleFilter
    

class BaseFilter(object):
    _filename = None
    def __init__(self):
        self._defines = {}
        self.on_code_dirty = Event()      
    
    def get_name(self):
        raise NotYetImplemented()
    
    def get_number_of_inputs(self):
        raise NotYetImplemented()
        
    def generate_code(self):
        code = ''
        for k,v in self._defines.iteritems():
            code += '#define /*id*/{0} {1}\n'.format(k,v)
        
        if self._filename:
            path = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), self._filename)
            with open(path) as file:
                code += file.read()
            return code
        else: raise NotYetImplemented()
        
    def __repr__(self):
        raise NotYetImplemented()
