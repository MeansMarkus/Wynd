class TurnManager:
	def __init__(self, players):
		self.players = list(players)
		self.index = 0
		self.direction = 1
		self.skip = 0

	def current_player(self):
		return self.players[self.index]

	def peek_next_player(self):
		next_index = (self.index + self.direction) % len(self.players)
		return self.players[next_index]

	def advance(self):
		steps = 1 + self.skip
		self.skip = 0
		self.index = (self.index + self.direction * steps) % len(self.players)

	def reverse(self):
		self.direction *= -1

	def skip_next(self, count=1):
		self.skip += count
