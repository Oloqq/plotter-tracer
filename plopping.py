# make a plopchart from input image (black-white)
# the plopchart represents where should the pen plop the paper
# find a decent order of strokes to fill all the positions on the plopchart
# convert to gcode

# only pure black pixels (0, 0, 0) are interpreted as painted

from PIL import Image
import math

brush_um = 800
pixel_to_um = 2400
plops_per_pixel = math.floor(pixel_to_um / brush_um)
print('ppp: ', plops_per_pixel)

# pixels, width, height, plops per pixel
def make_plopchart(pixels, w, h, ppp):
	if ppp < 1:
		print('ppp < 1 will need some smart interpolation. TBD')
		exit()

	out = Image.new('1', (w*ppp, h*ppp), (1))
	for x in range(w):
		for y in range(h):
			(r, g, b) = pixels[x, y]
			val = r+g+b
			for i in range(ppp):
				for j in range(ppp):
					out.putpixel((x*ppp+i, y*ppp+j), val)

	out.save('data/out.png')
	# out.show()

	return out

def main():
	img = Image.open('data/3x3.png')
	pixels = img.load()
	width, height = img.size
	make_plopchart(pixels, width, height, plops_per_pixel)
	# for x in range(width):
	# 	for y in range(height):
	# 		print(pixels[x, y])

if __name__ == "__main__":
	main()


