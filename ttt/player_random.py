import random

class RandomPlayer:
	def __init__(self, board):
		pass

	def play(self, board):
		return (random.randrange(board.size), random.randrange(board.size))

def create_player(board):
	return RandomPlayer(board)

def destroy_player(player):
	pass
