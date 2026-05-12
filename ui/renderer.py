import pygame


class Renderer:
    def __init__(self, board, cell_size=80, margin=40):
        self.board = board
        self.cell_size = cell_size
        self.margin = margin
        self.tray_height = 140
        self.top_bar_height = 28
        self.dark = (118, 150, 86)
        self.light = (238, 238, 210)
        self.grid = (30, 30, 30)
        self.highlight = (246, 246, 105)
        self.hover = (220, 220, 140)
        self.check = (220, 80, 80)
        self.white_piece = (245, 245, 245)
        self.black_piece = (30, 30, 30)
        self.outline = (15, 15, 15)
        self.font = pygame.font.SysFont("Segoe UI", 36, bold=True)
        self.status_font = pygame.font.SysFont("Segoe UI", 20, bold=True)
        self.card_font = pygame.font.SysFont("Segoe UI", 18, bold=True)
        self.banner_font = pygame.font.SysFont("Segoe UI", 28, bold=True)
        self.card_bg = (60, 60, 60)
        self.card_bg_selected = (90, 90, 90)
        self.card_text = (240, 240, 240)
        self.card_border = (120, 120, 120)
        self.panel_width = 240
        self.last_hand_start_y = None
        self.last_tray_rects = []
        self.last_play_rect = None
        self.side_panel_top_pad = 120

    def draw(
        self,
        screen,
        selected=None,
        hover_square=None,
        turn=None,
        status_lines=None,
        moves=None,
        hand=None,
        opponent_hand_count=0,
        selected_card_index=None,
        hover_card_index=None,
        show_play=False,
        animation=None,
        deck_count=0,
        discard_top=None,
        check_color=None,
        checkmate=False,
        board_offset=(0, 0),
    ):
        self._draw_status(screen, turn)
        self._draw_deck_discard(screen, deck_count, discard_top)
        panel_y = self._draw_side_panel(screen, status_lines, moves)
        self._draw_tray(
            screen,
            hand,
            opponent_hand_count,
            selected_card_index,
            hover_card_index,
            show_play,
        )
        self._draw_card_animation(screen, animation)
        board_size = self.board.size
        for row in range(board_size):
            for col in range(board_size):
                x = self.margin + col * self.cell_size + board_offset[0]
                y = self.margin + row * self.cell_size + board_offset[1]
                is_dark = (row + col) % 2 == 1
                color = self.dark if is_dark else self.light
                if selected == (row, col):
                    color = self.highlight
                elif hover_square == (row, col):
                    color = self.hover
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

        if check_color:
            self._draw_check_highlight(screen, check_color, board_offset)
        if checkmate:
            self._draw_checkmate_banner(screen, checkmate)

    def _draw_status(self, screen, turn):
        y = 10
        if turn:
            label = self.status_font.render(f"Turn: {turn}", True, (230, 230, 230))
            screen.blit(label, (self.margin, y))
            y += 22

    def _draw_side_panel(self, screen, status_lines, moves):
        y = self.margin + self.side_panel_top_pad
        if not status_lines and not moves:
            return y

        max_lines = 12
        x = self._side_panel_x()

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

    def _draw_tray(
        self,
        screen,
        hand,
        opponent_hand_count,
        selected_card_index,
        hover_card_index,
        show_play,
    ):
        tray_top = self.margin + self.board.size * self.cell_size + 10
        tray_left = self.margin
        tray_width = self.board.size * self.cell_size
        tray_rect = pygame.Rect(tray_left, tray_top, tray_width, self.tray_height - 20)
        pygame.draw.rect(screen, (25, 25, 25), tray_rect)
        pygame.draw.rect(screen, self.grid, tray_rect, 1)

        title = self.status_font.render("Hand", True, (230, 230, 230))
        screen.blit(title, (tray_left + 10, tray_top + 8))

        self.last_tray_rects = []
        self.last_play_rect = None
        if not hand:
            return

        card_count = len(hand)
        available_width = tray_width - 20
        card_w = min(100, max(64, (available_width - 10) // max(1, card_count)))
        card_h = 64
        gap = 8
        total_width = card_count * card_w + (card_count - 1) * gap
        start_x = tray_left + (tray_width - total_width) // 2
        card_y = tray_top + 40

        for idx, card in enumerate(hand):
            x = start_x + idx * (card_w + gap)
            rect = pygame.Rect(x, card_y, card_w, card_h)
            if idx == selected_card_index:
                rect = rect.move(0, -6)
            self.last_tray_rects.append(rect)

            is_selected = idx == selected_card_index
            is_hover = idx == hover_card_index
            bg = self.card_bg_selected if is_selected else self.card_bg
            if is_hover:
                bg = (bg[0] + 10, bg[1] + 10, bg[2] + 10)
            pygame.draw.rect(screen, bg, rect)
            pygame.draw.rect(screen, self.card_border, rect, 1)
            label = self.card_font.render(str(card), True, self.card_text)
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

        if show_play:
            play_w = 80
            play_h = 32
            play_x = tray_left + tray_width - play_w - 12
            play_y = tray_top + 8
            self.last_play_rect = pygame.Rect(play_x, play_y, play_w, play_h)
            pygame.draw.rect(screen, (80, 110, 80), self.last_play_rect)
            pygame.draw.rect(screen, self.card_border, self.last_play_rect, 1)
            label = self.card_font.render("Play", True, self.card_text)
            label_rect = label.get_rect(center=self.last_play_rect.center)
            screen.blit(label, label_rect)

        if opponent_hand_count:
            back_w = 28
            back_h = 40
            opp_x = tray_left + 10
            opp_y = tray_top + 8
            for i in range(min(opponent_hand_count, 8)):
                rect = pygame.Rect(opp_x + i * 8, opp_y, back_w, back_h)
                pygame.draw.rect(screen, (70, 70, 90), rect)
                pygame.draw.rect(screen, self.card_border, rect, 1)
            count_label = self.card_font.render(
                f"Opponent: {opponent_hand_count}", True, (200, 200, 200)
            )
            screen.blit(count_label, (opp_x + 8 * 8 + 8, opp_y + 10))

    def card_at_pos(self, pos):
        for idx, rect in enumerate(self.last_tray_rects):
            if rect.collidepoint(pos):
                return idx
        return None

    def play_button_hit(self, pos):
        return bool(self.last_play_rect and self.last_play_rect.collidepoint(pos))

    def _draw_deck_discard(self, screen, deck_count, discard_top):
        x = self._side_panel_x()
        y = self.margin + 10

        deck_rect = pygame.Rect(x, y, 70, 90)
        discard_rect = pygame.Rect(x + 90, y, 70, 90)
        pygame.draw.rect(screen, (50, 50, 60), deck_rect)
        pygame.draw.rect(screen, self.card_border, deck_rect, 1)
        pygame.draw.rect(screen, (70, 60, 60), discard_rect)
        pygame.draw.rect(screen, self.card_border, discard_rect, 1)

        deck_label = self.card_font.render(f"Deck {deck_count}", True, self.card_text)
        screen.blit(deck_label, (x, y + 96))
        discard_label = self.card_font.render("Discard", True, self.card_text)
        screen.blit(discard_label, (x + 90, y + 96))

        if discard_top:
            card_label = self.card_font.render(str(discard_top), True, self.card_text)
            card_rect = card_label.get_rect(center=discard_rect.center)
            screen.blit(card_label, card_rect)

    def _side_panel_x(self):
        return self.margin + self.board.size * self.cell_size + 10

    def _draw_check_highlight(self, screen, color, board_offset):
        king_pos = self.board.find_king(color)
        if not king_pos:
            return
        row, col = king_pos
        x = self.margin + col * self.cell_size + board_offset[0]
        y = self.margin + row * self.cell_size + board_offset[1]
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, self.check, rect, 3)

    def _draw_checkmate_banner(self, screen, text):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        label = self.banner_font.render(text, True, (240, 240, 240))
        rect = label.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(label, rect)

    def _draw_card_animation(self, screen, animation):
        if not animation:
            return

        progress = max(0.0, min(1.0, animation.get("progress", 1.0)))
        name = animation.get("name", "")

        x = self.margin + self.board.size * self.cell_size + 10
        base_y = self.margin + 10
        y = base_y - int(20 * progress)
        rect = pygame.Rect(x, y, self.panel_width - 20, 48)

        alpha = int(255 * (1.0 - progress))
        surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        surface.fill((80, 80, 120, alpha))
        pygame.draw.rect(surface, (160, 160, 190, alpha), surface.get_rect(), 2)

        label = self.card_font.render(f"Played: {name}", True, (240, 240, 240))
        label.set_alpha(alpha)
        label_rect = label.get_rect(center=(rect.width / 2, rect.height / 2))
        surface.blit(label, label_rect)

        screen.blit(surface, rect.topleft)

    def square_from_mouse(self, pos, board_offset=(0, 0)):
        x, y = pos
        board_size = self.board.size
        x -= board_offset[0]
        y -= board_offset[1]
        if x < self.margin or y < self.margin:
            return None
        x -= self.margin
        y -= self.margin
        col = x // self.cell_size
        row = y // self.cell_size
        if 0 <= row < board_size and 0 <= col < board_size:
            return int(row), int(col)
        return None
