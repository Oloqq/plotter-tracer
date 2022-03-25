# 1st proof of concept idk if it's even worth improving

# from turtle import Vec2D
# from navigation_types import *
# from logger import log


# # check how many nodes can be painted in a given direction from a node
# def check_direction(node: Node, direction: tuple[int, int]):
# 	chain = 1
# 	while node.neibs[direction] and not node.neibs[direction].visited:
# 		chain += 1
# 		node = node.neibs[direction]
# 	return chain

# # mark nodes in a direction of node as selected
# # additionaly, return position of the last node
# def mark_direction_visited(node: Node, direction: tuple[int, int]) -> Node:
# 	node.visited = True
# 	while node.neibs[direction] and not node.neibs[direction].visited:
# 		node = node.neibs[direction]
# 		node.visited = True
# 	return node

# # algorithm (longstroke):
# # pick an unpainted spot
# # find longest uninterrupted orthodiagonal stroke from it
# # repeat until all nodes are in a path
# # find a way to draw all the paths asap
# def longstroke(img, neighbor_mode: Direction = Direction.ORTHODIAGONAL):
# 	(nodes, _) = make_nodes(img)
# 	paths = []
	
# 	# find all the paths
# 	node = nodes.pop()
# 	paths.append([])
# 	path = paths[len(paths) - 1]
# 	path.append(node.pos)
# 	while len(nodes) > 0:		
# 		longchain = 0
# 		selected = (0, 0)
# 		for reverse in directions[neighbor_mode]:
# 			chain = check_direction(node, reverse)
# 			if chain > longchain:
# 				longchain = chain
# 				selected = reverse
# 		endnode = mark_direction_visited(node, selected)

# 		if longchain > 1: # there is an actual stroke
# 			path.append(endnode.pos)
# 			node = endnode
# 		elif longchain == 1: # this node is the only one getting painted
# 			while len(nodes) > 0:
# 				node = nodes.pop()
# 				if not node.visited: break
# 			else: break
# 			paths.append([])
# 			path = paths[len(paths) - 1]
# 			path.append(node.pos)			
	
# 	# figure out the order of drawing
# 	def distance(left: Vec2D, right: Vec2D):
# 		return math.sqrt((left - right) * (left - right))

# 	# TODO there's no need do lift the pen if the next point is right next to the tool
# 	# ignore lifting when going over painted area: turn on / off by a setting
# 	moves: list[Vec2D | str] = []
# 	toolhead = Vec2D(0, 0)
# 	while len(paths) > 0:
# 		min_dist = 1000000
# 		chosen = None
# 		reverse = False
# 		for path in paths:
# 			d = distance(toolhead, path[0])
# 			if d < min_dist:
# 				min_dist = d
# 				chosen = path
# 				reverse = False
# 			d = distance(toolhead, path[-1])
# 			if d < min_dist:
# 				min_dist = d
# 				chosen = path
# 				reverse = True
# 		paths.remove(chosen)
# 		if reverse: chosen.reverse()
# 		toolhead = chosen[-1]
# 		moves.append(chosen[0])
# 		moves.append('pen down')
# 		for i in range(1, len(chosen)):
# 			moves.append(chosen[i])
# 		moves.append('pen up')

# 	return moves
