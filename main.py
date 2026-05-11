from game.board import Board


def main():
    board = Board()
    board.place_piece("e", 2, "P")
    board.place_piece("e", 7, "p")
    board.place_piece("d", 1, "K")
    print(board.render())


if __name__ == "__main__":
    main()
        