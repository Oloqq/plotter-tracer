from plopping import make_plopchart
from navigating import navigate
from visualiser import visualize
from PIL import Image

if __name__ == '__main__':
	plopchart = make_plopchart('data/lenny.png', save=False, show=False)
	moves = navigate(plopchart)

	width, height = plopchart.size
	visualize(moves, width, height)