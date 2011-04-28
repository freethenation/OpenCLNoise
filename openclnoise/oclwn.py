#!/usr/bin/python
from filterstack import *
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
    help="width of image (default: %default)")
parser.add_option("-H", "--height",
    default=800, type=int, dest="height",
    help="height of image (default: %default)")
parser.add_option("-c", "--code",
    action="store", dest="savecode",
    help="save the generated kernel to this file")
parser.add_option("-s", "--scale",
    default=10, type=int, dest="scale",
    help="range from -scale/2 to scale/2 (default: %default)")
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
scale = options.scale

# build filter stack
fs = FilterStack(filter_runtime)

# Push clear and scale-trans filters
from clear import Clear
from scaletrans import ScaleTrans
clear = Clear()
scale = ScaleTrans(scale=(scale*width/height,scale,1,1), translate=(-scale/2.0*width/height,-scale/2.0,0,0))
fs.push(clear)
fs.push(scale)

# TESTING FILTERS HERE
from checkerboard import CheckerBoard
from blend import Blend, BlendMode
fs.push(CheckerBoard(black_color=(0.0,0.0,1.0,1.0), white_color=(1.0,1.0,1.0,1.0)))
fs.push(clear)
fs.push(scale)
fs.push(ScaleTrans(translate=(.5,.5,0,0)))
fs.push(CheckerBoard(black_color=(1.0,0.0,0.0,1.0), white_color=(1.0,0.0,0.0,0.5)))
fs.push(Blend(mode=BlendMode.ADD))
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
imagename = len(args) and args[0] or 'image.png'
print "Saving output to %dx%d image '%s'" % (width,height,imagename)
fs.save_image(imagename,width=width,height=height)

# Time
print "Last run took: %.2fms" % (fs.last_run_time*1000.0,)
