from basefilter import *

class BlendMode:
    NORMAL='Normal'
    LIGHTEN='Lighten'
    DARKEN='Darken'
    MULTIPLY='Multiply'
    AVERAGE='Average'
    ADD='Add'
    SUBTRACT='Subtract'
    DIFFERENCE='Difference'
    NEGATION='Negation'
    SCREEN='Screen'
    EXCLUSION='Exclusion'
    OVERLAY='Overlay'
    SOFTLIGHT='SoftLight'
    HARDLIGHT='HardLight'
    COLORDODGE='ColorDodge'
    COLORBURN='ColorBurn'
    LINEARDODGE='LinearDodge'
    LINEARBURN='LinearBurn'
    LINEARLIGHT='LinearLight'
    VIVIDLIGHT='VividLight'
    PINLIGHT='PinLight'
    HARDMIX='HardMix'
    REFLECT='Reflect'
    GLOW='Glow'
    PHOENIX='Phoenix'


class Blend(BaseFilter):
    _filename = 'blend.cl'
    
    def __init__(self,mode=BlendMode.NORMAL):
        super(type(self),self).__init__()
        self.__mode = mode
    
    def get_number_of_inputs(self):
        return 2
    
    @property
    def mode(self):
        return self.__mode
    
    @mode.setter
    def mode(self,value):
        if self.__mode != value:
            self.__mode = value
            self.on_code_dirty(self)
    
    def generate_code(self):
        code = '#define /*id*/CHANNEL_BLEND_FUNC ChannelBlend_{0}\n'.format(self.__mode)
        code += super(type(self),self).generate_code()
        return code
        
    def get_name(self):
        return 'blend'
        
    def __repr__(self):
        return 'Blend(mode = "{0}")'.format(self.__mode)
