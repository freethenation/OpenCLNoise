#!/usr/bin/python
import pyopencl as cl
import optparse
import random
import numpy
import time
import math
import pdb

CPU_MAX_WIDTH = 532

def askLongOptions(prompt,options):
    print("{0}:".format(prompt))
    for i,o in enumerate(options):
        print("\t{0}: {1}".format(i,o))

    while 1:
        x = raw_input('? ')

        try:
            x = int(x)
        except ValueError:
            print("Error: choose a number between 0 and {0}.".format(len(options)))
            continue

        if x < 0 or x >= len(options):
            print("Error: choose a number between 0 and {0}.".format(len(options)))
            continue

        return options[x]

def roundUpToIncrements(inp,inc):
	if inp % inc == 0: return inp
	return inc * (int(inp/inc) + 1)

def getDevices():
	platforms = cl.get_platforms()
	assert len(platforms) >= 1, "No CL platforms found."
	if len(platforms) > 1:
		print "Warning: we have {0} platforms. Selecting the first one.".format(len(platforms))
	devices = platforms[0].get_devices()
	return devices

parser = optparse.OptionParser()
parser.add_option("-d", "--device",
                  action="store", type=int, dest="device", default=None,
                  help="which compute device to use (starts at 0)")
parser.add_option("-w", "--width",
                  default=132, type=int, dest="width",
                  help="width of matrix (default: %default)")
parser.add_option("-c", "--cpu",
                  default=False, action="store_true", dest="forcecpucompute",
                  help="force full CPU computation; otherwise, will only compute and check diagonal if width > %d" % (CPU_MAX_WIDTH,))
parser.add_option("-n", "--no-cpu",
                  default=True, action="store_false", dest="allowcpucompute",
                  help="prevent CPU computation")

(options, args) = parser.parse_args()

DESIRED_WIDTH = options.width
CPUCOMPUTE = (options.forcecpucompute or DESIRED_WIDTH < CPU_MAX_WIDTH) and options.allowcpucompute

devices = getDevices()
device = None
if options.device:
	if options.device < 0 or options.device >= len(devices):
		print "Invalid device selection: {0}.".format(options.device)
	else:
		device = devices[options.device]
		print "Selecting device {0}: {1}".format(options.device,device)
if len(devices) == 1:
	print "Selecting the first and only device."
	device = devices[0]
if not device:
	device = askLongOptions("Select a device",devices)


# Calculate optimal tile size
wgs = device.get_info(cl.device_info.MAX_WORK_GROUP_SIZE)
print "This device supports up to {0} work group threads.".format(wgs)
tile_size = 2 ** int(math.log(int(math.sqrt(wgs)))/math.log(2))
	
# Build arrays
#~ array1 = []
#~ array2 = []
#~ printTgts = DESIRED_WIDTH ** 2 / 128
#~ for i in xrange(DESIRED_WIDTH**2):
	#~ if i % printTgts == 0: print "Generated element %d of %d: %.2f%%" % (i+1,DESIRED_WIDTH**2,100.0*(i+1)/DESIRED_WIDTH**2)
	#~ array1.append(random.random() * 50)
	#~ array2.append(random.random() * 50)
print "Generating array 1: %d elements" % (DESIRED_WIDTH**2,)
array1 = numpy.random.normal(size=DESIRED_WIDTH**2)
print "Generating array 2: %d elements" % (DESIRED_WIDTH**2,)
array2 = numpy.random.normal(size=DESIRED_WIDTH**2)
assert len(array1) == len(array2)
width = int(math.sqrt(len(array1)))
assert width == DESIRED_WIDTH
lws = roundUpToIncrements(width,tile_size)

# Alert user
print "Working on a %d x %d matrix; tile size: %d; global work size: %d" % (width,width,tile_size,lws)

# Set up OpenCL
defines = {}
context = cl.Context([device],None,None)	
defines = ' '.join(['-D{0}{1}'.format(k,'='+str(v) if v else '') for (k,v) in defines.iteritems()])
with open('ker.cl', 'r') as kernelFile: kernel = kernelFile.read()
worker = cl.Program(context, kernel).build(defines)
queue = cl.CommandQueue(context)

# Prepare buffers
t = time.time()
arr1_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=array1.astype(numpy.float32))
arr2_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=array2.astype(numpy.float32))

output = numpy.zeros(width*width,numpy.float32)
output_buf = cl.Buffer(context, cl.mem_flags.WRITE_ONLY | cl.mem_flags.USE_HOST_PTR, hostbuf=output)

# Start compute
worker.matmult(queue, (lws,lws), (tile_size,tile_size), 
	arr1_buf, arr2_buf, output_buf, numpy.int32(width))

# Read output buffer back to host
cl.enqueue_read_buffer(queue, output_buf, output).wait()
gputime = time.time() - t
print "gpu time: {0:8.2f}ms".format(gputime * 1000)

#print "array",array1
#print "gpu product:", list(output)
if not CPUCOMPUTE:
	print "Only the diagonal will be computed and checked on the CPU to save time"
t = time.time()
noutput = []
for i in xrange(width):
	for j in xrange(width):
		noutput.append(0.0)
		if CPUCOMPUTE or j == i: # Either we can reasonably check it all, or we should just compute the diagonal
			for x in xrange(width):
				noutput[i * width + j] += array1[i * width + x] * array2[x * width + j]
cputime = time.time() - t
print "cpu time{1}: {0:8.2f}ms".format(cputime * 1000, ' (LIES!)' if not CPUCOMPUTE else '')
print "speedup: {0:.2f}".format(cputime/gputime)
#print "cpu product:", noutput

for i,a in enumerate( zip(noutput,list(output)) ):
	cpu,gpu = a
	if CPUCOMPUTE or i % width == i / width:
		if abs(cpu - gpu) > 0.10:
			print "Warning: %.3f CPU != %.3f GPU @ %d" % (cpu,gpu,i)

