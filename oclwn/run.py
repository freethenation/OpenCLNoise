from filterstack import *
stack = FilterStack()
stack.runtime.device = stack.runtime.get_devices()[1]
from generators.checkerboard import CheckerBoard
from generators.clear import Clear
from transforms.scaletrans import ScaleTrans
from selectors.select import Select
from generators.worley import Worley
#from modifiers.lut import Lut
from combiners.blend import Blend
#filter 1
stack.push(Clear())
stack.push(ScaleTrans((10.0,10.0,10.0,10.0)))
stack.push(CheckerBoard((0.0,1,0.0,0.5)))
stack.push(Clear())
stack.push(ScaleTrans((10.0,10.0,10.0,10.0)))
stack.push(Worley())
stack.push(Blend())

#check = CheckerBoard()
#stack.push(check)
##filter 2
#clear = Clear()
#stack.push(clear)
#scale = ScaleTrans((10.0,10.0,10.0,10.0))
#stack.push(scale)
#check = CheckerBoard((1.0,0.5,1.0,1.0),(0.0,0.5,0.0,1.0))
#stack.push(check)
##filter 3
#clear = Clear()
#stack.push(clear)
#scale = ScaleTrans((10.0,10.0,10.0,10.0))
#stack.push(scale)
#check = CheckerBoard()
#stack.push(check)
#select = Select()
#stack.push(select)

try:
    stack.save_image("freethenation.png",1024,1024)
except Exception: raise
finally:
    f = open("code.txt","w")
    f.write(stack.generate_code())
    f.close()
    