from turtle import Vec2D
from PIL import Image, ImageDraw
from navigating import longstroke
from datetime import datetime

# figure out the size of the visualisation from the moves

line_contact_color = (128, 255, 255, 180)
line_lifted_color = (255, 255, 128, 100)
gridline_color = (0, 0, 0)
bg_color = (87, 87, 87)

dot_size = 8
line_size = 10
tile_size = 50
pad = tile_size / 2
centering_vec = Vec2D(tile_size / 2, tile_size / 2)
grid = True

def convert(pos: Vec2D, translate=0):
	return list(pos * tile_size + Vec2D(translate, translate))

def circle_boundary(pos: Vec2D, radius):
	center = pos * tile_size + centering_vec
	return list(center - Vec2D(radius, 2*radius)) + list(center + Vec2D(radius, 2*radius))

def visualize(moves, width, height, show=False):
	img = Image.new('RGB',
		(width * tile_size, height * tile_size), color=bg_color)
	draw = ImageDraw.Draw(img, 'RGBA')

	outw = width * tile_size
	outh = height * tile_size

	if grid:
		for x in range(width):
			draw.line([x*tile_size, 0, x*tile_size, outh], fill=gridline_color, width=1)
		for y in range(height):
			draw.line([0, y*tile_size, outw, y*tile_size], fill=gridline_color, width=1)
		draw.line([outw-1, 0, outw-1, outh], fill=gridline_color, width=1)
		draw.line([0, outh-1, outw, outh-1], fill=gridline_color, width=1)
	
	pos = Vec2D(0, 0)
	pen_down = False
	for move in moves:
		# print(move)
		if type(move) is Vec2D: # it's a displacement
			color = line_contact_color if pen_down else line_lifted_color
			draw.line(convert(pos, pad) + convert(move, pad), fill=color, width=line_size)
			pos = move
		elif type(move) is str: # it's a non-displacement operation 
			match move:
				case 'pen up':
					pen_down = False
					draw.arc(circle_boundary(pos, dot_size), 180, 0, fill=(255, 0, 0), width=15)
				case 'pen down':
					pen_down = True
					draw.arc(circle_boundary(pos, dot_size), 0, 180, fill=(0, 255, 0), width=15)

	if show: img.show()
	now = datetime.now()
	img.save(f'data/visualiser_out/{now.strftime("%m-%d-%Y %H-%M-%S")}.png')


if __name__ == '__main__':
	width = 32
	height = 32
	img = Image.open('data/out.png')
	moves = longstroke(img)
	# print(moves)
	visualize(moves, width, height, show=True)