import numpy as np

from common import nn

SHAPE = (9, 81, 9)
FILE = '../data/ttt_nn.pickle'
RATE = 0.01
MULTIPLIERS = (+1.0, +0.5, -1.0) # win, draw, loss

class NNumpyPlayer:
	def __init__(self, board, my_token, net):
		self.token = my_token
		self.net = net
		self.moves = []
		self.all_moves = {}
		for p in board.players:
			self.all_moves[p] = []

	def play(self, board):
		board_num = self._board_to_input(board)
		outp = self.net.execute([board_num])[0]
		chosen = max(enumerate(outp), key=lambda ix: ix[1])[0]
		self.moves.append((board_num, chosen))

		(x, y) = (chosen % 3, chosen // 3)
		return (x, y)

	def played(self, player, board, move):
		self.all_moves[player].append((self._board_to_input(board), move))

	def result(self, board, winner):
		for p in self.all_moves:
			if winner == p:
				mul = MULTIPLIERS[0]
			elif winner == board.DRAW:
				mul = MULTIPLIERS[1]
			else:
				mul = MULTIPLIERS[2]

			for (board_input, move) in self.all_moves[p]:
				move_num = move[1] * board.size + move[0]
				outp = list(map(lambda w: mul if w == move_num else -mul, range(9)))
				self.net.train([board_input], [outp], RATE)

	def _board_to_input(self, board):
		inp = list(map(lambda xyp: 0 if xyp[2] == board.EMPTY else 1 if xyp[2] == board.to_play() else -1, board.as_tuples()))
		return inp

def create_player(board, token):
	try:
		with open(FILE, 'rb') as f:
			net = nn.MLP.from_file(f)
	except FileNotFoundError:
		print("Creating network from scratch")
		net = nn.MLP(SHAPE)
		net.randomize()

	return NNumpyPlayer(board, token, net)

def destroy_player(player):
	with open(FILE, 'wb') as f:
		player.net.save(f)
