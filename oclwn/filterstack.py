from basefilter import FilterArgument,ArgumentTypes
import time
import logging as log
import pyopencl as cl
from event import Event
import numpy

class FilterRuntime(object):
    def __init__(self):
        self.on_code_dirty = Event()
        self._device = None
        self.__context = None
        self.__queue = None
        devices = self.get_devices()
        if(len(devices) > 0): 
            log.warn("Selecting default OpenCL device '{0}'. Use get_devices() to get a full list of available devices.".format(devices[0].name))
            self.device = devices[0]
    
    def get_devices(self):
        platforms = cl.get_platforms()
        if len(platforms) < 1: 
            log.error("No OpenCL platforms found!")
            return []
        if len(platforms) > 1:
            log.warn("{0} OpenCL platforms were found. Selecting the first one.".format(len(platforms)))
        devices = platforms[0].get_devices()
        return devices
        
    def compile(self, code):
        return cl.Program(self.context, code).build()

    def run(self, compiled_program, kernel_name, output_width, output_height, output_depth, args_float, args_int, args_float4, args_int4):
        output = numpy.zeros((output_width*output_height*output_depth,4),numpy.float32)
        output_buf = cl.Buffer(self.context, cl.mem_flags.WRITE_ONLY | cl.mem_flags.USE_HOST_PTR, hostbuf=output)
        
        # Make a buffer out of x. y is type of buffer: 0 - float, 1 - int, 2 - float4, 3 - walrus; returns buffer of 1 element if array is empty
        def m(x,y):
            if not x:
                if y in (2,3):
                    x = [0,0,0,0]
                else:
                    x = 0
            if y in (0,2):
                typ = numpy.float32
            else:
                typ = numpy.int32
            if y in (2,3): x = list(x)

            arr = numpy.array(x, dtype=typ)

            return cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=arr)
        #print(args_float, args_int, args_float4, args_int4)
        nargs_float  = m(args_float,0)
        nargs_int    = m(args_int,1)
        nargs_float4 = m(args_float4,2)
        nargs_int4   = m(args_int4,3)

        getattr(compiled_program, kernel_name)(self.queue, (output_width, output_height, output_depth), None, output_buf, nargs_float, nargs_int, nargs_float4, nargs_int4)
        cl.enqueue_read_buffer(self.queue, output_buf, output).wait()
        del output_buf
        return output
        
    @property
    def device(self):
        return self._device
    @device.setter
    def device(self, device):
        if self._device == device: return
        old = self._device
        del self.__context
        del self.__queue
        self._device = device
        self.__context = cl.Context([device],None,None)
        self.__queue = cl.CommandQueue(self.context)
        #fire event indicating code must be recompiled 
        self.on_code_dirty(self)
    
    @property
    def context(self): return self.__context
    @property
    def queue(self): return self.__queue
    
        
