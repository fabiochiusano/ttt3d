import matplotlib.pyplot as plt
from utils import *
from players import *
from board import *
from game import *

class Simulation:
	pass

class Simulation1vs1:
	def __init__(self, p1, p2, levels, rows, cols):
		self.p1 = p1
		self.p2 = p2
		self.board = Board(levels,rows,cols)
		self.results = [0,0,0]
		self.tot_turns = 0

	def play(self, iterations):
		for i in range(0, iterations):
			self.board.reset()

			# half times p1 starts, half times p2 starts
			start_p1 = i % 2 == 0
			if start_p1:
				game = Game(self.board, self.p1, self.p2)
			else:
				game = Game(self.board, self.p2, self.p1)

			result = game.play()
			self.tot_turns += len(game.moves_1) + len(game.moves_2)

			if (result == Result.RESULT_WIN_1 and start_p1) or (result == Result.RESULT_WIN_2 and not start_p1):
				self.results[0] += 1
			elif (result == Result.RESULT_WIN_2 and start_p1) or (result == Result.RESULT_WIN_1 and not start_p1):
				self.results[1] += 1
			else:
				self.results[2] += 1

			self.avg_turns = self.tot_turns / (i + 1)
			self.print_summary()

			#if i % int(iterations / 8) == 0:
			#	self.print_summary()

		self.avg_turns = self.tot_turns / iterations
		self.print_summary()

	def show_results(self):
		# Results of p1
		names = ["win", "lost", "draw"]

		for i,name in enumerate(names):
		    plt.bar(i, self.results[i])

		plt.xticks(range(len(names)), names)
		plt.yticks(range(0, 100, 5))
		plt.ylim(0, 100)

		plt.show()

	def print_summary(self):
		print("Win: {0}".format(self.results[0]))
		print("Lost: {0}".format(self.results[1]))
		print("Draw: {0}".format(self.results[2]))
		print("Avg # of turns per game: {0}".format(self.avg_turns))