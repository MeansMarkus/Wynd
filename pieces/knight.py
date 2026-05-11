from pieces.piece import Piece


class Knight(Piece):
	symbol = "n"

	def get_moves(self, board, position):
		steps = [
			(2, 1),
			(2, -1),
			(-2, 1),
			(-2, -1),
			(1, 2),
			(1, -2),
			(-1, 2),
			(-1, -2),
		]
		return self._step_moves(board, position, steps)
