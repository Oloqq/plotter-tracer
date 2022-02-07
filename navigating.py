# this is a proof of concept navigator, I plan to do a better one in the future

# algorithm (stripes):
# pick the direction of the stripes
# start up of the plate
# move back and forth lowering the pen wherever there is a dot 

from turtle import Vec2D
from typing_extensions import Self

moves = []

class Node:
	def __init__(self, x, y):
		self.pos = Vec2D(x, y)
		self.visited = False
		self.left = None
		self.right = None
		self.top = None
		self.bottom = None

	def __getitem__(self, key) -> Self | None:
		match key:
			case (-1, 0): return self.left
			case (1, 0):  return self.right
			case (0, -1): return self.top
			case (0, 1):  return self.bottom
			case _: raise KeyError
			

def check_direction(node: Node, direction: tuple[int, int]):
	chain = 1
	while node[direction] and not node[direction].visited:
		chain += 1
		node = node[direction]
	return chain

# mark nodes in a direction of node as selected
# additionaly, return position of the last node
def mark_direction_visited(node: Node, direction: tuple[int, int]) -> Node:
	node.visited = True
	while node[direction] and not node[direction].visited:
		node = node[direction]
		node.visited = True
	return node

# algorithm (longstroke):
# pick an unpainted spot
# find longest uninterrupted orthagonal (todo: orthodiagonal) path from it
# paint it try to repeat from the end spot, else pick a random new spot
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
					nodemap[x-1][y].right = node
					node.left = nodemap[x-1][y]
				if y > 0 and painted(pixels[x, y-1]):
					nodemap[x][y-1].bottom = node
					node.top = nodemap[x][y-1]
	return nodes, nodemap


# algorithm (closing circles):
# get outline of the shape
# draw that outline in one long stroke
# remove the outline from plopchart
# repeat
# # with a limit on depth can act as contour drawing
# # select continuous line vs distinct circles
# def closing_circles(img):
# 	(nodes, _) = make_nodes(img)
# 	moves: list[tuple[int, int] | str] = []


from PIL import Image, ImageDraw
import visualiser
if __name__ == "__main__":
	width = 32
	height = 32
	img = Image.open('data/out.png')
	moves = longstroke(img)
	print(moves)
	# visualiser.visualize(moves, width, height, show=True)
