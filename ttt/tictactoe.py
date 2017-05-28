class Board:
	DRAW = "(draw)"
	EMPTY = ' '

	def __init__(self, size=3, players=['X', 'O']):
		self.size = size
		self.players = players
		self.board = [[self.EMPTY for y in range(size)] for x in range(size)]
		self.turn = 0

	def draw(self, pmap=None):
		fmt = (" . | . | . \n"
		       "---+---+---\n"
		       " . | . | . \n"
		       "---+---+---\n"
		       " . | . | . \n".replace('.', '%s'))

		if pmap is None:
			pmap = lambda x, y, p: p

		return (fmt % tuple(map(lambda xyp: pmap(*xyp), self.as_tuples())))

	def winner(self):
		for p in self.players:
			# Horizontal
			for y in range(self.size):
				if all(map(lambda m: m == p, [self.board[x][y] for x in range(self.size)])):
					return p

			# Vertical
			for x in range(self.size):
				if all(map(lambda m: m == p, [self.board[x][y] for y in range(self.size)])):
					return p

			# Diagonal \
			if all(map(lambda m: m == p, [self.board[d][d] for d in range(self.size)])):
				return p

			# Diagonal /
			if all(map(lambda m: m == p, [self.board[(self.size-1)-d][d] for d in range(self.size)])):
				return p

		if len(list(filter(lambda m: m == self.EMPTY, self.as_list()))) == 0:
			return self.DRAW

		return None

	def play(self, x, y):
		if self.board[x][y] != self.EMPTY:
			return False

		self.board[x][y] = self.players[self.turn]
		self.turn = (self.turn + 1) % len(self.players)
		return True

	def to_play(self):
		return self.players[self.turn]

	def as_list(self):
		return [self.board[x][y] for y in range(self.size) for x in range(self.size)]

	def as_tuples(self):
		return [(x, y, self.board[x][y]) for y in range(self.size) for x in range(self.size)]
