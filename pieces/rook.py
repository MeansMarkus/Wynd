from pieces.piece import Piece


class Rook(Piece):
	symbol = "r"

	def get_moves(self, board, position):
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		return self._ray_moves(board, position, directions)
