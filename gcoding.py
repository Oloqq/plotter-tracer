#temp
from plopping import make_plopchart
from navigating import navigate
from visualiser import visualize

def encode(moves, save=False):
	gcode = header()
	gcode += 'bruh'
	gcode += footer()

	if type(save) is str:
		with open(save, 'w') as f:
			f.write(gcode)

	return gcode

def header():
	return """; I'm already Tracer
M140 S0 ; Bed temperature
M104 S0 ; Hotend temperature
M105 ; Report temperatures
M107 ; No fan
G92 E0 ; Reset Extruder
G1 F2700 E-5 ; Retract filament
G28 ; Home all axes
G0 F100 ; Set movement speed
"""

def footer():
	return """
M84 ; Disable all steppers
"""

if __name__ == '__main__':
	plopchart = make_plopchart('data/smile.png', save=False, show=False)
	moves = navigate(plopchart)

	width, height = plopchart.size
	# the result is saved in data/visualiser_out
	visualize(moves, width, height, show=False)

	gcode = encode(moves, save='data/smile.gcode')
	print(gcode)