from utils import *
import math
from multiprocessing import Pool
from copy import deepcopy


class Scorer:
	def __init__(self, max_score):
		self.max_score = max_score





class ScorerConclude(Scorer):
	def apply(self, board, moves, scores, pl_id):
		for i,move in enumerate(moves):
			board.do_move(move.level, move.row, move.col, pl_id)
			if board.check_win() == get_result_from_id(pl_id):
				scores[i] += self.max_score
			board.undo_move(move.level, move.row, move.col)

class ScorerNoConclude(Scorer):
	def apply(self, board, moves, scores, pl_id):
		other_id = get_other_player_id(pl_id)
		for i,move in enumerate(moves):
			board.do_move(move.level, move.row, move.col, other_id)
			if board.check_win() == get_result_from_id(other_id):
				scores[i] += self.max_score
			board.undo_move(move.level, move.row, move.col)





class ScorerRecursive(Scorer):
	def __init__(self, max_score, rec):
		super().__init__(max_score)
		self.rec = rec
		self.scorer_conclude = ScorerConclude(max_score)

	def play_recursive(self, board, moves, acc_rec, turn):
		new_scores = [0 for move in moves]
		self.scorer_conclude.apply(board, moves, new_scores, turn)

		if acc_rec > 1 and max(new_scores) == 0:
			if acc_rec == self.rec: # if beginning of recursion, spawn workers
				with Pool(4) as p:
					new_boards = [deepcopy(board) for i in range(0, len(moves))]
					for new_board, move in zip(new_boards, moves):
						new_board.do_move(move.level, move.row, move.col, turn)
					new_temp_moves = [new_board.get_available_moves() for new_board in new_boards]
					acc_recs = [acc_rec - 1 for i in range(0, len(moves))]
					turns = [get_other_player_id(turn) for i in range(0, len(moves))]

					new_temp_scores = p.starmap(self.play_recursive, zip(new_boards, new_temp_moves, acc_recs, turns))

					for i, scores in enumerate(new_temp_scores):
						new_scores[i] = -max(scores)
			else:
				for i,move in enumerate(moves):
					board.do_move(move.level, move.row, move.col, turn)

					temp_moves = board.get_available_moves()
					temp_scores = self.play_recursive(board, temp_moves, acc_rec - 1, get_other_player_id(turn))

					if len(temp_scores) > 0:
						new_scores[i] = -max(temp_scores)

					board.undo_move(move.level, move.row, move.col)
		return new_scores

	def apply(self, board, moves, scores, pl_id):
		new_scores = self.play_recursive(board, moves, self.rec, pl_id)

		normalized_scores = [(score/max(max(new_scores),1))*self.max_score for score in new_scores]
		for i in range(0, len(normalized_scores)):
			scores[i] += normalized_scores[i]





class ScorerRecursiveHeuristic(Scorer):
	def __init__(self, max_score, rec, scorers=None):
		super().__init__(max_score)
		self.rec = rec
		self.scorer_conclude = ScorerConclude(max_score)
		if scorers == None:
			self.scorers = []
		else:
			self.scorers = scorers


	def play_recursive(self, board, moves, acc_rec, turn):
		new_scores = [0 for move in moves]
		self.scorer_conclude.apply(board, moves, new_scores, turn)

		if acc_rec < self.rec and max(new_scores) == 0:
			if acc_rec == 1: # if beginning of recursion, spawn workers
				with Pool(4) as p:
					new_boards = [deepcopy(board) for i in range(0, len(moves))]
					for new_board, move in zip(new_boards, moves):
						new_board.do_move(move.level, move.row, move.col, turn)
					new_temp_moves = [new_board.get_available_moves() for new_board in new_boards]
					acc_recs = [acc_rec + 1 for i in range(0, len(moves))]
					turns = [get_other_player_id(turn) for i in range(0, len(moves))]

					new_temp_scores = p.starmap(self.play_recursive, zip(new_boards, new_temp_moves, acc_recs, turns))

					for i, scores in enumerate(new_temp_scores):
						new_scores[i] = -max(scores)
			else:
				for i,move in enumerate(moves):
					board.do_move(move.level, move.row, move.col, turn)

					temp_moves = board.get_available_moves()
					temp_scores = self.play_recursive(board, temp_moves, acc_rec + 1, get_other_player_id(turn))

					if len(temp_scores) > 0:
						new_scores[i] = -max(temp_scores)

					board.undo_move(move.level, move.row, move.col)
		
		for scorer in self.scorers:
			scorer.apply(board, moves, new_scores, turn)

		return new_scores

	def apply(self, board, moves, scores, pl_id):
		new_scores = self.play_recursive(board, moves, 1, pl_id)

		normalized_scores = [(score/max(max(new_scores),1))*self.max_score for score in new_scores]
		for i in range(0, len(normalized_scores)):
			scores[i] += normalized_scores[i]






