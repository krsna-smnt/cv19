
def normalize0_1(data_point, max_data_point, min_data_point):
	return (data_point - min_data_point) / (max_data_point - min_data_point)

def helper(st):
	if len(st) == 0:
		st += '00'
	elif len(st) == 1:
		st = '0' + st
	return st 

def rgb_vals(data_point):
	r = min(max(0, 1.5-abs(1-4*(data_point-0.5))),1)
	g = min(max(0, 1.5-abs(1-4*(data_point-0.25))),1)
	b = min(max(0, 1.5-abs(1-4*data_point)),1)

	R = hex(int(r*255)).lstrip("0x")
	G = hex(int(g*255)).lstrip("0x")
	B = hex(int(b*255)).lstrip("0x")



	return '#' + helper(R) + helper(G) + helper(B)


#if __name__ == "__main__":
#	print(rgb_vals(0.5))




