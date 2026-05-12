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
        self.card_font = pygame.font.SysFont("Segoe UI", 18, bold=True)
        self.card_bg = (60, 60, 60)
        self.card_bg_selected = (90, 90, 90)
        self.card_text = (240, 240, 240)
        self.card_border = (120, 120, 120)
        self.panel_width = 240
        self.last_hand_start_y = None

    def draw(
        self,
        screen,
        selected=None,
        turn=None,
        status_lines=None,
        moves=None,
        hand=None,
        selected_card_index=None,
        show_play=False,
    ):
        self._draw_status(screen, turn)
        panel_y = self._draw_side_panel(screen, status_lines, moves)
        self._draw_hand(screen, hand, selected_card_index, show_play, panel_y)
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

    def _draw_status(self, screen, turn):
        y = 10
        if turn:
            label = self.status_font.render(f"Turn: {turn}", True, (230, 230, 230))
            screen.blit(label, (self.margin, y))
            y += 22

    def _draw_side_panel(self, screen, status_lines, moves):
        y = self.margin
        if not status_lines and not moves:
            return y

        max_lines = 12
        x = self.margin + self.board.size * self.cell_size + 10

        if status_lines:
            title = self.status_font.render("Status", True, (230, 230, 230))
            screen.blit(title, (x, y))
            y += 22
            for line in status_lines:
                label = self.status_font.render(line, True, (230, 230, 230))
                screen.blit(label, (x, y))
                y += 20
            y += 10

        if not moves:
            return y

        recent = moves[-max_lines:]
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

        return y

    def _draw_hand(self, screen, hand, selected_card_index, show_play, start_y):
        if not hand:
            self.last_hand_start_y = None
            return

        x = self.margin + self.board.size * self.cell_size + 10
        y = start_y + 20

        title = self.status_font.render("Hand", True, (230, 230, 230))
        screen.blit(title, (x, y))
        y += 22

        self.last_hand_start_y = y

        card_rects, play_rect = self._hand_layout(y, len(hand))
        for idx, card in enumerate(hand):
            rect = card_rects[idx]
            is_selected = idx == selected_card_index
            bg = self.card_bg_selected if is_selected else self.card_bg
            pygame.draw.rect(screen, bg, rect)
            pygame.draw.rect(screen, self.card_border, rect, 1)
            label = self.card_font.render(str(card), True, self.card_text)
            label_rect = label.get_rect(midleft=(rect.x + 8, rect.centery))
            screen.blit(label, label_rect)

        if show_play and play_rect:
            pygame.draw.rect(screen, (80, 110, 80), play_rect)
            pygame.draw.rect(screen, self.card_border, play_rect, 1)
            label = self.card_font.render("Play", True, self.card_text)
            label_rect = label.get_rect(center=play_rect.center)
            screen.blit(label, label_rect)

    def _hand_layout(self, start_y, count):
        if count <= 0:
            return [], None

        x = self.margin + self.board.size * self.cell_size + 10
        card_w = self.panel_width - 20
        card_h = 40
        gap = 8
        rects = []
        for i in range(count):
            y = start_y + i * (card_h + gap)
            rects.append(pygame.Rect(x, y, card_w, card_h))

        play_y = start_y + count * (card_h + gap) + 10
        play_rect = pygame.Rect(x, play_y, card_w, 32)
        return rects, play_rect

    def card_at_pos(self, pos, hand_count, start_y):
        rects, _ = self._hand_layout(start_y, hand_count)
        for idx, rect in enumerate(rects):
            if rect.collidepoint(pos):
                return idx
        return None

    def play_button_hit(self, pos, hand_count, start_y):
        _, play_rect = self._hand_layout(start_y, hand_count)
        if play_rect and play_rect.collidepoint(pos):
            return True
        return False

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
