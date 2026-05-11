class GameState:
	def __init__(self, board, players, turn_manager, deck):
		self.board = board
		self.players = players
		self.turn_manager = turn_manager
		self.deck = deck