class ScorerReferenceMax(Scorer):
	def __init__(self, max_score, reference_max):
		super().__init__(max_score)
		self.reference_max = reference_max

class ScorerCreational(ScorerReferenceMax):
	def apply(self, board, moves, scores, pl_id):
		new_scores = [0 for score in scores]
		for i,move in enumerate(moves):
			lines = board.get_all_lines_with_cell(move.level, move.row, move.col)
			tot = 0
			for line in lines:
				is_line_occupied = False
				line_tot = 0
				if pl_id == PlayerID.PLAYER_1:
					for cell in line:
						if cell == Cell.CELL_PLAYER_1:
							line_tot += 1
						elif cell == Cell.CELL_PLAYER_2:
							is_line_occupied = True
				elif pl_id == PlayerID.PLAYER_2:
					for cell in line:
						if cell == Cell.CELL_PLAYER_2:
							line_tot += 1
						elif cell == Cell.CELL_PLAYER_1:
							is_line_occupied = True
				if not is_line_occupied:
					tot += line_tot
			new_scores[i] = tot

		#reference_max = 6

		normalized_scores = [min((score/self.reference_max)*self.max_score, self.max_score) for score in new_scores]
		for i in range(0, len(normalized_scores)):
			scores[i] += normalized_scores[i]




class ScorerLocality(ScorerReferenceMax):
	def apply(self, board, moves, scores, pl_id):
		cells = board.get_all_cells_of_player(pl_id)

		new_scores = [0 for score in scores]
		for i,move in enumerate(moves):
			for cell in cells:
				new_scores[i] += max(move.level - cell.level, move.row - cell.row, move.col - cell.col)

		for i in range(0, len(moves)):
			new_scores[i] = max(new_scores) - new_scores[i]

		reference_max = max(self.reference_max * len(cells), 1)

		normalized_scores = [min((score/reference_max)*self.max_score, self.max_score) for score in new_scores]
		for i in range(0, len(normalized_scores)):
			scores[i] += normalized_scores[i]




class ScorerPositionalConclude(ScorerReferenceMax):
	def apply(self, board, moves, scores, pl_id):
		new_scores = [0 for score in scores]
		for i,move in enumerate(moves):
			if move.level == 0 or move.level == 3:
				if move.row == 0 or move.row == 3:
					if move.col == 0 or move.col == 3:
						new_scores[i] = 7
					else:
						new_scores[i] = 4
				else:
					if move.col == 0 or move.col == 3:
						new_scores[i] = 4
					else:
						new_scores[i] = 4
			else:
				if move.row == 0 or move.row == 3:
					if move.col == 0 or move.col == 3:
						new_scores[i] = 4
					else:
						new_scores[i] = 4
				else:
					if move.col == 0 or move.col == 3:
						new_scores[i] = 4
					else:
						new_scores[i] = 7

		#reference_max = 7

		normalized_scores = [min((score/self.reference_max)*self.max_score, self.max_score) for score in new_scores]
		for i in range(0, len(normalized_scores)):
			scores[i] += normalized_scores[i]