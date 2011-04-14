#!/usr/bin/python
import pyopencl as cl
import optparse
import random
import numpy
import time
import math
import sys

# Types to use
VALUE_TYPE = numpy.ubyte
INDEX_TYPE = numpy.uint64

# Params for the random function
MEAN = 0
STD_DEV = 1

# Margin of error to use when comparing results to cpu calculations
FLOATING_POINT_MARGIN_OF_ERROR = 0.001

# Function to prompt for device selection
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

# Used to round the global work size up to a tile boundary
# e.g. roundUpToIncrements(30,16) = 32
def roundUpToIncrements(inp,inc):
    if inp % inc == 0: return inp
    return inc * (int(inp/inc) + 1)

# Find a list of platforms on the machine, then return a list of the first platform's devices
def getDevices():
    platforms = cl.get_platforms()
    assert len(platforms) >= 1, "No CL platforms found."
    if len(platforms) > 1:
	print "Warning: we have {0} platforms. Selecting the first (zeroth) one.".format(len(platforms))
    devices = platforms[0].get_devices()
    return devices

# Handle command line options
parser = optparse.OptionParser()
parser.add_option("-d", "--device", # Which device to use?
    action="store", type=int, dest="device", default=None,
    help="which compute device to use (starts at 0)")
parser.add_option("-l", "--length",
    default=2**16+1, type=int, dest="length",
    help="length of array (default: %default)")
parser.add_option("-n", "--no-cpu",
    default=True, action="store_false", dest="allowcpucompute",
    help="prevent CPU computation")
(options, args) = parser.parse_args()

if options.length > 2 ** 28:
	raise MemoryError("We can't allocate an array that big.")

# Select a device
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
    
# Find size of local memory:
# device.get_info(cl.device_info.LOCAL_MEM_SIZE)
    
# LAB-SPECIFIC CODE AFTER THIS

# Build array to sum
#print "Using Gaussian distribution with mean of %.2f and S.D. of %.2f" % (MEAN,STD_DEV)
print "Generating array:",
sys.stdout.flush()
array = numpy.arange(0,options.length).astype(VALUE_TYPE)
#array = numpy.random.normal(loc=MEAN, scale=STD_DEV, size=(options.length,)).astype(VALUE_TYPE)
print array.shape[0], 'elements.'

#~ # Calculate optimal tile size -- largest power of two less than sqrt of max work group size
#~ maxwgs = device.get_info(cl.device_info.MAX_WORK_GROUP_SIZE)
#~ print "This device supports up to {0} threads per work group.".format(maxwgs)
#~ tile_size = 2 ** int(math.log(int(math.sqrt(maxwgs)))/math.log(2))
	
#~ # Build matricies
#~ print
#~ print "Using Gaussian distribution with mean of %.2f and S.D. of %.2f" % (MEAN,STD_DEV)
#~ print "Generating matrix 1:",
#~ matrix1 = numpy.random.normal(loc=MEAN, scale=STD_DEV, size=(width,width))
#~ print matrix1.shape
#~ print "Generating matrix 2:",
#~ matrix2 = numpy.random.normal(loc=MEAN, scale=STD_DEV, size=(width,width))
#~ print matrix2.shape
#~ print
#~ 
#~ # Global work size - number of threads to run in total
#~ global_work_size = roundUpToIncrements(width,tile_size)

#~ print "Working on two %d x %d matrix; tile size: %d; global work size: %d" % (width,width,tile_size,global_work_size)

# Set up OpenCL
context = cl.Context([device],None,None) # Create a context
kernel = '''
#pragma OPENCL EXTENSION cl_khr_byte_addressable_store : enable
__kernel void sumreduce(__global uchar *arr, const ulong stride) {
    ulong idx = get_global_id(0) * stride;
    if(idx > get_global_size(0) || idx + stride/2 > get_global_size(0))
	return;
    arr[idx] += arr[idx+stride/2];
} '''

# Build a Program object -- kernel is compiled here, too. Can be cached for more responsiveness.
worker = cl.Program(context, kernel).build()
queue = cl.CommandQueue(context)

# Prepare sum buffer
t = time.time() # Start timing the GL code
buf = cl.Buffer(context, cl.mem_flags.USE_HOST_PTR, hostbuf=array)

# Do compute -- loop over all possible "stride" values, powers of two starting at 2 and going to width/2
for i in xrange(1,int(math.log(options.length)/math.log(2))+1):
	stride = 2 ** i
	#print "Doing calculation for stride 2**%d: %d" % (i,stride)
	worker.sumreduce(queue, (options.length,), None, buf, INDEX_TYPE(stride)).wait()	

# Allocate output "array" -- only need first cell
output = numpy.array((1,),dtype=VALUE_TYPE)

# Read output buffer back to host -- block here
cl.enqueue_read_buffer(queue, buf, output).wait()

gpu = output[0]
print "sum(array) == %f" % (gpu,)

# Compute the GPU time
gputime = time.time() - t
print "gpu time: {0:8.2f}ms".format(gputime * 1000)

if options.allowcpucompute:
    print "\nComputing on CPU"
    # Begin timing the CPU code
    t = time.time() 
    
	# Do the sum
    cpu = sum(array)
    print "sum(array) == %f" % (cpu,)
    
    # Compute the CPU time and speedup from GPU
    cputime = time.time() - t
    print "cpu time: {0:8.2f}ms".format(cputime * 1000)
    print "speedup: {0:.2f}".format(cputime/gputime)

    # Check for errors
    failed = False
    if abs(cpu - gpu) > FLOATING_POINT_MARGIN_OF_ERROR:
	    failed = True
	    print "Warning: %.3f CPU != %.3f GPU" % (cpu,gpu)
    if not failed:
		print "All tests passed! Answers agree within {0}.".format(FLOATING_POINT_MARGIN_OF_ERROR)
else:
    print "Not computing the sum on the CPU."

