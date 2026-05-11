from cards.card import Card


class SkipCard(Card):
	name = "Skip"

	def apply(self, game_state, player):
		game_state.turn_manager.skip_next()
