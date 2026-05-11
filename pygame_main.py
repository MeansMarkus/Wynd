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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((20, 20, 20))
        renderer.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
