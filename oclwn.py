#!/usr/bin/python
from openclnoise import *
import optparse
import sys
import os

# Function to prompt for device selection
def askLongOptions(prompt,options):
    print("{0}:".format(prompt))
    for i,o in enumerate(options):
        print("\t{0}: {1}".format(i,o.name))
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

# Handle command line options
parser = optparse.OptionParser()
parser.add_option("-d", "--device", # Which device to use?
    action="store", type=int, dest="device", default=None,
    help="which compute device to use (starts at 0)")
parser.add_option("-W", "--width",
    default=800, type=int, dest="width",
    help="width of output file (default: %default)")
parser.add_option("-H", "--height",
    default=800, type=int, dest="height",
    help="height of output file (default: %default)")
parser.add_option("-D", "--depth",
    default=1, type=int, dest="depth",
    help="depth of output file (default: %default)")
parser.add_option("-c", "--code",
    action="store", dest="savecode",
    help="save the generated kernel to this file")
parser.add_option("-s", "--scale",
    default=10, type=float, dest="scale",
    help="range from -scale/2 to scale/2 (default: %default)")
parser.add_option("-l", "--load",
    default=None, type=str, dest="load_path",
    help="the path specifying location of saved filter stack file")
parser.add_option("-f","--file",
    default=None, type=str, dest="filename",
    help="write image to this filename")
parser.add_option("-r","--raw",
    default=False, action="store_true", dest="raw_mode",
    help="write raw data (see README for format)")
(options, args) = parser.parse_args()

# Select a device
filter_runtime = FilterRuntime()
devices = filter_runtime.get_devices()
if len(devices) == 0:
    raise Exception("No OpenCL devices found.")
elif options.device is not None:
    filter_runtime.device = devices[options.device]
elif len(devices) >= 1: 
    filter_runtime.device = askLongOptions("Which compute device to use",devices)
else:
    filter_runtime.device = devices[0]

# Define input parameters
width = options.width
height = options.height
depth = options.depth
scale = options.scale

# build filter stack
fs = FilterStack(filter_runtime=filter_runtime)

if options.load_path:
    fs.load(options.load_path)
else:
    # Push clear and scale-trans filters
    #from clear import Clear
    #from scaletrans import ScaleTrans
    #rom perlin import Perlin
    clear = Clear()
    scale = ScaleTrans(scale=(scale*width/height,scale,scale,1), translate=(500+-scale/2.0*width/height,500+-scale/2.0,0,0))
    fs.push(clear)
    fs.push(scale)

    # TESTING FILTERS HERE
    #from checkerboard import CheckerBoard
    #from perlin import Perlin
    #from blend import Blend, BlendMode
    #fs.push(CheckerBoard())
    fs.push(Worley(distance='manhattan'))
    fs.push(clear)
    fs.push(scale)
    fs.push(Perlin())
    fs.push(clear)
    fs.push(scale)
    fs.push(Worley())
    fs.push(Select())
    #~ fs.push(clear)
    #~ fs.push(scale)
    #~ fs.push(ScaleTrans(translate=(.5,.5,0,0)))
    #~ fs.push(CheckerBoard(black_color=(1.0,0.0,0.0,1.0), white_color=(1.0,0.0,0.0,0.5)))
    #~ fs.push(Blend(mode=BlendMode.ADD))
    # END TESTING FILTERS

print "Filters:"
for f in fs:
    print "\t%s" % (f,)

# Save code to file
if options.savecode:
    print "Saving kernel code to %s." % (options.savecode,)
    with open(options.savecode,'w') as out:
        out.write(fs.generate_code())

# Run!
if options.filename:
    if options.raw_mode: # Raw mode
        print "Saving output to %dx%dx%d raw file '%s'" % (width,height,depth,options.filename)
        fs.run_to_file(options.filename,width,height,depth)
    else: # Image mode
        print "Saving output to %dx%d image '%s'" % (width,height,options.filename)
        fs.save_image(options.filename,width,height)
else:
    print "Running and discarding output of %dx%dx%d data" % (width,height,depth)
    fs.run_to_discard(width,height,depth)

# Time
print "Last run took: %.2fms" % (fs.last_run_time*1000.0,)
