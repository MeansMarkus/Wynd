from cards.card import Card


class PlusTwoCard(Card):
	name = "Plus Two"

	def apply(self, game_state, player):
		if not game_state.board.captured[player.color]:
			raise ValueError("No captured pieces to revive")

		revived = game_state.board.revive_captured(player.color, 2)
		if revived == 0:
			raise ValueError("No space to revive pieces")

		game_state.moves_left = max(game_state.moves_left, 2)
