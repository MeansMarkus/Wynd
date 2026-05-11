
import copy

from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
from pieces.rook import Rook


class Board:
    def __init__(self, size=8):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.en_passant_target = None
        self.move_history = []
        self.halfmove_clock = 0
        self.position_counts = {}

    def setup_initial(self):
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.en_passant_target = None
        self.move_history = []
        self.halfmove_clock = 0
        self.position_counts = {}

        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_type in enumerate(order):
            self.grid[0][col] = piece_type("black")
            self.grid[7][col] = piece_type("white")

        for col in range(self.size):
            self.grid[1][col] = Pawn("black")
            self.grid[6][col] = Pawn("white")

        self.record_position("white")

    def render(self):
        lines = []
        header = "  " + " ".join(chr(ord("a") + i) for i in range(self.size))
        lines.append(header)

        for row_index, row in enumerate(self.grid):
            rank = self.size - row_index
            rendered = []
            for piece in row:
                rendered.append(piece.get_symbol() if piece else ".")
            lines.append(f"{rank:2} " + " ".join(rendered))

        return "\n".join(lines)

    def in_bounds(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size

    def get_piece(self, row, col):
        return self.grid[row][col]

    def set_piece(self, row, col, piece):
        self.grid[row][col] = piece

    def place_piece(self, file_char, rank, piece):
        row, col = self.parse_position(file_char, rank)
        self.grid[row][col] = piece

    def parse_square(self, square):
        square = square.strip()
        if len(square) != 2:
            raise ValueError(f"Invalid square: {square}")
        return self.parse_position(square[0], square[1])

    def parse_position(self, file_char, rank):
        if not isinstance(file_char, str) or len(file_char) != 1:
            raise ValueError(f"Invalid file: {file_char}")
        if not str(rank).isdigit():
            raise ValueError(f"Invalid rank: {rank}")

        col = ord(file_char.lower()) - ord("a")
        row = self.size - int(rank)
        if self.in_bounds(row, col):
            return row, col

        raise ValueError(f"Position out of bounds: {file_char}{rank}")

    def coords_to_square(self, row, col):
        file_char = chr(ord("a") + col)
        rank = str(self.size - row)
        return f"{file_char}{rank}"

    def find_king(self, color):
        for row in range(self.size):
            for col in range(self.size):
                piece = self.get_piece(row, col)
                if isinstance(piece, King) and piece.color == color:
                    return row, col
        return None

    def square_attacked(self, row, col, by_color):
        for r in range(self.size):
            for c in range(self.size):
                piece = self.get_piece(r, c)
                if piece and piece.color == by_color:
                    if (row, col) in piece.attacks(self, (r, c)):
                        return True
        return False

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        enemy = "black" if color == "white" else "white"
        return self.square_attacked(king_pos[0], king_pos[1], enemy)

    def can_castle(self, color, side):
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        row, col = king_pos
        king = self.get_piece(row, col)
        if king.moved or self.is_in_check(color):
            return False

        if side == "kingside":
            rook_col = 7
            path_cols = [5, 6]
        else:
            rook_col = 0
            path_cols = [1, 2, 3]

        rook = self.get_piece(row, rook_col)
        if not isinstance(rook, Rook) or rook.color != color or rook.moved:
            return False

        for c in path_cols:
            if self.get_piece(row, c) is not None:
                return False

        step_cols = [col + 1, col + 2] if side == "kingside" else [col - 1, col - 2]
        enemy = "black" if color == "white" else "white"
        for c in step_cols:
            if self.square_attacked(row, c, enemy):
                return False

        return True

    def get_legal_moves_for_piece(self, position):
        row, col = position
        piece = self.get_piece(row, col)
        if not piece:
            return []

        legal = []
        for move in piece.get_moves(self, position):
            if not self._would_leave_in_check(position, move):
                legal.append(move)
        return legal

    def _would_leave_in_check(self, start, end):
        board_copy = copy.deepcopy(self)
        board_copy._apply_move(start, end)
        piece = self.get_piece(start[0], start[1])
        if piece is None:
            return False
        return board_copy.is_in_check(piece.color)

    def _apply_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.get_piece(start_row, start_col)
        if piece is None:
            return

        capture = self.get_piece(end_row, end_col) is not None
        pawn_move = isinstance(piece, Pawn)
        castling = isinstance(piece, King) and abs(end_col - start_col) == 2
        en_passant_capture = False
        promotion = False

        previous_en_passant = self.en_passant_target
        self.en_passant_target = None

        if castling:
            if end_col > start_col:
                rook_start = (start_row, 7)
                rook_end = (start_row, 5)
            else:
                rook_start = (start_row, 0)
                rook_end = (start_row, 3)
            rook = self.get_piece(rook_start[0], rook_start[1])
            self.set_piece(rook_end[0], rook_end[1], rook)
            self.set_piece(rook_start[0], rook_start[1], None)
            if rook:
                rook.moved = True

        if isinstance(piece, Pawn):
            direction = -1 if piece.color == "white" else 1
            if (end_row, end_col) == previous_en_passant and self.get_piece(end_row, end_col) is None:
                captured_row = end_row - direction
                self.set_piece(captured_row, end_col, None)
            capture = True
            en_passant_capture = True

        self.set_piece(end_row, end_col, piece)
        self.set_piece(start_row, start_col, None)
        piece.moved = True

        if isinstance(piece, Pawn):
            if abs(end_row - start_row) == 2:
                passed_row = start_row + (-1 if piece.color == "white" else 1)
                self.en_passant_target = (passed_row, start_col)

            if end_row == 0 or end_row == self.size - 1:
                self.set_piece(end_row, end_col, Queen(piece.color))
                promotion = True

        return {
            "piece": piece,
            "capture": capture,
            "pawn_move": pawn_move,
            "castling": castling,
            "en_passant": en_passant_capture,
            "promotion": promotion,
        }

    def move_piece(self, start_square, end_square, color):
        start = self.parse_square(start_square)
        end = self.parse_square(end_square)
        piece = self.get_piece(start[0], start[1])
        if not piece:
            raise ValueError("No piece on that square")
        if piece.color != color:
            raise ValueError("Not your piece")

        legal_moves = self.get_legal_moves_for_piece(start)
        if end not in legal_moves:
            raise ValueError("Illegal move")

        move_info = self._apply_move(start, end)
        if move_info["pawn_move"] or move_info["capture"]:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        self.move_history.append(
            {
                "start": start_square,
                "end": end_square,
                "color": color,
                "piece": move_info["piece"].get_symbol(),
                "capture": move_info["capture"],
                "castling": move_info["castling"],
                "en_passant": move_info["en_passant"],
                "promotion": move_info["promotion"],
            }
        )

        next_turn = "black" if color == "white" else "white"
        self.record_position(next_turn)

    def has_legal_moves(self, color):
        for row in range(self.size):
            for col in range(self.size):
                piece = self.get_piece(row, col)
                if piece and piece.color == color:
                    if self.get_legal_moves_for_piece((row, col)):
                        return True
        return False

    def is_checkmate(self, color):
        return self.is_in_check(color) and not self.has_legal_moves(color)

    def is_stalemate(self, color):
        return not self.is_in_check(color) and not self.has_legal_moves(color)

    def _castling_rights(self):
        rights = []

        white_king = self.get_piece(7, 4)
        if isinstance(white_king, King) and not white_king.moved:
            rook = self.get_piece(7, 7)
            if isinstance(rook, Rook) and not rook.moved:
                rights.append("K")
            rook = self.get_piece(7, 0)
            if isinstance(rook, Rook) and not rook.moved:
                rights.append("Q")

        black_king = self.get_piece(0, 4)
        if isinstance(black_king, King) and not black_king.moved:
            rook = self.get_piece(0, 7)
            if isinstance(rook, Rook) and not rook.moved:
                rights.append("k")
            rook = self.get_piece(0, 0)
            if isinstance(rook, Rook) and not rook.moved:
                rights.append("q")

        return "".join(rights) if rights else "-"

    def _position_key(self, turn):
        rows = []
        for row in self.grid:
            rendered = []
            for piece in row:
                rendered.append(piece.get_symbol() if piece else ".")
            rows.append("".join(rendered))

        piece_layout = "/".join(rows)
        rights = self._castling_rights()
        en_passant = "-"
        if self.en_passant_target:
            en_passant = self.coords_to_square(self.en_passant_target[0], self.en_passant_target[1])
        return f"{piece_layout} {turn[0]} {rights} {en_passant}"

    def record_position(self, turn):
        key = self._position_key(turn)
        self.position_counts[key] = self.position_counts.get(key, 0) + 1

    def is_threefold_repetition(self, turn):
        key = self._position_key(turn)
        return self.position_counts.get(key, 0) >= 3

    def is_fifty_move_rule(self):
        return self.halfmove_clock >= 100
    


