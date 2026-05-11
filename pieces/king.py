from pieces.piece import Piece


class King(Piece):
	symbol = "k"

	def get_moves(self, board, position):
		steps = [
			(1, 0),
			(-1, 0),
			(0, 1),
			(0, -1),
			(1, 1),
			(1, -1),
			(-1, 1),
			(-1, -1),
		]
		moves = self._step_moves(board, position, steps)

		row, col = position
		if board.can_castle(self.color, "kingside"):
			moves.append((row, col + 2))
		if board.can_castle(self.color, "queenside"):
			moves.append((row, col - 2))

		return moves

	def attacks(self, board, position):
		steps = [
			(1, 0),
			(-1, 0),
			(0, 1),
			(0, -1),
			(1, 1),
			(1, -1),
			(-1, 1),
			(-1, -1),
		]
		return self._step_moves(board, position, steps)
