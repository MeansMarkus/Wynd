from game.board import Board


def main():
    board = Board()
    board.setup_initial()
    turn = "white"

    while True:
        print(board.render())
        if board.is_checkmate(turn):
            print(f"Checkmate! {turn} loses.")
            break
        if board.is_stalemate(turn):
            print("Stalemate.")
            break
        if board.is_in_check(turn):
            print("Check!")

        move_input = input(f"{turn} move (e2 e4) or 'quit': ").strip()
        if move_input.lower() in ("quit", "exit"):
            break

        parts = move_input.split()
        if len(parts) != 2:
            print("Enter moves like: e2 e4")
            continue

        try:
            board.move_piece(parts[0], parts[1], turn)
        except ValueError as exc:
            print(exc)
            continue

        turn = "black" if turn == "white" else "white"


if __name__ == "__main__":
    main()
        