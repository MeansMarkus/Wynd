import unittest

from game.board import Board
from pieces.king import King


class TestRules(unittest.TestCase):
    def test_threefold_repetition(self):
        board = Board()
        board.setup_initial()
        turn = "white"

        moves = [
            ("g1", "f3"),
            ("g8", "f6"),
            ("f3", "g1"),
            ("f6", "g8"),
        ]

        for _ in range(2):
            for start, end in moves:
                board.move_piece(start, end, turn)
                turn = "black" if turn == "white" else "white"

        self.assertTrue(board.is_threefold_repetition("white"))

    def test_fifty_move_rule(self):
        board = Board()
        board.grid = [[None for _ in range(board.size)] for _ in range(board.size)]
        board.place_piece("e", 1, King("white"))
        board.place_piece("e", 8, King("black"))
        board.record_position("white")

        turn = "white"
        for _ in range(50):
            board.move_piece("e1", "e2", turn)
            turn = "black"
            board.move_piece("e8", "e7", turn)
            turn = "white"
            board.move_piece("e2", "e1", turn)
            turn = "black"
            board.move_piece("e7", "e8", turn)
            turn = "white"

        self.assertTrue(board.is_fifty_move_rule())


if __name__ == "__main__":
    unittest.main()
