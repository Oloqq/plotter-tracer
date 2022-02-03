# this is a proof of concept navigator, I plan to do a better one in the future
# add diagonal lines
# draw outline first

# tuple[int, int] prolly should have its own Position class

from typing_extensions import Self
from PIL import Image

moves = []

class Node:
	def __init__(self, x, y):
		self.x = x
		self.y = y
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
def mark_direction_visited(node: Node, direction: tuple[int, int]) -> tuple[int, int]:
	node.visited = True
	while node[direction] and not node[direction].visited:
		node = node[direction]
		node.visited = True
	return (node.x, node.y)

# algorithm: pick an unvisited spot, find longest uninterrupted orthagonal path
# from it, paint it, mark as visited, repeat
def navigate(img):
	(nodes, _) = make_nodes(img)
	moves: list[tuple[tuple[int, int], tuple[int, int]]] = []
	
	while len(nodes) > 0:
		while len(nodes) > 0:
			node = nodes.pop()
			if not node.visited: break
		else: break
		longchain = 0
		selected = (0, 0)
		for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			chain = check_direction(node, direction)
			if chain > longchain:
				longchain = chain
				selected = direction
		endpos = mark_direction_visited(node, selected)
		moves.append(((node.x, node.y), endpos))
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

if __name__ == "__main__":
	def t_make_nodes():
		img = Image.open('data/plopchart.png')
		nodes, nodemap = make_nodes(img)
		lefttop = nodemap[0][0]
		assert lefttop
		assert not lefttop.top
		assert not lefttop.left
		assert lefttop.bottom
		cursor = lefttop.bottom
		assert cursor.top
		assert cursor.bottom
		cursor = lefttop.bottom
		assert cursor.top
		assert cursor.right

	def t_navigate():
		img = Image.open('data/plopchart.png')
		moves = navigate(img)
		print(moves)
	
	t_navigate()
