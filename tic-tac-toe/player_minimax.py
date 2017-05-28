import copy

class MinimaxPlayer:
	def __init__(self, board):
		pass

	def play(self, board):
		move = self.eval_board(board)
		return move[0]

	def eval_board(self, board):
		if board.winner() != None:
			if board.winner() == board.DRAW:
				return (None, 0)
			else:
				return (None, -100)

		avail = map(lambda xyp: (xyp[0], xyp[1]), filter(lambda xyp: xyp[2] == board.EMPTY, board.as_tuples()))

		scores = []
		for move in avail:
			board_save = board.save()
			board.play(move[0], move[1])
			score = self.eval_board(board)
			board.load(board_save)
			scores.append((move, -score[1]))

		return max(scores, key=lambda s: s[1])

def create_player(board):
	return MinimaxPlayer(board)

def destroy_player(player):
	pass
