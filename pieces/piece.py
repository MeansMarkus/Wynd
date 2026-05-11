class Piece:
	symbol = "?"

	def __init__(self, color):
		self.color = color
		self.moved = False

	def get_symbol(self):
		return self.symbol.upper() if self.color == "white" else self.symbol.lower()

	def get_moves(self, board, position):
		return []

	def attacks(self, board, position):
		return self.get_moves(board, position)

	def _ray_moves(self, board, position, directions):
		row, col = position
		moves = []
		for dr, dc in directions:
			r, c = row + dr, col + dc
			while board.in_bounds(r, c):
				target = board.get_piece(r, c)
				if target is None:
					moves.append((r, c))
				else:
					if target.color != self.color:
						moves.append((r, c))
					break
				r += dr
				c += dc
		return moves

	def _step_moves(self, board, position, steps):
		row, col = position
		moves = []
		for dr, dc in steps:
			r, c = row + dr, col + dc
			if board.in_bounds(r, c):
				target = board.get_piece(r, c)
				if target is None or target.color != self.color:
					moves.append((r, c))
		return moves
