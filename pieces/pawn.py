from pieces.piece import Piece


class Pawn(Piece):
	symbol = "p"

	def get_moves(self, board, position):
		row, col = position
		direction = -1 if self.color == "white" else 1
		start_row = 6 if self.color == "white" else 1
		moves = []

		one_step = row + direction
		if board.in_bounds(one_step, col) and board.get_piece(one_step, col) is None:
			moves.append((one_step, col))
			two_step = row + (2 * direction)
			if row == start_row and board.get_piece(two_step, col) is None:
				moves.append((two_step, col))

		for dc in (-1, 1):
			r, c = row + direction, col + dc
			if board.in_bounds(r, c):
				target = board.get_piece(r, c)
				if target and target.color != self.color:
					moves.append((r, c))

		if board.en_passant_target:
			ep_row, ep_col = board.en_passant_target
			if ep_row == row + direction and abs(ep_col - col) == 1:
				moves.append((ep_row, ep_col))

		return moves

	def attacks(self, board, position):
		row, col = position
		direction = -1 if self.color == "white" else 1
		attacks = []
		for dc in (-1, 1):
			r, c = row + direction, col + dc
			if board.in_bounds(r, c):
				attacks.append((r, c))
		return attacks
