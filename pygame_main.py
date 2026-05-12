import sys

import pygame

from game.board import Board
from ui.renderer import Renderer


def main():
    pygame.init()

    board = Board()
    board.setup_initial()
    renderer = Renderer(board)

    board_pixels = board.size * renderer.cell_size
    window_width = renderer.margin * 2 + board_pixels + 220
    window_height = renderer.margin * 2 + board_pixels
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Chaos Chess")

    clock = pygame.time.Clock()
    running = True
    selected = None
    turn = "white"

    while running:
        is_checkmate = board.is_checkmate(turn)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if is_checkmate:
                continue
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = renderer.square_from_mouse(event.pos)
                if clicked is None:
                    selected = None
                    continue

                if selected is None:
                    piece = board.get_piece(clicked[0], clicked[1])
                    if piece and piece.color == turn:
                        selected = clicked
                    else:
                        selected = None
                else:
                    start = board.coords_to_square(selected[0], selected[1])
                    end = board.coords_to_square(clicked[0], clicked[1])
                    try:
                        board.move_piece(start, end, turn)
                        turn = "black" if turn == "white" else "white"
                    except ValueError:
                        pass
                    selected = None

        status_lines = []
        if is_checkmate:
            winner = "white" if turn == "black" else "black"
            status_lines.append(f"Checkmate: {winner} wins")
        elif board.is_in_check(turn):
            status_lines.append("Check")

        screen.fill((20, 20, 20))
        renderer.draw(
            screen,
            selected=selected,
            turn=turn,
            status_lines=status_lines,
            moves=board.move_history,
        )
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
