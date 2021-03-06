import random

class RandomPlayer:
	def play(self, board):
		avail = filter(lambda xyp: xyp[2] == board.EMPTY, board.as_tuples())
		(x, y, t) = random.choice(list(avail))
		return (x, y)

def create_player(board, token):
	return RandomPlayer()

def destroy_player(player):
	pass
