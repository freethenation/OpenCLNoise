class FilterLut(class):
    def __init__(self):
        self.table = []
    def add(self, value, color):
        self.table.append((value, color))
    def clear(self):
	self.table = []
    def generate_code():
	table.sort()
	output += """PointColor filter_lut(PointColor input) {
		FLOAT_T avg = input.point.x + input.point.y + input.point.z;"""
	for i, item in enumerate(table):
		if i==0: continue
		value, color = item
		output += "if(avg<{0})  ;".format(value)
