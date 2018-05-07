from enum import Enum

class PlayerID(Enum):
	PLAYER_1 = 0
	PLAYER_2 = 1

class Cell(Enum):
	CELL_EMPTY = 0
	CELL_PLAYER_1 = 1
	CELL_PLAYER_2 = 2

class Result(Enum):
	RESULT_CONTINUE = 0
	RESULT_WIN_1 = 1
	RESULT_WIN_2 = 2
	RESULT_DRAW = 3

class Diagonal(Enum):
	DIAGONAL_PRIMARY = 0
	DIAGONAL_SECONDARY = 1


class Move:
	def __init__(self, level, row, col, undo=False):
		self.level = level
		self.row = row
		self.col = col
		self.undo = undo

def get_other_player_id(i):
		if i == PlayerID.PLAYER_1:
			return PlayerID.PLAYER_2
		else:
			return PlayerID.PLAYER_1

def get_result_from_id(i):
	if i == PlayerID.PLAYER_1:
		return Result.RESULT_WIN_1
	else:
		return Result.RESULT_WIN_2

def transpose(matrix):
	return [list(x) for x in zip(*matrix)]