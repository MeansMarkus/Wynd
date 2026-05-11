from cards.card import Card


class ReverseCard(Card):
	name = "Reverse"

	def apply(self, game_state, player):
		game_state.turn_manager.reverse()
