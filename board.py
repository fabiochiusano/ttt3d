from utils import *

class Board:
	def __init__(self, levels, rows, cols):
		self.levels = levels
		self.rows = rows
		self.cols = cols
		matrix = []
		for i in range(0,levels):
			level = []
			for j in range(0,rows):
				row = []
				for k in range(0,cols):
					row.append(Cell.CELL_EMPTY)
				level.append(row)
			matrix.append(level)
		self.matrix = matrix

	def get_available_moves(self):
		available_moves = []

		for level in range(0, len(self.matrix)):
			for row in range(0, len(self.matrix[level])):
				for col in range(0, len(self.matrix[level][row])):
					if self.is_move_ok(level, row, col):
						available_moves.append(Move(level, row, col))

		return available_moves

	def get_all_cells_of_player(self, pl_id):
		if pl_id == PlayerID.PLAYER_1:
			check_cell = Cell.CELL_PLAYER_1
		else:
			check_cell = Cell.CELL_PLAYER_2

		res = []

		for level in range(0, len(self.matrix)):
			for row in range(0, len(self.matrix[level])):
				for col in range(0, len(self.matrix[level][row])):
					if self.matrix[level][row][col] == check_cell:
						res.append(Move(level, row, col))

		return res


	def get_all_lines_with_cell(self, level, row, col):
		# Returns an array of lines
		res = []

		# Lines in planes
		level_plane = self.get_level_plane(level)
		res.append(level_plane[row])
		res.append(transpose(level_plane)[col])
		row_plane = self.get_row_plane(row)
		res.append(transpose(row_plane)[col])
		
		# Diagonals in planes
		if (level == row):
			col_plane = self.get_col_plane(col)
			res.append([col_plane[c][c] for c in range(0, len(col_plane))])
		if (level == self.rows - row - 1):
			col_plane = self.get_col_plane(col)
			res.append([col_plane[c][len(col_plane) - c - 1] for c in range(0, len(col_plane))])
		if (level == col):
			row_plane = self.get_row_plane(row)
			res.append([row_plane[c][c] for c in range(0, len(row_plane))])
		if (level == self.cols - col - 1):
			row_plane = self.get_row_plane(row)
			res.append([row_plane[c][len(row_plane) - c - 1] for c in range(0, len(row_plane))])
		if (row == col):
			level_plane = self.get_level_plane(level)
			res.append([level_plane[c][c] for c in range(0, len(level_plane))])
		if (row == self.cols - col - 1):
			level_plane = self.get_level_plane(level)
			res.append([level_plane[c][len(level_plane) - c - 1] for c in range(0, len(level_plane))])

		# Cube diagonal
		if (level == row == col):
			diag_plane = self.get_diagonal_plane(Diagonal.DIAGONAL_PRIMARY)
			res.append([diag_plane[c][c] for c in range(0, len(diag_plane))])
		if (level == (self.rows - row - 1) == (self.cols - col - 1)):
			diag_plane = self.get_diagonal_plane(Diagonal.DIAGONAL_PRIMARY)
			res.append([diag_plane[c][len(diag_plane) - c - 1] for c in range(0, len(diag_plane))])
		if (level == col == (self.rows - row - 1)):
			diag_plane = self.get_diagonal_plane(Diagonal.DIAGONAL_SECONDARY)
			res.append([diag_plane[c][c] for c in range(0, len(diag_plane))])
		if (level == row == (self.cols - col - 1)):
			diag_plane = self.get_diagonal_plane(Diagonal.DIAGONAL_SECONDARY)
			res.append([diag_plane[c][len(diag_plane) - c - 1] for c in range(0, len(diag_plane))])

		return res


	def check_win(self, last_move=None):
		# Returns a RESULT

		# Check level planes
		for level in range(0, self.levels):
			if last_move == None or last_move.level == level:
				level_plane = self.get_level_plane(level)
				result = self.check_win_in_plane(level_plane)
				if result != Result.RESULT_CONTINUE:
					return result

		# Check row planes
		for row in range(0, self.rows):
			if last_move == None or last_move.row == row:
				row_plane = self.get_row_plane(row)
				result = self.check_win_in_plane(row_plane)
				if result != Result.RESULT_CONTINUE:
					return result

		# Check col planes
		for col in range(0, self.cols):
			if last_move == None or last_move.col == col:
				col_plane = self.get_col_plane(col)
				result = self.check_win_in_plane(col_plane)
				if result != Result.RESULT_CONTINUE:
					return result

		# Check cube diagonals
		diag_plane_1 = self.get_diagonal_plane(Diagonal.DIAGONAL_PRIMARY)
		result = self.check_win_in_plane(diag_plane_1)
		if result != Result.RESULT_CONTINUE:
			return result
		diag_plane_2 = self.get_diagonal_plane(Diagonal.DIAGONAL_SECONDARY)
		result = self.check_win_in_plane(diag_plane_2)
		if result != Result.RESULT_CONTINUE:
			return result

		# Check if draw
		is_draw = True
		for row in self.matrix[self.levels-1]:
			for col in row:
				if col == Cell.CELL_EMPTY:
					is_draw = False
		if is_draw:
			return Result.RESULT_DRAW

		return Result.RESULT_CONTINUE

	def check_win_in_plane(self, plane):
		# Returns a RESULT
		# "plane" is a 2D matrix

		# Check rows
		for row in plane:
			result = self.check_win_in_line(row)
			if result != Result.RESULT_CONTINUE:
				return result

		# Check cols
		transposed_plane = transpose(plane)
		for row in transposed_plane:
			result = self.check_win_in_line(row)
			if result != Result.RESULT_CONTINUE:
				return result

		# Check diagonals
		diag_1 = [plane[col_n][col_n] for col_n in range(0, len(plane))]
		result = self.check_win_in_line(diag_1)
		if result != Result.RESULT_CONTINUE:
			return result
		diag_2 = [plane[col_n][self.cols-col_n-1] for col_n in range(0, len(plane))]
		result = self.check_win_in_line(diag_2)
		if result != Result.RESULT_CONTINUE:
			return result

		return Result.RESULT_CONTINUE

	def check_win_in_line(self, line):
		# Returns a RESULT
		# "line" is a 1D matrix

		cell_check = line[0]

		if cell_check == Cell.CELL_EMPTY:
			return Result.RESULT_CONTINUE

		for cell_n in range(1, len(line)):
			cell = line[cell_n]
			if cell != cell_check:
				return Result.RESULT_CONTINUE

		if cell_check == Cell.CELL_PLAYER_1:
			return Result.RESULT_WIN_1
		else:
			return Result.RESULT_WIN_2

	def get_level_plane(self, level):
		# Return a rows_x_cols matrix
		return self.matrix[level]

	def get_row_plane(self, row):
		# Return a levels_x_cols matrix
		structured_row = []

		for level in self.matrix:
			structured_row.append(level[row])

		return structured_row

	def get_col_plane(self, col):
		# Return a levels_x_rows matrix
		structured_col = []

		for level in self.matrix:
			temp = []
			for row in level:
				temp.append(row[col])
			structured_col.append(temp)

		return structured_col

	def get_diagonal_plane(self, diag):
		# Returns a levels_x_[rows,cols] matrix
		structured_diag = []

		for level in self.matrix:
			temp = []
			for row in range(0, len(level)):
				for col in range(0, len(level[row])):
					if (diag == Diagonal.DIAGONAL_PRIMARY and row == col) or (diag == Diagonal.DIAGONAL_SECONDARY and row == (self.cols-col-1)):
						temp.append(level[row][col])

			structured_diag.append(temp)

		return structured_diag

	def do_move(self, level, row, col, p_id, verbose=False):
		ok = self.is_move_ok(level, row, col, verbose)

		if ok:
			if p_id == PlayerID.PLAYER_1:
				self.matrix[level][row][col] = Cell.CELL_PLAYER_1
			else:
				self.matrix[level][row][col] = Cell.CELL_PLAYER_2
		
		return ok

	def undo_move(self, level, row, col):
		self.matrix[level][row][col] = Cell.CELL_EMPTY

	def is_move_ok(self, level, row, col, verbose=False):
		# Out of bounds
		if (level < 0 or level >= self.levels) or (row < 0 or row >= self.rows) or (col < 0 or col >= self.cols):
			if verbose:
				print("Cell out of bounds")
			return False

		# If the cell is already occupied
		if self.matrix[level][row][col] != Cell.CELL_EMPTY:
			if verbose:
				print("Cell already occupied")
			return False

		# If the underlying level is not already occupied
		elif level > 0 and self.matrix[level-1][row][col] == Cell.CELL_EMPTY:
			if verbose:
				print("Underlying cell still empty")
			return False

		else:
			return True

	def print_board(self):
		for level in range(0, len(self.matrix)):
			print("Level {0}".format(level))
			for row in range(0, len(self.matrix[level])):
				for col in range(0, len(self.matrix[level][row])):
					print(self.matrix[level][row][col].value, end=' ')
				print()
			print()

	def reset(self):
		for level in range(0, len(self.matrix)):
			for row in range(0, len(self.matrix[level])):
				for col in range(0, len(self.matrix[level][row])):
					self.matrix[level][row][col] = Cell.CELL_EMPTY