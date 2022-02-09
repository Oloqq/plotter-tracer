from turtle import Vec2D
from enum import Enum
from typing_extensions import Self

def painted(pixel):
	return pixel == 0 # black pixels are considered painted

class Direction(Enum):
	ORTHAGONAL = 1,
	DIAGONAL = 2,
	ORTHODIAGONAL = 3

directions = {
	Direction.ORTHAGONAL: [(-1, 0), (1, 0), (0, -1), (0, 1)],
	Direction.DIAGONAL: [(-1, -1), (1, -1), (1, 1), (-1, 1)],
}
directions[Direction.ORTHODIAGONAL] = directions[Direction.ORTHAGONAL] + \
                                      directions[Direction.DIAGONAL]

class Node:
	def __init__(self, x, y):
		self.pos = Vec2D(x, y)
		self.visited = False
		self.neibs: dict[Vec2D, Self] = {}
		for d in directions[Direction.ORTHODIAGONAL]:
			self.neibs[d] = None

	def neibs_in(self, control: list[Self]) -> list[Self]:
		ret = []
		for d in directions[Direction.ORTHODIAGONAL]:
			if self.neibs[d] in control:
				ret.append(self.neibs[d])
		return ret

	def neighborhood(self, control: list[Self]) -> tuple[int, dict[Self, int]|Self]:
		neibs = self.neibs_in(control)
		if len(neibs) == 0:
			return (0, None)
		if len(neibs) == 1:
			return (1, neibs[0])

		ret = {}
		for neib in neibs:
			l = len(neib.neibs_in(control))
			if l > 0:
				ret[neib] = l

		return (len(neibs), ret)
