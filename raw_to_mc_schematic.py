#!/usr/bin/python
from nbt import *
import numpy
from openclnoise.vec import vec # Our own local copy! :)
import sys

with open('mc.raw') as inp:
    dims = numpy.empty((3,),dtype=numpy.uint64)
    dims.data = inp.read(24)
    data = numpy.empty((dims[0],dims[1],dims[2]),dtype=vec.float4)
    data.data = inp.read()

w = dims[0]
h = dims[1]
l = dims[2]

narr = numpy.empty((w,h,l),dtype=numpy.uint8)
for x in xrange(w):
    for y in xrange(h):
        for z in xrange(l):
            point = (data[x,y,z])[0]
            if point < 0.50:
                narr[x,y,z] = 1
            else:
                narr[x,y,z] = 0
    
s = TAG_Compound(name="Schematic")

s["Width"] = TAG_Short(w)
s["Length"] = TAG_Short(l)
s["Height"] = TAG_Short(h)

s["Materials"] = TAG_String("Alpha")

s["Blocks"] = TAG_Byte_Array()
s["Blocks"].value = narr

s["Blocks"].value.shape = (w,h,l)
s["Data"] = TAG_Byte_Array()
s["Data"].value = numpy.zeros(l*w*h, dtype=numpy.uint8)
s["Data"].value.shape = (w,h,l)
s["Entities"] = TAG_List()
s["TileEntities"] = TAG_List()

# Put wood at the bottom :)
s["Blocks"].value[0, :, :] = 5
    
s.save('woodystone.schematic')

