# make a plopchart from input image (black-white)
# the plopchart represents where should the pen plop the paper

# only pure black pixels (0, 0, 0) are interpreted as painted

from PIL import Image
import math

# sample values todo: make configurable
brush_um = 2400  # um = micrometers
pixel_to_um = 2400
# brush_um = 9600  # um = micrometers
# pixel_to_um = 9600
plops_per_pixel = math.floor(pixel_to_um / brush_um)


def make_plopchart(filename, save=False, show=False):
    img = Image.open(filename)
    pixels = img.load()
    w, h = img.size
    ppp = plops_per_pixel

    if ppp < 1:
        print('ppp < 1 will need some smart interpolation. TBD')
        exit()

    out = Image.new('1', (w*ppp, h*ppp), (1))
    for x in range(w):
        for y in range(h):
            try:
                (r, g, b) = pixels[x, y]
            except ValueError:
                (r, g, b, a) = pixels[x, y]
            val = r+g+b
            for i in range(ppp):
                for j in range(ppp):
                    out.putpixel((x*ppp+i, y*ppp+j), val)

    if type(save) is str:
        out.save(save)
    if show:
        out.show()

    return out


if __name__ == "__main__":
    out = make_plopchart('data/albania.png', save='data/out.png', show=False)
    print(out)
