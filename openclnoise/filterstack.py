from basefilter import FilterArgument, ArgumentTypes, BaseFilter
import time
import logging as log
import pyopencl as cl
try:
    from pyopencl.array import vec
except ImportError:
    from vec import vec # Our own local copy! :)
from event import Event
import numpy
import math

class FilterRuntime(object):
    def __init__(self,device=None):
        self.on_code_dirty = Event()

        self.__context = None
        self.__queue = None

        self._device = None
        if isinstance(device,int):
            self.device = self.get_devices()[device]
        elif not device: 
            devices = self.get_devices()
            self.device = devices[0]
        else:
            self.device = device
    
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

        # Handle arguments
        nargs_float  = m(args_float,  0)
        nargs_int    = m(args_int,    1)
        nargs_float4 = m(args_float4, 2)
        nargs_int4   = m(args_int4,   3)

        # Determine total number of chunks
        chunk_width = min(512,output_width)
        chunk_height = min(512,output_height)
        chunk_depth = min(16,output_depth)
        total_chunks = (int(math.ceil(output_width/float(chunk_width))),int(math.ceil(output_height/float(chunk_height))),int(math.ceil(output_depth/float(chunk_depth))))
        
        # Allocate final output array, per-chunk array, and output buffer
        final_output = numpy.empty((output_width,output_height,output_depth),vec.float4)
        chunk_output = numpy.empty((chunk_width,chunk_height,chunk_depth),vec.float4)
        output_buf = cl.Buffer(self.context, cl.mem_flags.WRITE_ONLY | cl.mem_flags.USE_HOST_PTR, hostbuf=chunk_output)

        # Get kernel and run
        kernel = getattr(compiled_program, kernel_name)
        for x in xrange(total_chunks[0]):
            for y in xrange(total_chunks[1]):
                for z in xrange(total_chunks[2]):
                    current_chunk = (x,y,z,0)

                    # Run and read from GPU
                    kernel(self.queue, (chunk_width, chunk_height, chunk_depth), None, 
                           vec.make_int4(*total_chunks), vec.make_int4(*current_chunk), 
                           output_buf, 
                           nargs_float, nargs_int, nargs_float4, nargs_int4)
                    cl.enqueue_read_buffer(self.queue, output_buf, chunk_output).wait()
                    
                    return chunk_output
#                    yield current_chunk[:3], chunk_output

#        del output_buf
#        del chunk_output
#        return final_output
        
    @property
    def device(self):
        return self._device
    @device.setter
    def device(self, device):
        if self._device == device: return
        log.warn("Using OpenCL device '{0}'.".format(device.name))
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
    def __init__(self, filters=None, filter_runtime=None):
        self._list = []
        self._mark_dirty()
        self.runtime = filter_runtime
        self.__program = None
        self.width = 800
        self.height = 800
        self.depth = 1
        if not self.runtime: self.runtime = FilterRuntime()
        if filters: self.append(filters)
        
    def _mark_dirty(self, *args):
        self._cached_sourcecode = None
        self._cached_bytecode = None
    
    @property
    def is_dirty(self):
        return self._cached_sourcecode == None
        
    def append(self,filter):
        try:
            for f in filter:
                if not isinstance(f, BaseFilter): raise Exception()
            for f in filter:
                self._list.append(f)
                f.on_code_dirty += self._mark_dirty
        except:
            if not isinstance(filter, BaseFilter): 
                raise Exception("Cannot add filter which does not inherit from BaseFilter")
            self._list.append(filter)
            filter.on_code_dirty += self._mark_dirty
        self._mark_dirty()
        
    def pop(self):
        self._mark_dirty()
        x = self._list.pop()
        x.on_code_dirty -= self._mark_dirty
        
    def insert(self, index, filter):
        try:
            for f in filter:
                if not isinstance(f, BaseFilter): raise Exception()
            for i,f in enumerate(filter):
                self._list.insert(index+i, f)
                f.on_code_dirty += self._mark_dirty
        except:
            if not isinstance(filter, BaseFilter): 
                raise Exception("Cannot add filter which does not inherit from BaseFilter")
            self._list.insert(index, filter)
            filter.on_code_dirty += self._mark_dirty
        self._mark_dirty()
        
    push = append
    add = append
    def clear(self):
        self._mark_dirty()
        del self._list
        self._list = []
        
    def __setitem__(self, key,value): 
        self._mark_dirty()
        x = self._list[key]
        x.on_code_dirty -= self._mark_dirty
        value.on_code_dirty += self._mark_dirty
        self._list[key] = value        
    def __delitem__(self, key):
        self._mark_dirty()
        x = self._list[key]
        x.on_code_dirty -= self._mark_dirty
        return self._list.__delitem__[key]
    def __getitem__(self, key): return self._list[key]
    def __iter__(self): return self._list.__iter__()
    def __repr__(self):
        ret = "FilterStack(["
        ret += ", ".join([repr(f) for f in self]) 
        return ret + "])"
        
    def save(self, file):
        if isinstance(file,basestring): 
            f = open(file, "w")
            f.write(repr(self))
            f.close()
        else: file.write(repr(self))
    
    def load(self, file):
        if isinstance(file,basestring):
            file = open(file, "r")
            code = file.read()
            file.close()
        else: code = file.read()
        self.clear()
        self.append(eval(code, __import__("openclnoise").__dict__))
    
    def run(self, width=None, height=None, depth=None):
        if not width: width = self.width
        if not height: height = self.height
        if not depth: depth = self.depth
        if self.is_dirty or not self.__program:
            self.__program = self.runtime.compile(self.generate_code())
        args_float,args_int,args_float4,args_int4 = self.get_args_arrays()
        stime = time.time()
        ret = self.runtime.run(self.__program, "ZeroToOneKernel", width, height, depth, args_float, args_int, args_float4, args_int4)
        self.__last_run_time = time.time() - stime
        return ret
        
    @property
    def last_run_time(self):
        return self.__last_run_time
        
    def gen_image(self, width=None, height=None):
        output = self.run(width, height, 1)[:,:,0] # 2-d output
        from PIL import Image

        output = numpy.ndarray(shape=(width,height,4),buffer=output.data,dtype=numpy.float32)

        im = Image.fromarray((output*255).astype(numpy.ubyte))
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
__kernel void ZeroToOneKernel(int4 totalChunks, int4 currentChunk, __global float4 *output, __global float *args_float, __global int *args_int, __global float4 *args_float4, __global int4 *args_int4) {
    uint idX = get_global_id(0);
    uint idY = get_global_id(1);
    uint idZ = get_global_id(2);
    uint width = get_global_size(0);
    uint height = get_global_size(1);
    uint depth = get_global_size(2);

    uint arrIdx = idX + idY * width + idZ * width * height;
'''
            
            self._cached_sourcecode += "\n    PointColor "+', '.join(['o{0}'.format(i) for i in xrange(max_stack_size+1)])+';\n'
            self._cached_sourcecode += ('\n'.join(['    '+str(k) for k in kernel_main]) + '\n\n').replace('clear()','clear(totalChunks,currentChunk)');
            
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
