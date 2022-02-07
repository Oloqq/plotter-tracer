from plopping import make_plopchart
from navigating import longstroke
from visualiser import visualize

# coords scopes
# X: 0 - 200
# Y: 75 - 220 
# Z: 0 - draw [5,10] - lifted

class Gcoder:
	def __init__(self, settings: dict):
		self.code: str = ''
		self.tile_size: int = settings['tile_size']
		self.pen_down = False
		self.z_high = settings['z_high']
		self.z_low = settings['z_low']
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
G0 Z20 ; Lift the pen
M84 ; Disable all steppers
"""

	def move(self, x, y):
		self.code += f'G{1 if self.pen_down else 0} X{x*self.tile_size+50} Y{y*self.tile_size+100}\n'
		if x*self.tile_size > 220 or y*self.tile_size > 220:
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
				f.write(self.code)

		return self.code

if __name__ == '__main__':
	plopchart = make_plopchart('data/smile.png', save=False, show=False)
	moves = longstroke(plopchart)

	# width, height = plopchart.size
	# the result is saved in data/visualiser_out
	# visualize(moves, width, height, show=False)
	settings = {
		'tile_size': 4,
		'z_high': 5,
		'z_low': 0
	}

	gcoder = Gcoder(settings)

	gcode = gcoder.encode(moves, save='data/smile.gcode')
	# print(gcode)