import pygame


class Renderer:
    def __init__(self, board, cell_size=80, margin=40):
        self.board = board
        self.cell_size = cell_size
        self.margin = margin
        self.dark = (118, 150, 86)
        self.light = (238, 238, 210)
        self.grid = (30, 30, 30)
        self.highlight = (246, 246, 105)
        self.text_color = (20, 20, 20)
        self.font = pygame.font.SysFont("Segoe UI", 36, bold=True)

    def draw(self, screen, selected=None):
        board_size = self.board.size
        for row in range(board_size):
            for col in range(board_size):
                x = self.margin + col * self.cell_size
                y = self.margin + row * self.cell_size
                is_dark = (row + col) % 2 == 1
                color = self.dark if is_dark else self.light
                if selected == (row, col):
                    color = self.highlight
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

                piece = self.board.get_piece(row, col)
                if piece:
                    label = self.font.render(piece.get_symbol(), True, self.text_color)
                    label_rect = label.get_rect(
                        center=(x + self.cell_size / 2, y + self.cell_size / 2)
                    )
                    screen.blit(label, label_rect)

    def square_from_mouse(self, pos):
        x, y = pos
        board_size = self.board.size
        if x < self.margin or y < self.margin:
            return None
        x -= self.margin
        y -= self.margin
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < board_size and 0 <= col < board_size:
            return int(row), int(col)
        return None
