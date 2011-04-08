#!/usr/bin/python
import pyopencl as cl
import optparse
import random
import struct
import numpy
import time
import math
import sys
import os

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
#~ parser.add_option("-w", "--height",
    #~ default=132, type=int, dest="height",
    #~ help="height of matrix (default: %default)")
#~ parser.add_option("-n", "--no-cpu",
    #~ default=True, action="store_false", dest="allowcpucompute",
    #~ help="prevent CPU computation")
(options, args) = parser.parse_args()
#height = options.height

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

# Calculate optimal tile size -- largest power of two less than sqrt of max work group size
maxwgs = device.get_info(cl.device_info.MAX_WORK_GROUP_SIZE)
print "This device supports up to {0} threads per work group.".format(maxwgs)

# Create input array
width = 1920
height = 1080
arr = []
for x in xrange(height):
    for y in xrange(width):
        arr.append((x/50.0,y/50.0,0,0))
input_array = numpy.array(arr,dtype=numpy.float32)

print "Working on {0} element array.".format(len(input_array))

# Global work size - number of threads to run in total
#global_work_size = roundUpToIncrements(height,tile_size)

# Set up OpenCL
context = cl.Context([device],None,None) # Create a context
with open('ker.cl','r') as inp:
    kernel = inp.read()

# Build a Program object -- kernel is compiled here, too. Can be cached for more responsiveness.
worker = cl.Program(context, kernel).build()
queue = cl.CommandQueue(context)

# Prepare input buffers
t = time.time() # Start timing the GL code
input_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=input_array)

# Allocate space for output buffer
output = numpy.zeros((len(input_array),4),numpy.float32)
output_buf = cl.Buffer(context, cl.mem_flags.WRITE_ONLY | cl.mem_flags.USE_HOST_PTR, hostbuf=output)

# Start compute - call the matmult kernel function using command queue queue, 2d global work size as given, and 2d local work size as given
# Returns immediately -- we block at the enqueue_read_buffer
worker.WorleyNoise(queue, (len(input_array),), None, input_buf, output_buf)

# Read output buffer back to host 
cl.enqueue_read_buffer(queue, output_buf, output).wait()

# Compute the GPU time
gputime = time.time() - t
print "gpu time: {0:8.2f}ms".format(gputime * 1000)

# Write image using PIL
from PIL import Image
output.shape = (height,width,4)
im = Image.fromarray( (output*255).astype(numpy.ubyte) )
fn = '{0}.png'.format(os.environ.get('USER','unknown'))
im.save(fn)
print "Saved image to {0}".format(fn)
