from PIL import Image, ImageDraw
from navigating import navigate

line_contact_color = (128, 255, 255, 180)
line_lifted_color = (255, 255, 128, 100)
gridline_color = (0, 0, 0)
bg_color = (87, 87, 87)

dot_size = 8
line_size = 10
tile_size = 50
pad = tile_size / 2
grid = True

def convert(pos, translate=0):
	return (pos[0]*tile_size + translate, pos[1]*tile_size + translate)

def visualize(moves, width, height):
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
	
	pos = (0, 0)
	pen_down = False
	for move in moves:
		print(move)
		if type(move) is tuple: # it's a displacement
			color = line_contact_color if pen_down else line_lifted_color
			draw.line(convert(pos, pad) + convert(move, pad), fill=color, width=line_size)
			pos = move
		elif type(move) is str: # it's a non-displacement operation 
			match move:
				case 'pen up':
					pen_down = False
					draw.arc(convert(pos, pad-dot_size) + convert(pos, pad+dot_size), -90, 90, fill=(255, 0, 0), width=15)
				case 'pen down':
					pen_down = True
					draw.arc(convert(pos, pad-dot_size) + convert(pos, pad+dot_size), 90, -90, fill=(0, 255, 0), width=15)

	img.show()


if __name__ == '__main__':
	# moves = [((8, 8), (0, 8)), ((8, 7), (0, 7)), ((8, 6), (0, 6)), ((8, 5), (8, 0)), ((7, 5), (7, 0)), ((6, 5), (6, 0)), ((5, 2), (0, 2)), ((5, 1), (0, 1)), ((5, 0), (0, 0)), ((2, 5), (0, 5)), ((2, 4), (0, 4)), ((2, 3), (0, 3))]
	width = 32
	height = 32
	img = Image.open('data/out.png')
	moves = navigate(img)
	print(moves)
	visualize(moves, width, height)

# slicing 3d objects into layers to print - slicer
# tracing the route of a pen on paper - tracer