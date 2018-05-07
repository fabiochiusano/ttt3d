from utils import *

class Game:
	def __init__(self, board, p1, p2):
		self.board = board
		p1.set_id(PlayerID.PLAYER_1)
		self.p1 = p1
		self.moves_1 = []
		p2.set_id(PlayerID.PLAYER_2)
		self.p2 = p2
		self.moves_2 = []

	def play(self, verbose=False):
		result = self.board.check_win()
		while result == Result.RESULT_CONTINUE:
			if verbose:
				self.board.print_board()
			move_1 = self.p1.play(self.board)
			executed_move = self.execute_move(move_1, self.p1)
			result = self.board.check_win(executed_move)
			if result != Result.RESULT_CONTINUE:
				break

			if verbose:
				self.board.print_board()
			move_2 = self.p2.play(self.board)
			executed_move = self.execute_move(move_2, self.p2)
			result = self.board.check_win(executed_move)

		if verbose:
			self.board.print_board()

			if result == Result.RESULT_WIN_1:
				print("Player 1 won!")
			elif result == Result.RESULT_WIN_2:
				print("Player 2 won!")
			else:
				print("Draw!")

		return result

	def execute_move(self, move, p):
		if move.undo:
			if p == self.p1:
				last_move_2 = self.moves_2.pop()
				self.board.undo_move(last_move_2.level, last_move_2.row, last_move_2.col)
				last_move_1 = self.moves_1.pop()
				self.board.undo_move(last_move_1.level, last_move_1.row, last_move_1.col)
			else:
				last_move_1 = self.moves_1.pop()
				self.board.undo_move(last_move_1.level, last_move_1.row, last_move_1.col)
				last_move_2 = self.moves_2.pop()
				self.board.undo_move(last_move_2.level, last_move_2.row, last_move_2.col)
			print("Move undone")
			self.board.print_board()
			new_move = p.play(self.board)
			return self.execute_move(new_move, p)
		else:
			self.board.do_move(move.level, move.row, move.col, p.id)
			if p == self.p1:
				self.moves_1.append(move)
			else:
				self.moves_2.append(move)
			return move