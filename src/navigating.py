from .navigation_types import *
from .logger import log

Coord = Vec2D


def make_nodes(img):
    def meet(x, y, dx, dy):  # makes a pair of nodes neighbors
        nodemap[x+dx, y+dy].neibs[-dx, -dy] = node
        node.neibs[dx, dy] = nodemap[x+dx, y+dy]

    pixels = img.load()
    width, height = img.size
    nodemap: dict[Coord, Node] = {}
    nodes: list[Node] = []
    for x in range(width):
        for y in range(height):
            if painted(pixels[x, y]):
                node = Node(x, y)
                nodes.append(node)
                nodemap[x, y] = node
                # connect neighbors
                if x > 0:
                    if painted(pixels[x-1, y]):
                        meet(x, y, -1, 0)
                    if y > 0 and painted(pixels[x-1, y-1]):
                        meet(x, y, -1, -1)
                    if y < height-1 and painted(pixels[x-1, y+1]):
                        meet(x, y, -1, 1)
                if y > 0:
                    if painted(pixels[x, y-1]):
                        meet(x, y, 0, -1)
    return nodes, nodemap

# algorithm (squiggler):
# perform closing circles but don't use a buffer when updating nodemap
# the result is very long, continuous but squiggly lines


def squiggler(img):
    return closing_circles(img, peel_in_place=True)

# algorithm (closing circles):
# get outline of the shape - outline <=> there is a white pixel next to a black one
# draw that outline in a few long strokes
# remove the outline from plopchart
# repeat
# # with a limit on depth can act as contour drawing
# # select continuous line vs distinct circles
# TODO needs optimalization (of both output and algorithm itself)
# for output: start new line near the end of previous one
# do not lift the pen when unnecessary
# for working: when creating outline make new list of nodes to check from
# nodes met in the iteration


def closing_circles(img, limit=None, continuous=False, peel_in_place=False):
    def is_outline(node: Node):
        nonlocal nodemap
        for d in directions[Direction.ORTHAGONAL]:
            if node.pos + d not in nodemap:
                return True
        return False

    def peel_in_place_f(nodes: list[Node], nodemap: dict[Coord, Node]) \
            -> tuple[list[Node], list[Node], dict[Coord, Node]]:
        outline = []
        inside = []
        for node in nodes:
            if is_outline(node):
                outline.append(node)
                nodemap.pop(node.pos)
            else:
                inside.append(node)
        return outline, inside, nodemap

    def peel(nodes: list[Node], nodemap: dict[Coord, Node]) \
            -> tuple[list[Node], list[Node], dict[Coord, Node]]:
        outline = []
        inside = []
        newnodemap = nodemap.copy()
        for node in nodes:
            if is_outline(node):
                outline.append(node)
                newnodemap.pop(node.pos)
            else:
                inside.append(node)
        nodemap = newnodemap
        return outline, inside, nodemap

    def trace_outline(outline: list[Node]):
        def prioritize_loneliest(nodes):
            least = 10  # max neighbors in outline is 7
            chosen = None
            for neib, his_neibs in nodes.items():
                if his_neibs < least:
                    least = his_neibs
                    chosen = neib
            return chosen

        current = outline.pop()
        moves.append(current.pos)
        moves.append('pen down')
        while len(outline) > 0:
            # when using lefttop this function could be much simpler
            available, neighborhood = current.neighborhood(outline)
            match available:
                case 0:
                    if len(outline) == 0:
                        return
                    current = outline.pop()
                    moves.append('pen up')
                    moves.append(current.pos)
                    moves.append('pen down')
                    # continue
                case 1:
                    current = neighborhood
                    outline.remove(current)
                case _:  # choose the leftmost one, then the topmost
                    current = prioritize_loneliest(neighborhood)
                    outline.remove(current)
            moves.append(current.pos)

    if peel_in_place:
        peel = peel_in_place_f
    (nodes, nodemap) = make_nodes(img)
    moves: list[tuple[int, int] | str] = []

    log('Peeling')
    peels = 0
    while len(nodes) > 0:
        outline, nodes, nodemap = peel(nodes, nodemap)
        peels += 1
        log(f'Peel {peels} finished. Outline size: {len(outline)}. Remaining: {len(nodes)}', console=True)
        if len(outline) > 0:
            log(f'Tracing', console=True)
            trace_outline(outline)
        else:
            break

        # log(f'Merging', console=True)

        # break # TEMP testing on just one layer
    return moves


if __name__ == "__main__":
    from visualiser import visualize
    from PIL import Image

    width = 32
    height = 32
    img = Image.open('data/out.png')
    moves = squiggler(img)
    # print(moves)
    visualize(moves, width, height, show=True)
