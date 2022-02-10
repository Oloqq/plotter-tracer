# this is a proof of concept navigator, I plan to do a better one in the future

# algorithm (stripes): continuous Z movement gets the motor really hot so idk if its a good idea
# pick the direction of the stripes
# start up of the plate
# move back and forth lowering the pen wherever there is a dot 

from functools import reduce
import functools
import math
from turtle import Vec2D
from plopping import make_plopchart
from navigation_types import Node, Direction, painted, directions

# check how many nodes can be painted in a given direction from a node
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
# find longest uninterrupted orthodiagonal stroke from it
# repeat until all nodes are in a path
# find a way to draw all the paths asap
def longstroke(img, neighbor_mode: Direction = Direction.ORTHODIAGONAL):
	(nodes, _) = make_nodes(img)
	paths = []
	
	# find all the paths
	node = nodes.pop()
	paths.append([])
	path = paths[len(paths) - 1]
	path.append(node.pos)
	while len(nodes) > 0:		
		longchain = 0
		selected = (0, 0)
		for reverse in directions[neighbor_mode]:
			chain = check_direction(node, reverse)
			if chain > longchain:
				longchain = chain
				selected = reverse
		endnode = mark_direction_visited(node, selected)

		if longchain > 1: # there is an actual stroke
			path.append(endnode.pos)
			node = endnode
		elif longchain == 1: # this node is the only one getting painted
			while len(nodes) > 0:
				node = nodes.pop()
				if not node.visited: break
			else: break
			paths.append([])
			path = paths[len(paths) - 1]
			path.append(node.pos)			
	
	# figure out the order of drawing
	def distance(left: Vec2D, right: Vec2D):
		return math.sqrt((left - right) * (left - right))

	# TODO there's no need do lift the pen if the next point is right next to the tool
	# ignore lifting when going over painted area: turn on / off by a setting
	moves: list[Vec2D | str] = []
	toolhead = Vec2D(0, 0)
	while len(paths) > 0:
		min_dist = 1000000
		chosen = None
		reverse = False
		for path in paths:
			d = distance(toolhead, path[0])
			if d < min_dist:
				min_dist = d
				chosen = path
				reverse = False
			d = distance(toolhead, path[-1])
			if d < min_dist:
				min_dist = d
				chosen = path
				reverse = True
		paths.remove(chosen)
		if reverse: chosen.reverse()
		toolhead = chosen[-1]
		moves.append(chosen[0])
		moves.append('pen down')
		for i in range(1, len(chosen)):
			moves.append(chosen[i])
		moves.append('pen up')

	return moves

def make_nodes(img):
	def meet(x, y, dx, dy): # makes a pair of nodes neighbors
		nodemap[x+dx, y+dy].neibs[-dx, -dy] = node
		node.neibs[dx, dy] = nodemap[x+dx, y+dy]

	pixels = img.load()
	width, height = img.size
	nodemap: dict[Vec2D, Node] = {}
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
					if y < height and painted(pixels[x-1, y+1]):
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

	def peel_in_place_f(nodes: list[Node], nodemap: dict[Vec2D, Node]) \
		-> tuple[list[Node], list[Node], dict[Vec2D, Node]]:
		outline = []
		inside = []
		for node in nodes:
			if is_outline(node):
				outline.append(node)
				nodemap.pop(node.pos)
			else:
				inside.append(node)
		return outline, inside, nodemap

	def peel(nodes: list[Node], nodemap: dict[Vec2D, Node]) \
		-> tuple[list[Node], list[Node], dict[Vec2D, Node]]:
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
		current = outline.pop()
		moves.append(current.pos)
		moves.append('pen down')
		while len(outline) > 0:
			available, neighborhood = current.neighborhood(outline)
			match available:
				case 0:
					if len(outline) == 0:
						return
					current = outline.pop()
					moves.append('pen up')
					moves.append(current.pos)
					moves.append('pen down')
				case 1:
					current = neighborhood
					outline.remove(current)
				case _: # choose the one with least connections
					least = 10 # max neighbors in outline is 7
					chosen = None
					# print('search start', available, len(neighborhood.items()))
					for neib, his_neibs in neighborhood.items():
						if his_neibs < least:
							least = his_neibs
							chosen = neib
							# print('new chosen', chosen, least)
					current = chosen
					# print('done', current, least)
					outline.remove(current)
			moves.append(current.pos)

	if peel_in_place:
		peel = peel_in_place_f
	(nodes, nodemap) = make_nodes(img)
	moves: list[tuple[int, int] | str] = []

	while len(nodes) > 0:
		outline, nodes, nodemap = peel(nodes, nodemap)
		if len(outline) > 0:
			trace_outline(outline)
		else:
			break

	return moves

import visualiser
if __name__ == "__main__":
	# img = Image.open('data/out.png')
	plopchart = make_plopchart('data/mak.png', save=False, show=False)
	moves = closing_circles(plopchart)
	# moves = squiggler(plopchart)
	# print(moves)
	width, height = plopchart.size
	visualiser.visualize(moves, width, height, show=True)