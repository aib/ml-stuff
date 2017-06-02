class HumanPlayer:
	def __init__(self, board):
		pass

	def play(self, board):
		print(board.draw(lambda x, y, p: p if p != board.EMPTY else self.xytonum(board.size, x, y)), end="")
		print("Playing as %s, please input the square" % board.to_play())

		while True:
			try:
				num = int(input())
			except ValueError:
				continue
			xy = self.numtoxy(board.size, num)
			if xy is not None: break

		return xy

	def xytonum(self, size, x, y):
		return ((size - 1) - y) * size + x + 1

	def numtoxy(self, size, num):
		y = (size - 1) - ((num - 1) // size)
		x = (num - 1) % size
		if x in range(size) and y in range(size):
			return (x, y)
		else:
			return None

def create_player(board, token):
	return HumanPlayer(board)

def destroy_player(player):
	pass
