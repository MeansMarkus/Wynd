import sys

import pygame

from game.board import Board
from ui.renderer import Renderer


def main():
    pygame.init()

    board = Board()
    board.setup_initial()
    renderer = Renderer(board)

    window_size = renderer.margin * 2 + board.size * renderer.cell_size
    screen = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption("Chaos Chess")

    clock = pygame.time.Clock()
    running = True
    selected = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                selected = renderer.square_from_mouse(event.pos)

        screen.fill((20, 20, 20))
        renderer.draw(screen, selected=selected)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
