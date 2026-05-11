import pygame


class Renderer:
    def __init__(self, board, cell_size=80, margin=40):
        self.board = board
        self.cell_size = cell_size
        self.margin = margin
        self.dark = (118, 150, 86)
        self.light = (238, 238, 210)
        self.grid = (30, 30, 30)

    def draw(self, screen):
        board_size = self.board.size
        for row in range(board_size):
            for col in range(board_size):
                x = self.margin + col * self.cell_size
                y = self.margin + row * self.cell_size
                is_dark = (row + col) % 2 == 1
                color = self.dark if is_dark else self.light
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(x, y, self.cell_size, self.cell_size),
                )
                pygame.draw.rect(
                    screen,
                    self.grid,
                    pygame.Rect(x, y, self.cell_size, self.cell_size),
                    1,
                )
