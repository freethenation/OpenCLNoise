#!/usr/bin/python
from BaseFilter import FilterArgument,ArgumentTypes

class FilterStack(object):
	def __init__(self):
		self._list = []
		self._mark_dirty()
		
	def _mark_dirty(self):
		self._cached_sourcecode = None
		self._cached_bytecode = None
		
	def append(self,filter):
		#filter.on_dirty += self.mark_dirty
		self._list.append(filter)
		self._mark_dirty()
		
	def pop(self):
		x = self._list.pop()
		#x.on_dirty -= self.mark_dirty
		self._mark_dirty()
		
	push = append
	add = append
	
	def generate_code(self,force=False):
		if not self._cached_sourcecode:
			kernel_main = []
			
			stack = []
			max_stack_size = -1
			
			args_float = []
			args_int = []
			args_float4 = []
			args_int4 = []
			
			for filterid,filter in enumerate(self._list):
				# Find unique ID for namespacing
				filterid = 'n{0}'.format(filterid)
				
				# Build code
				code = filter.generate_code() # Get the code for this filter
				code = code.replace('/*id*/',filterid) # Do namespacing
				
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
				for arr in args:
					idx,typ,val = arr
					if typ == ArgumentTypes.FLOAT:
						inputs.append('args_float[{0}]'.format(len(args_float)))
						args_float.append(val)
					elif typ == ArgumentTypes.INT:
						inputs.append('args_int[{0}]'.format(len(args_int)))
						args_int.append(val)
					elif typ == ArgumentTypes.FLOAT4:
						inputs.append('args_float4[{0}]'.format(len(args_float4)))
						args_float4.append(val)
					elif typ == ArgumentTypes.INT4:
						inputs.append('args_int4[{0}]'.format(len(args_int4)))
						args_int.append(val)
					else:
						raise Exception("Invalid argment type {0}".format(typ))
				
				# Append to kernel main function
				kernel_main.append('{output} = {id}{name}({inputs});'.format(output=output,id=filterid,name=filter.get_name(),inputs=', '.join(inputs)))	
				
			if len(stack) > 0:
				raise Exception("Some items left on the stack.")
			kernel = "PointColor "+', '.join(['o{0}'.format(i) for i in xrange(max_stack_size+1)])+';\n'
			kernel += '\n'.join(kernel_main)
			print kernel
			
		return self._cached_sourcecode
		
class BFilter(object):
	def __init__(self,name,numinputs):
		self.name = name
		self.numinputs = numinputs
	
	def get_name(self):
		return self.name
		
	def get_number_of_inputs(self):
		return self.numinputs

if __name__ == '__main__':
	fs = FilterStack()
	fs.add(BFilter('filter_black',0))
	fs.add(BFilter('filter_scale',1))
	fs.add(BFilter('filter_worley',1))
	#fs.add(BFilter('filter_black',0))
	#fs.add(BFilter('filter_scale',1))
	#fs.add(BFilter('filter_worley',1))
	#fs.add(BFilter('filter_blend',2))
	print fs.generate_code()
