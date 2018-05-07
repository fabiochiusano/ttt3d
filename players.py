from utils import *
from random import randint
from scorer import *

class Player:
	def set_id(self, i):
		self.id = i

	def print_move(self, level, row, col, verbose=False):
		if verbose:
			print("Player {0} plays {1}{2}{3}".format(self.id,level,row,col))







class AIPlayer(Player):
	pass





class AISequentialPlayer(AIPlayer):
	def play(self, board, verbose=False):
		for level in range(0, board.levels):
			for row in range(0, board.rows):
				for col in range(0, board.cols):
					if board.do_move(level, row, col, self.id):
						self.print_move(level, row, col, verbose)
						return Move(level, row, col)

class AIRandomPlayer(AIPlayer):
	def play(self, board, verbose=False):
		available_moves = board.get_available_moves()
		choice = randint(0, len(available_moves)-1)
		move = available_moves[choice]
		board.do_move(move.level, move.row, move.col, self.id)
		self.print_move(move.level, move.row, move.col, verbose)
		return move

class AIScorePlayer(AIPlayer):
	def __init__(self, scorers=None):
		if scorers == None:
			self.scorers = []
		else:
			self.scorers = scorers

	def get_best_move(self, moves, scores):
		best_idx = []
		max_score = max(scores)
		for i,score in enumerate(scores):
			if score == max_score:
				best_idx.append(i)

		best_id = randint(0, len(best_idx)-1)
		return moves[best_idx[best_id]]

	def play(self, board, verbose=False):
		available_moves = board.get_available_moves()
		scores = [0 for move in available_moves]

		for scorer in self.scorers:
			scorer.apply(board, available_moves, scores, self.id)

		best_move = self.get_best_move(available_moves, scores)

		board.do_move(best_move.level, best_move.row, best_move.col, self.id)
		self.print_move(best_move.level, best_move.row, best_move.col, verbose)

		return best_move






class AIConcludePlayer(AIScorePlayer):
	def __init__(self):
		super().__init__()
		self.scorers.append(ScorerConclude(1))


class AINoConcludePlayer(AIScorePlayer):
	def __init__(self):
		super().__init__()
		self.scorers.append(ScorerNoConclude(1))

class AIFullConcludePlayer(AIScorePlayer):
	def __init__(self):
		super().__init__()
		self.scorers.append(ScorerConclude(2))
		self.scorers.append(ScorerNoConclude(1))

class AIFCRPlayer(AIScorePlayer):
	def __init__(self, rec):
		super().__init__()
		self.scorers.append(ScorerRecursive(1, rec))







class HumanPlayer(Player):
	def play(self, board, verbose=True):
		move = input("Player {0} move: ".format(self.id))
		try:
			level = int(move[0])
			row = int(move[1])
			col = int(move[2])
		except ValueError:
			if len(move) == 1 and move[0] == "-":
				return Move(0, 0, 0, True)
			else:
				print("Input format: [0-{levels-1}]^3 to move, [-] to undo last move")
				return self.play(board)

		while not board.is_move_ok(level, row, col, verbose=True):
			board.print_board()

			move = input("Player {0} move: ".format(self.id))
			try:
				level = int(move[0])
				row = int(move[1])
				col = int(move[2])
			except ValueError:
				if len(move) == 1 and move[0] == "-":
					return Move(0, 0, 0, True)
				print("Input format: [0-{levels-1}]^3")
				continue 

		self.print_move(level, row, col, verbose)
		return Move(level, row, col)