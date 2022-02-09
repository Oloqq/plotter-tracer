from turtle import Vec2D
from plopping import make_plopchart
from navigating import closing_circles, longstroke, squiggler
from logger import log
from datetime import datetime
from visualiser import visualize

# TODO flip the image in Y

class Gcoder:
	def __init__(self, settings: dict):
		self.code: str = ''
		self.tile_size: int = settings['tile_size']
		self.pen_down = False
		self.z_high = settings['z_high']
		self.z_low = settings['z_low']
		self.min_x = settings['x'][0]
		self.max_x = settings['x'][1]
		self.min_y = settings['y'][0]
		self.max_y = settings['y'][1]
		self.vertical_force = settings['vertical_move_force']
		self.horizontal_force = settings['horizontal_move_force']

		self.header = f"""; I'm already Tracer {datetime.now().strftime('%d.%m.%Y %H-%M-%S')}
M140 S0 ; Bed temperature
M104 S0 ; Hotend temperature
M105 ; Report temperatures
M107 ; No fan
G92 E0 ; Reset Extruder
G28 ; Home all axes
G90 ; Set all axes to absolute
G0 F{self.vertical_force} Z{self.z_high} ; Lift the pen

; Drawing
"""
		
		self.footer = """
; Footer
G0 Z20 ; Lift the pen
M84 ; Disable all steppers
"""

	def move(self, x, y):
		out_x = x * self.tile_size + self.min_x
		out_y = y * self.tile_size + self.min_y
		self.code += f'G{1 if self.pen_down else 0} F{self.horizontal_force} X{out_x} Y{out_y}\n'

		if out_x > self.max_x or out_y > self.max_y:
			log(f'! TOO LARGE X/Y !: X:{x}->{out_x} Y:{y}->{out_y}', console=True)
			log(f'! TOO LARGE X/Y !: max X:{self.max_x} max Y:{self.max_y}', console=True)

	def lift(self):
		self.pen_down = False
		self.code += f'G0 F{self.vertical_force} Z{self.z_high}\n'

	def dive(self):
		self.pen_down = True
		self.code += f'G1 F{self.vertical_force} Z{self.z_low}\n'

	def encode(self, moves, save=False):
		self.code = self.header
		
		self.pen_down = False
		for step in moves:
			if type(step) is Vec2D: # it's a displacement
				x, y = list(step)
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
	plopchart = make_plopchart('data/mak.png', save=False, show=False)
	moves = closing_circles(plopchart)

	width, height = plopchart.size
	# the result is saved in data/visualiser_out
	visualize(moves, width, height, show=False)

	# coords scopes
	# X: 0 - 200
	# Y: 75 - 220 
	# Z: 0 - draw [5,10] - lifted
	settings = {
		'tile_size': 0.39,
		'z_high': 19,
		'z_low': 14,
		'x': (0, 200),
		'y': (75, 220),
		'horizontal_move_force': 1000,
		'vertical_move_force': 100
	}

	gcoder = Gcoder(settings)

	gcode = gcoder.encode(moves, save='data/mak.gcode')
	# print(gcode)