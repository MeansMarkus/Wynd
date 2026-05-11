from cards.card import Card


class PlusFourCard(Card):
	name = "Plus Four"

	def apply(self, game_state, player):
		target = game_state.turn_manager.peek_next_player()
		for _ in range(4):
			card = game_state.deck.draw()
			if card is None:
				break
			target.hand.append(card)
		game_state.turn_manager.skip_next()
