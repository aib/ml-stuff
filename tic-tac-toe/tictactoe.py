import copy

class Board:
	DRAW = "(draw)"
	EMPTY = ' '

	def __init__(self, size=3, players=['X', 'O']):
		self.size = size
		self.players = copy.copy(players)
		self.original_players = copy.copy(players)
		self.board = [self.EMPTY] * (size * size)
		self.turn = 0
		self.players_eliminated = True

	def get(self, x, y):
		return self.board[x + y*self.size]

	def set(self, x, y, p):
		self.board[x + y*self.size] = p

	def save(self):
		return (copy.copy(self.board), self.turn)

	def load(self, data):
		(self.board, self.turn) = data

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
		if self.players_eliminated:
			if len(self.players) == 0:
				return self.DRAW
			elif len(self.players) == 1:
				return self.players[0]

		# Horizontal -
		for y in range(self.size):
			f = self.get(0, y)
			if f in self.players:
				if all(map(lambda x: self.get(x, y) == f, range(1, self.size))):
					return f

		# Vertical |
		for x in range(self.size):
			f = self.get(x, 0)
			if f in self.players:
				if all(map(lambda y: self.get(x, y) == f, range(1, self.size))):
					return f

		# Diagonal \
		f = self.get(0, 0)
		if f in self.players:
			if all(map(lambda d: self.get(d, d) == f, range(1, self.size))):
				return f

		# Diagonal /
		f = self.get((self.size-1), 0)
		if f in self.players:
			if all(map(lambda d: self.get((self.size-1)-d, d) == f, range(1, self.size))):
				return f

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

	def eliminate(self, player):
		self.players.remove(player)
		self.players_eliminated = True

	def as_list(self):
		return [self.get(x, y) for y in range(self.size) for x in range(self.size)]

	def as_tuples(self):
		return [(x, y, self.get(x, y)) for y in range(self.size) for x in range(self.size)]
