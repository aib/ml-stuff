import random

class RandomPlayer:
	def __init__(self, board):
		pass

	def play(self, board):
		avail = [(x, y, board.board[x][y])
		         for y in range(board.size)
		         for x in range(board.size)
		         if board.board[x][y] == board.EMPTY]
		(x, y, t) = random.choice(avail)
		return (x, y)

def create_player(board):
	return RandomPlayer(board)

def destroy_player(player):
	pass
