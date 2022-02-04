from plopping import make_plopchart
from navigating import navigate
from visualiser import visualize
from gcoding import encode

# slicing 3d objects into layers to print - slicer
# tracing the route of a pen on paper     - tracer

if __name__ == '__main__':
	plopchart = make_plopchart('data/smile.png', save=False, show=False)
	moves = navigate(plopchart)

	width, height = plopchart.size
	# the result is saved in data/visualiser_out
	visualize(moves, width, height, show=False)

	# encode(moves)