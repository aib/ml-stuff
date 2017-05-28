class Board:
	DRAW = "(draw)"
	EMPTY = ' '

	def __init__(self, size=3, players=['X', 'O']):
		self.size = size
		self.players = players
		self.board = [self.EMPTY] * (size * size)
		self.turn = 0

	def get(self, x, y):
		return self.board[x + y*self.size]

	def set(self, x, y, p):
		self.board[x + y*self.size] = p

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
				if all(map(lambda m: m == p, [self.get(x, y) for x in range(self.size)])):
					return p

			# Vertical
			for x in range(self.size):
				if all(map(lambda m: m == p, [self.get(x, y) for y in range(self.size)])):
					return p

			# Diagonal \
			if all(map(lambda m: m == p, [self.get(d, d) for d in range(self.size)])):
				return p

			# Diagonal /
			if all(map(lambda m: m == p, [self.get((self.size-1)-d, d) for d in range(self.size)])):
				return p

		if len(list(filter(lambda m: m == self.EMPTY, self.as_list()))) == 0:
			return self.DRAW

		return None

	def play(self, x, y):
		if self.get(x, y) != self.EMPTY:
			return False

		self.set(x, y, self.players[self.turn])
		self.turn = (self.turn + 1) % len(self.players)
		return True

	def to_play(self):
		return self.players[self.turn]

	def as_list(self):
		return [self.get(x, y) for y in range(self.size) for x in range(self.size)]

	def as_tuples(self):
		return [(x, y, self.get(x, y)) for y in range(self.size) for x in range(self.size)]
