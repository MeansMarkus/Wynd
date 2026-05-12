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
        self.white_piece = (245, 245, 245)
        self.black_piece = (30, 30, 30)
        self.outline = (15, 15, 15)
        self.font = pygame.font.SysFont("Segoe UI", 36, bold=True)
        self.status_font = pygame.font.SysFont("Segoe UI", 20, bold=True)

    def draw(self, screen, selected=None, turn=None, status_lines=None, moves=None):
        self._draw_status(screen, turn, status_lines)
        self._draw_moves(screen, moves)
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
                    color = self.white_piece if piece.color == "white" else self.black_piece
                    label = self.font.render(piece.get_symbol(), True, color)
                    label_rect = label.get_rect(
                        center=(x + self.cell_size / 2, y + self.cell_size / 2)
                    )
                    if piece.color == "white":
                        outline = self.font.render(piece.get_symbol(), True, self.outline)
                        outline_rect = outline.get_rect(center=label_rect.center)
                        screen.blit(outline, outline_rect.move(1, 1))
                    screen.blit(label, label_rect)

    def _draw_status(self, screen, turn, status_lines):
        y = 10
        if turn:
            label = self.status_font.render(f"Turn: {turn}", True, (230, 230, 230))
            screen.blit(label, (self.margin, y))
            y += 22

        if status_lines:
            for line in status_lines:
                label = self.status_font.render(line, True, (230, 230, 230))
                screen.blit(label, (self.margin, y))
                y += 22

    def _draw_moves(self, screen, moves):
        if not moves:
            return

        max_lines = 12
        recent = moves[-max_lines:]
        x = self.margin + self.board.size * self.cell_size + 10
        y = self.margin

        title = self.status_font.render("Moves", True, (230, 230, 230))
        screen.blit(title, (x, y))
        y += 22

        start_index = len(moves) - len(recent)
        for idx, move in enumerate(recent, start=start_index + 1):
            if isinstance(move, dict):
                text = f"{idx}. {move['start']}-{move['end']}"
            else:
                text = f"{idx}. {move}"
            label = self.status_font.render(text, True, (230, 230, 230))
            screen.blit(label, (x, y))
            y += 20

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
