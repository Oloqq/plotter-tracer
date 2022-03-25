from turtle import Vec2D
import numpy as np
from numpy import linalg

def analyse(moves: list[Vec2D|str]):
	pen_down = False
	paint_distance = 0
	idle_distance = 0

	pos = np.array([0, 0])
	for move in moves:
		if move == 'pen down':
			pen_down = True
			continue
		elif move == 'pen up':
			pen_down = False
			continue
		
		move = np.array([move[0], move[1]])
		dist = linalg.norm(pos - move)
		if pen_down:
			paint_distance += dist
		else:
			idle_distance += dist


	return {
		'travel-distance': int(paint_distance + idle_distance),
		'paint-distance': int(paint_distance),
		'idle-distance': int(idle_distance),
		'idle-percent': int(100 * idle_distance / (paint_distance + idle_distance)),
	}
