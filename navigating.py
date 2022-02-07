# this is a proof of concept navigator, I plan to do a better one in the future

# algorithm (stripes):
# pick the direction of the stripes
# start up of the plate
# move back and forth lowering the pen wherever there is a dot 

from turtle import Vec2D
from typing_extensions import Self

from plopping import make_plopchart

moves = []

class Node:
	def __init__(self, x, y):
		self.pos = Vec2D(x, y)
		self.visited = False
		self.neibs = { # neighbors
			(-1, 0): None,
			(1, 0):  None,
			(0, -1): None,
			(0, 1):  None,
		}
			

def check_direction(node: Node, direction: tuple[int, int]):
	chain = 1
	while node.neibs[direction] and not node.neibs[direction].visited:
		chain += 1
		node = node.neibs[direction]
	return chain

# mark nodes in a direction of node as selected
# additionaly, return position of the last node
def mark_direction_visited(node: Node, direction: tuple[int, int]) -> Node:
	node.visited = True
	while node.neibs[direction] and not node.neibs[direction].visited:
		node = node.neibs[direction]
		node.visited = True
	return node

# algorithm (longstroke):
# pick an unpainted spot
# find longest uninterrupted orthagonal (todo: orthodiagonal) path from it
# paint it try to repeat from the end spot, else pick a random new spot
## make diagonal moves
def longstroke(img):
	(nodes, _) = make_nodes(img)
	moves: list[Vec2D | str] = []
	
	node = nodes.pop()
	moves.append(node.pos)
	moves.append('pen down')

	while len(nodes) > 0:		
		longchain = 0
		selected = (0, 0)
		for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			chain = check_direction(node, direction)
			if chain > longchain:
				longchain = chain
				selected = direction
		endnode = mark_direction_visited(node, selected)

		if longchain > 1: # there is an actual stroke
			moves.append(endnode.pos)
			node = endnode
		elif longchain == 1: # this node is the only one getting painted
			moves.append('pen up')
			while len(nodes) > 0:
				node = nodes.pop()
				if not node.visited: break
			else: break
			moves.append(node.pos)
			moves.append('pen down')
	return moves

def painted(pixel):
	return pixel == 0 # black pixels are considered painted

def make_nodes(img):
	pixels = img.load()
	width, height = img.size
	nodemap: list[list[Node]] = [[None for _ in range(height)] for _ in range(width)]
	nodes: list[Node] = []
	for x in range(width):
		for y in range(height):
			if painted(pixels[x, y]):
				node = Node(x, y)
				nodes.append(node)
				nodemap[x][y] = node
				# connect neighbors
				if x > 0 and painted(pixels[x-1, y]):
					nodemap[x-1][y].neibs[1, 0] = node
					node.neibs[-1, 0] = nodemap[x-1][y]
				if y > 0 and painted(pixels[x, y-1]):
					nodemap[x][y-1].neibs[0, 1] = node
					node.neibs[0, -1] = nodemap[x][y-1]
	return nodes, nodemap


# algorithm (closing circles):
# get outline of the shape - outline <=> there is a white pixel next to a black one
# draw that outline in one long stroke
# remove the outline from plopchart
# repeat
# # with a limit on depth can act as contour drawing
# # select continuous line vs distinct circles
def closing_circles(img, limit=None, continuous=False):
	(nodes, nodemap) = make_nodes(img)
	moves: list[tuple[int, int] | str] = []

	return moves


from PIL import Image, ImageDraw
import visualiser
if __name__ == "__main__":
	width = 32
	height = 32
	# img = Image.open('data/out.png')
	plopchart = make_plopchart('data/banana.png', save=False, show=False)
	moves = closing_circles(plopchart)
	print(moves)
	visualiser.visualize(moves, width, height, show=True)
