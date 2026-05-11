from pieces.piece import Piece


class Bishop(Piece):
	symbol = "b"

	def get_moves(self, board, position):
		directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
		return self._ray_moves(board, position, directions)
