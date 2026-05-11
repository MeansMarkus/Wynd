class Player:
	def __init__(self, name, color):
		self.name = name
		self.color = color
		self.hand = []

	def draw(self, deck, count=1):
		for _ in range(count):
			card = deck.draw()
			if card is None:
				break
			self.hand.append(card)

	def play_card(self, index, game_state):
		if index < 0 or index >= len(self.hand):
			raise ValueError("Invalid card index")
		card = self.hand.pop(index)
		card.apply(game_state, self)
		game_state.deck.discard(card)
		return card
