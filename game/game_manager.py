class GameManager:
	def __init__(self, game_state):
		self.game_state = game_state

	def run(self):
		board = self.game_state.board
		turn_manager = self.game_state.turn_manager

		while True:
			player = turn_manager.current_player()
			color = player.color

			print(board.render())
			if board.is_checkmate(color):
				print(f"Checkmate! {color} loses.")
				break
			if board.is_stalemate(color):
				print("Stalemate.")
				break
			if board.is_threefold_repetition(color):
				print("Draw by threefold repetition.")
				break
			if board.is_fifty_move_rule():
				print("Draw by fifty-move rule.")
				break
			if board.is_in_check(color):
				print("Check!")

			if len(player.hand) < 5:
				player.draw(self.game_state.deck)

			hand_display = ", ".join(f"{i}:{card}" for i, card in enumerate(player.hand))
			print(f"{player.name} hand: {hand_display}")

			move_input = input(f"{player.name} ({color}) move or 'card #': ").strip()
			if move_input.lower() in ("quit", "exit"):
				break

			if move_input.startswith("card"):
				parts = move_input.split()
				if len(parts) != 2 or not parts[1].isdigit():
					print("Use: card <index>")
					continue
				try:
					index = int(parts[1])
					card = player.play_card(index, self.game_state)
					print(f"Played {card}.")
				except ValueError as exc:
					print(exc)
					continue
			else:
				parts = move_input.split()
				if len(parts) != 2:
					print("Enter moves like: e2 e4")
					continue

				try:
					board.move_piece(parts[0], parts[1], color)
				except ValueError as exc:
					print(exc)
					continue

			turn_manager.advance()
