from pieces.piece import Piece


class Queen(Piece):
	symbol = "q"

	def get_moves(self, board, position):
		directions = [
			(1, 0),
			(-1, 0),
			(0, 1),
			(0, -1),
			(1, 1),
			(1, -1),
			(-1, 1),
			(-1, -1),
		]
		return self._ray_moves(board, position, directions)
