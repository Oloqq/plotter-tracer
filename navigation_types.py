from turtle import Vec2D
from enum import Enum

def painted(pixel):
	return pixel == 0 # black pixels are considered painted

class Direction(Enum):
	ORHTAGONAL = 1,
	DIAGONAL = 2,
	ORTHODIAGONAL = 3

directions = {
	Direction.ORHTAGONAL: [(-1, 0), (1, 0), (0, -1), (0, 1)],
	Direction.DIAGONAL: [(-1, -1), (1, -1), (1, 1), (-1, 1)],
}
directions[Direction.ORTHODIAGONAL] = directions[Direction.ORHTAGONAL] + \
                                      directions[Direction.DIAGONAL]

class Node:
	def __init__(self, x, y):
		self.pos = Vec2D(x, y)
		self.visited = False
		self.neibs = {}
		for d in directions[Direction.ORTHODIAGONAL]:
			self.neibs[d] = None
			
