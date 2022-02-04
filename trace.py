from plopping import make_plopchart
from navigating import navigate
from visualiser import visualize
from PIL import Image

if __name__ == '__main__':
	img = Image.open('data/lenny.png')
	pixels = img.load()
	width, height = img.size
	make_plopchart(pixels, width, height, 1)

	img = Image.open('data/out.png')
	moves = navigate(img)

	width, height = img.size
	visualize(moves, width, height)