#!/usr/bin/python
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
			stack = []
			max_stack_size = -1
			kernel_main = []
			for filterid,filter in enumerate(self._list):
				#code = filter.generate_code() # Get the code for this filter
				#code = code.replace('/*id*/','I{0}'.format(filterid)) # Do namespacing
				
				# Work out input variables
				inputs = []
				numinputs = filter.get_number_of_inputs()
				for i in xrange(numinputs): 
					inputs.append(stack.pop())
					
				# Work out name of output variable
				ssize = len(stack)
				if ssize > max_stack_size:
					max_stack_size = ssize
				output = 'o'+str(ssize)
				stack.append(output)
					
				# Append to kernel
				kernel_main.append('{output} = I{id}{name}({inputs});'.format(output=output,id=filterid,name=filter.get_name(),inputs=','.join(inputs)))	
				
			if len(stack) > 0:
				raise Exception("Some items left on the stack.")
			kernel = "PointColor "+', '.join(['o{0}'.format(i) for i in xrange(max_stack_size+1)])+';\n'
			kernel += '\n'.join(kernel_main)
			
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
	fs.generate_code()