class FilterStack(object):
    def __init__(self, filter_runtime=None):
        self._list = []
        self._mark_dirty()
        self.runtime = filter_runtime
        self.__program = None
        self.width = 800
        self.height = 800
        self.depth = 1
        if not self.runtime: self.runtime = FilterRuntime()
        
    def _mark_dirty(self, *args):
        self._cached_sourcecode = None
        self._cached_bytecode = None
    
    @property
    def is_dirty(self):
        return self._cached_sourcecode == None
        
    def append(self,filter):
        filter.on_code_dirty += self._mark_dirty
        self._list.append(filter)
        self._mark_dirty()
        
    def pop(self):
        x = self._list.pop()
        x.on_code_dirty -= self._mark_dirty
        self._mark_dirty()
        
    push = append
    add = append
    
    def run(self, width=None, height=None, depth=None):
        if not width: width = self.width
        if not height: height = self.height
        if not depth: depth = self.depth
        if self.is_dirty or not self.__program:
            self.__program = self.runtime.compile(self.generate_code())
        args_float,args_int,args_float4,args_int4 = self.get_args_arrays()
        return self.runtime.run(self.__program, "ZeroToOneKernel", width, height, depth, args_float, args_int, args_float4, args_int4)
        
    def gen_image(self, width=None, height=None):
        output = self.run(width, height, 1)
        from PIL import Image
        output.shape = (width, height,4)
        im = Image.fromarray( (output*255).astype(numpy.ubyte) )
        return im
    
    def save_image(self, path, width=None, height=None):
        im = self.gen_image(width, height)
        im.save(path)
        del im
    
    def get_args_arrays(self):
        args_float = []
        args_int = []
        args_float4 = []
        args_int4 = []
        self._argsforfilter = {}
        
        for filter in self._list:
            self._argsforfilter[filter] = []
            
            # Handle args - get them from the filter
            args = []
            for k,v in filter.__class__.__dict__.iteritems():
                if isinstance(v,FilterArgument):
                    args.append(( v.index, v.type, getattr(filter,k) ))
                                
            # Sort args list so they're in the right order for insertion
            args.sort()
            
            # DO ERROR CHECKING ON ARGS LIST
            pass
            
            # Add arg values to arrays
            for idx,typ,val in args:
                if typ == ArgumentTypes.FLOAT:
                    self._argsforfilter[filter].append('args_float[{0}]'.format(len(args_float)))
                    args_float.append(val)
                elif typ == ArgumentTypes.INT:
                    self._argsforfilter[filter].append('args_int[{0}]'.format(len(args_int)))
                    args_int.append(val)
                elif typ == ArgumentTypes.FLOAT4:
                    self._argsforfilter[filter].append('args_float4[{0}]'.format(len(args_float4)))
                    args_float4.append(val)
                elif typ == ArgumentTypes.INT4:
                    self._argsforfilter[filter].append('args_int4[{0}]'.format(len(args_int4)))
                    args_int.append(val)
                else:
                    raise Exception("Invalid argment type {0}".format(typ))
                    
        return args_float,args_int,args_float4,args_int4

    def generate_code(self,force=False):
        if not self._cached_sourcecode:
            self._cached_sourcecode = ''
            self._cached_sourcecode += '// Start utility.cl\n'
            with open('utility.cl') as inp: self._cached_sourcecode += inp.read().strip() + '\n'
            self._cached_sourcecode += '// End utility.cl\n'
            
            kernel_main = []
            
            stack = []
            max_stack_size = -1
            
            self.get_args_arrays()
            
            for filterid,filter in enumerate(self._list):
                # Find unique ID for namespacing
                filterid = 'n{0}'.format(filterid)
                
                # Build code
                code = filter.generate_code() # Get the code for this filter
                code = code.replace('/*id*/',filterid) # Do namespacing
                self._cached_sourcecode += '\n' + code.strip() + '\n'                
                
                # Work out number and names of inputs (PointColors)
                inputs = []
                numinputs = filter.get_number_of_inputs()
                for i in xrange(numinputs): 
                    inputs.append(stack.pop())
                    
                # Work out name of output PointColor and push to stack
                ssize = len(stack)
                if ssize > max_stack_size:
                    max_stack_size = ssize
                output = 'o'+str(ssize)
                stack.append(output)
                
                # Pull inputs
                inputs += self._argsforfilter[filter]
                
                # Append to kernel main function
                kernel_main.append('{output} = {id}{name}({inputs});'.format(output=output,id=filterid,name=filter.get_name(),inputs=', '.join(inputs)))    
                
            if len(stack) != 1:
                raise Exception("Some items left on the stack.")
                
            self._cached_sourcecode += '''
__kernel void ZeroToOneKernel(__global float4 *output, __global float *args_float, __global int *args_int, __global float4 *args_float4, __global int4 *args_int4) {
    uint idX = get_global_id(0);
    uint idY = get_global_id(1);
    uint idZ = get_global_id(2);
    uint width = get_global_size(0);
    uint height = get_global_size(1);
    uint depth = get_global_size(2);

    uint arrIdx = idX + idY * width + idZ * width * height;
'''
            
            self._cached_sourcecode += "\n    PointColor "+', '.join(['o{0}'.format(i) for i in xrange(max_stack_size+1)])+';\n'
            self._cached_sourcecode += '\n'.join(['    '+str(k) for k in kernel_main]) + '\n\n';
            
            self._cached_sourcecode += '    output[arrIdx] = o0.color;\n}'
            
        return self._cached_sourcecode

##Sample code to get shit running
#from filterstack import *
#stack = FilterStack()
#stack.runtime.device = stack.runtime.get_devices()[1]
#from generators.checkerboard import CheckerBoard
#c = CheckerBoard()
#stack.push(c)
#stack.run()
