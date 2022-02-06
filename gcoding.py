#temp
from plopping import make_plopchart
from navigating import longstroke
from visualiser import visualize

gcode = ''
tile_size = 32

# determine experimentally
z_high = 10 
z_low = 9
# 

def move(x, y, contact=False):
	global gcode
	gcode += f'G{1 if contact else 0} X{x*tile_size} Y{y*tile_size}\n'
	if x > 22 or y > 22:
		print(f'!LARGE X/Y!: X:{x} Y:{y}')

def lift():
	global gcode
	gcode += f'G0 Z{z_high}\n'

def sink():
	global gcode
	gcode += f'G1 Z{z_low}\n'

def encode(moves, save=False):
	global gcode

	gcode = header
	
	pen_down = False
	for step in moves:
		print(step)
		if type(step) is tuple: # it's a displacement
			x, y = step
			move(x, y, pen_down)
		elif type(step) is str: # it's a non-displacement operation 
			match step:
				case 'pen up':
					pen_down = False
					lift()
				case 'pen down':
					pen_down = True
					sink()


	gcode += footer

	if type(save) is str:
		with open(save, 'w') as f:
			f.write(gcode)

	return gcode

header = """; I'm already Tracer
M140 S0 ; Bed temperature
M104 S0 ; Hotend temperature
M105 ; Report temperatures
M107 ; No fan
G92 E0 ; Reset Extruder
G28 ; Home all axes
G90 ; Set all axes to absolute
G0 F1000 ; Set movement speed

; Drawing
"""

footer = """
; Footer
M84 ; Disable all steppers
"""

if __name__ == '__main__':
	plopchart = make_plopchart('data/smile.png', save=False, show=False)
	moves = longstroke(plopchart)


	# width, height = plopchart.size
	# the result is saved in data/visualiser_out
	# visualize(moves, width, height, show=False)

	gcode = encode(moves, save='data/smile.gcode')
	print(gcode)