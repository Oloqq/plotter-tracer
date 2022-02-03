# this is a proof of concept navigator, I plan to do a better one in the future
# add diagonal lines
# draw outline first

from tabnanny import check
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

	def __getitem__(self, key):
		match key:
			case (-1, 0):
				return self.left

def check_direction(node, direction: tuple[int, int]):
	chain = 1
	while node[direction]:
		node = node[direction]
		chain += 1
	return chain

# algorithm: pick an unvisited spot, find longest uninterrupted orthagonal path
# from it, paint it, mark as visited, repeat
def navigate(img):
	(nodes, _) = make_nodes(img)
	node = nodes.pop()
	longchain = 0
	selected = (0, 0)
	# check left
	chain = check_direction(node, (-1, 0))
	if chain > longchain:
		longchain = chain
		selected = (-1, 0)

	assert selected == (-1, 0)
	assert longchain == 9, longchain
	

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
		# should start at bottom right

		# should pick line to the left or up
	
	t_navigate()
