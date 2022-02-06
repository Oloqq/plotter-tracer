from plopping import make_plopchart
from navigating import longstroke
from visualiser import visualize

gcode = ''
tile_size = 32

# TODO lift the pen in gcode footer

class Gcoder:
	def __init__(self, settings: dict):
		self.code: str = ''
		self.tile_size: int = settings['tile_size']
		self.pen_down = False
		# determine experimentally
		self.z_high = 10 
		self.z_low = 9
		# 
		self.header = """; I'm already Tracer
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
		
		self.footer = """
; Footer
M84 ; Disable all steppers
"""

	def move(self, x, y):
		self.code += f'G{1 if self.pen_down else 0} X{x*self.tile_size} Y{y*self.tile_size}\n'
		if x > 22 or y > 22:
			print(f'!LARGE X/Y!: X:{x} Y:{y}')

	def lift(self):
		self.pen_down = False
		self.code += f'G0 Z{self.z_high}\n'

	def dive(self):
		self.pen_down = True
		self.code += f'G1 Z{self.z_low}\n'

	def encode(self, moves, save=False):
		self.code = self.header
		
		self.pen_down = False
		for step in moves:
			# print(step)
			if type(step) is tuple: # it's a displacement
				x, y = step
				self.move(x, y)
			elif type(step) is str: # it's a non-displacement operation 
				match step:
					case 'pen up':
						self.lift()
					case 'pen down':
						self.dive()

		self.code += self.footer

		if type(save) is str:
			with open(save, 'w') as f:
				f.write(gcode)

		return self.code

if __name__ == '__main__':
	plopchart = make_plopchart('data/smile.png', save=False, show=False)
	moves = longstroke(plopchart)

	# width, height = plopchart.size
	# the result is saved in data/visualiser_out
	# visualize(moves, width, height, show=False)
	settings = {
		'tile_size': 32
	}

	gcoder = Gcoder(settings)

	gcode = gcoder.encode(moves, save='data/smile.gcode')
	print(gcode)