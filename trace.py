from plopping import make_plopchart
from navigating import longstroke
from visualiser import visualize
from gcoding import encode

# slicing 3d objects into layers to print - slicer
# tracing the route of a pen on paper     - tracer

# todo: handle grayscale as well as rgba

if __name__ == '__main__':
	plopchart = make_plopchart('data/mak.png', save=False, show=False)
	moves = longstroke(plopchart)

	width, height = plopchart.size
	# the result is saved in data/visualiser_out
	visualize(moves, width, height, show=True)

	encode(moves, save='data/mak.gcode')