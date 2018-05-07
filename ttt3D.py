from utils import *
from players import *
from board import *
from game import *
from simulation import *
import time

if __name__ == "__main__":
	start = time.time()

	p1 = AIScorePlayer([
		ScorerRecursive(max_score=100, rec=3),
		ScorerPositionalConclude(max_score=1, reference_max=7)
		])
	#p2 = AIFullConcludePlayer()
	p2 = AIScorePlayer([
		ScorerRecursive(max_score=100, rec=3),
		ScorerCreational(max_score=1, reference_max=7)
		])
	#p2 = HumanPlayer()

	sim = Simulation1vs1(p1, p2, 4, 4, 4)

	sim.play(100)

	end = time.time()
	print("Time elapsed: {0}".format(end - start))

	sim.show_results()

	"""

	board = Board(4,4,4)
	game = Game(board, p1, p2)
	game.play(verbose=True)

	"""