# this is a proof of concept navigator, I plan to do a better one in the future

# algorithm (stripes):
# pick the direction of the stripes
# start up of the plate
# move back and forth lowering the pen wherever there is a dot 

from turtle import Vec2D
from plopping import make_plopchart
from navigation_types import Node, Direction, painted, directions

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
def longstroke(img, neighbor_mode: Direction = Direction.ORTHODIAGONAL):
	(nodes, _) = make_nodes(img)
	moves: list[Vec2D | str] = []
	
	node = nodes.pop()
	moves.append(node.pos)
	moves.append('pen down')

	while len(nodes) > 0:		
		longchain = 0
		selected = (0, 0)
		for direction in directions[neighbor_mode]:
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

def make_nodes(img):
	def meet(x, y, dx, dy): # makes a pair of nodes neighbors
		nodemap[x+dx][y+dy].neibs[-dx, -dy] = node
		node.neibs[dx, dy] = nodemap[x+dx][y+dy]

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
				if x > 0: 
					if painted(pixels[x-1, y]):
						meet(x, y, -1, 0)
					if y > 0 and painted(pixels[x-1, y-1]):
						meet(x, y, -1, -1)
					if y < height and painted(pixels[x-1, y+1]):
						meet(x, y, -1, 1)
				if y > 0:
					if painted(pixels[x, y-1]):
						meet(x, y, 0, -1)
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
	moves = longstroke(plopchart, Direction.ORTHODIAGONAL)
	# print(moves)
	visualiser.visualize(moves, width, height, show=True)
