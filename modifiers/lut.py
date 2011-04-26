from basefilter import *

class Lut(BaseFilter):
    def __init__(self):
        BaseFilter.__init__(self)
        self.table = {}
    
    def get_name(self):
        return "lut"
    
    def get_number_of_inputs(self):
        return 1
    
    def generate_code(self):
        template = """
        PointColor /*id*/lut(PointColor input) {
            float4 avg = (input.color.x+input.color.y+input.color.z)/3.0f;
            if(false){}
            CODE_HERE
            return input;
        }
        """
        lutCode = ""
        table = self.table.items().sort()
                
        for i, rec in enumerate(self.table.items().sort()[1:-1]):
            
            
        #START {0}
        #END {1}
        #A {2}
        #B {3}
        lutCode += "else if(avg < {1}){return lerp((float4){2},(float4){3},({0} - avg)/({0} - {1}));}".replace()
        
