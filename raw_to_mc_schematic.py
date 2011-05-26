#!/usr/bin/python
from nbt import *
import numpy
from openclnoise.vec import vec # Our own local copy! :)
import sys,os

if len(sys.argv) < 3:
    print "Usage: raw_to_mc_schematic.py <input.raw> <output.schematic>"
    sys.exit(1)
    
inf = sys.argv[1]
if not os.path.exists(inf):
    print "Can't find",inf
    sys.exit(1)

size = os.stat(inf).st_size

print "Reading",inf
with open(inf) as inp:
    dims = numpy.empty((3,),dtype=numpy.uint64)
    dims.data = inp.read(24)
    w,h,d = dims
    
    elmsize = (size - 24) / (w*h*d)
    datatype = vec.float4 if (elmsize == 4*4) else vec.uchar4
    
    print "Found block {0} x {1} x {2}, size {3} bytes ({4}b / elm)".format(w,h,d,size,elmsize)
    data = numpy.empty((dims[0],dims[1],dims[2]),dtype=datatype)
    data.data = inp.read()

print data

comp = 0.50
if datatype == vec.float4:
    print "Data is in float4s, comparing to {0}".format(comp)
else:
    comp = 255 * comp
#    dirtlower = 0.47
#    dirtupper = 0.50
    print "Data is in byte4s, comparing to {0}".format(comp)

#print data

w,h,d = dims
narr = numpy.empty(w*h*d,dtype=numpy.uint8)
for x in xrange(w):
    for y in xrange(h):
        for z in xrange(d):
            mcd = y + z * h + x * d * h
            point = (data[x,y,z])[0]
            if point > comp:
                narr[mcd] = 1
                alpha = (data[x,y,z])[3]
                if abs(alpha - 128) <= 8:
                    narr[mcd] = 3
            else:
                narr[mcd] = 0 # Insert air
        
s = TAG_Compound(name="Schematic")

s["Width"] = TAG_Short(w)
s["Length"] = TAG_Short(d)
s["Height"] = TAG_Short(h)

s["Materials"] = TAG_String("Alpha")

s["Blocks"] = TAG_Byte_Array()
s["Blocks"].value = narr
#s["Blocks"].value.shape = (w,d,h)

s["Data"] = TAG_Byte_Array()
s["Data"].value = numpy.zeros(w*d*h, dtype=numpy.uint8)
#s["Data"].value.shape = (w,d,h)
s["Entities"] = TAG_List()
s["TileEntities"] = TAG_List()

# Put wood at the bottom :)
#s["Blocks"].value[0, :, :] = 5
    
outf = sys.argv[2]
print "Writing",outf
s.save(outf)

