import random


class Card:
	name = "Card"

	def apply(self, game_state, player):
		raise NotImplementedError()

	def __str__(self):
		return self.name


class Deck:
	def __init__(self, cards):
		self.draw_pile = list(cards)
		self.discard_pile = []
		random.shuffle(self.draw_pile)

	def draw(self):
		if not self.draw_pile:
			self._reshuffle()
		if not self.draw_pile:
			return None
		return self.draw_pile.pop()

	def discard(self, card):
		if card is not None:
			self.discard_pile.append(card)

	def _reshuffle(self):
		if not self.discard_pile:
			return
		self.draw_pile = self.discard_pile
		self.discard_pile = []
		random.shuffle(self.draw_pile)
