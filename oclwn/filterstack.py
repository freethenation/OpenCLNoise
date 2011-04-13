#!/usr/bin/python
from basefilter import FilterArgument,ArgumentTypes
import time

class FilterStack(object):
	def __init__(self):
		self._list = []
		self._mark_dirty()
		
	def _mark_dirty(self):
		self._cached_sourcecode = None
		self._cached_bytecode = None
		
	def append(self,filter):
		filter.on_dirty += self.mark_dirty
		self._list.append(filter)
		self._mark_dirty()
		
	def pop(self):
		x = self._list.pop()
		x.on_dirty -= self.mark_dirty
		self._mark_dirty()
		
	push = append
	add = append
	
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

    PointColor v;
    v.point.x = (float)idX/width;
    v.point.y = (float)idY/height;
    v.point.z = (float)idZ/depth;
'''
			
			self._cached_sourcecode += "\n    PointColor "+', '.join(['o{0}'.format(i) for i in xrange(max_stack_size+1)])+';\n'
			self._cached_sourcecode += '\n'.join(['    '+str(k) for k in kernel_main]) + '\n\n';
			
			self._cached_sourcecode += '    output[arrIdx] = o0.color;\n}'
			
		return self._cached_sourcecode

