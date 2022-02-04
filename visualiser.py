from PIL import Image, ImageDraw

line_color = (128, 255, 255)

line_size = 20
tile_size = 50
pad = tile_size / 2
grid = True

def visualize(moves, width, height):
	img = Image.new('RGB',
		(width * tile_size, height * tile_size), color=(87, 87, 87))
	draw = ImageDraw.Draw(img)

	outw = width * tile_size
	outh = height * tile_size

	if grid:
		for x in range(width):
			draw.line([x*tile_size, 0, x*tile_size, outh], fill=(0, 0, 0), width=1)
		for y in range(height):
			draw.line([0, y*tile_size, outw, y*tile_size], fill=(0, 0, 0), width=1)
		draw.line([outw-1, 0, outw-1, outh], fill=(0, 0, 0), width=1)
		draw.line([0, outh-1, outw, outh-1], fill=(0, 0, 0), width=1)
	
	for move in moves:
		if type(move) is tuple: # it's a displacement
			(start, end) = move
			draw.line([start[0]*tile_size+pad, start[1]*tile_size+pad, end[0]*tile_size+pad, end[1]*tile_size+pad], fill=line_color, width=line_size)
		elif type(move) is str: # it's a non-displacement operation 
			print(f'MOVE: {move}')

	img.show()


if __name__ == '__main__':
	moves = [((8, 8), (0, 8)), ((8, 7), (0, 7)), ((8, 6), (0, 6)), ((8, 5), (8, 0)), ((7, 5), (7, 0)), ((6, 5), (6, 0)), ((5, 2), (0, 2)), ((5, 1), (0, 1)), ((5, 0), (0, 0)), ((2, 5), (0, 5)), ((2, 4), (0, 4)), ((2, 3), (0, 3))]
	width = 9
	height = 9
	visualize(moves, width, height)

# slicing 3d objects into layers to print - slicer
# tracing the route of a pen on paper - tracer