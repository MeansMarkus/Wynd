import sys

import pygame

from cards.card import Deck
from cards.number import NumberCard
from cards.plus_two import PlusTwoCard
from cards.reverse import ReverseCard
from game.board import Board
from game.game_state import GameState
from game.turn_manager import TurnManager
from players.player import Player
from ui.renderer import Renderer


def build_deck():
    cards = []
    cards.extend(ReverseCard() for _ in range(2))
    cards.extend(PlusTwoCard() for _ in range(3))
    for number in range(1, 6):
        cards.extend(NumberCard(number) for _ in range(2))
    return Deck(cards)


def main():
    pygame.init()

    board = Board()
    board.setup_initial()
    renderer = Renderer(board)

    players = [Player("White", "white"), Player("Black", "black")]
    turn_manager = TurnManager(players)
    deck = build_deck()
    state = GameState(board, players, turn_manager, deck)

    board_pixels = board.size * renderer.cell_size
    window_width = renderer.margin * 2 + board_pixels + renderer.panel_width
    window_height = renderer.margin * 2 + board_pixels + renderer.tray_height
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Chaos Chess")

    clock = pygame.time.Clock()
    running = True
    selected = None
    hover_square = None
    selected_card_index = None
    hover_card_index = None
    card_animation = None
    shake_until = 0
    turn_started = True

    while running:
        now = pygame.time.get_ticks()
        shake_offset = (0, 0)
        if now < shake_until:
            phase = (shake_until - now) / 250.0
            shake_x = int(6 * phase) * (-1 if (now // 50) % 2 == 0 else 1)
            shake_offset = (shake_x, 0)
        board_offset = shake_offset

        player = turn_manager.current_player()
        turn = player.color
        is_checkmate = board.is_checkmate(turn)
        if turn_started:
            if len(player.hand) < 5:
                player.draw(deck)
            state.moves_left = 1
            turn_started = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                print(board.to_fen(turn))
            if event.type == pygame.MOUSEMOTION:
                hover_square = renderer.square_from_mouse(event.pos, board_offset=board_offset)
                hover_card_index = renderer.card_at_pos(event.pos)
            if is_checkmate:
                continue
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if renderer.play_button_hit(event.pos):
                    if selected_card_index is not None:
                        try:
                            card = player.play_card(selected_card_index, state)
                            card_animation = {
                                "name": str(card),
                                "start": pygame.time.get_ticks(),
                                "duration": 900,
                            }
                        except ValueError:
                            pass
                        selected_card_index = None
                        selected = None
                        continue

                card_index = renderer.card_at_pos(event.pos)
                if card_index is not None:
                    if selected_card_index == card_index:
                        selected_card_index = None
                    else:
                        selected_card_index = card_index
                    continue

                clicked = renderer.square_from_mouse(event.pos, board_offset=board_offset)
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
                        state.moves_left -= 1
                        if state.moves_left <= 0:
                            turn_manager.advance()
                            turn_started = True
                    except ValueError:
                        shake_until = pygame.time.get_ticks() + 250
                    selected = None

        status_lines = []
        status_lines.append(f"Legal moves: {board.count_legal_moves(turn)}")
        status_lines.append(f"Moves left: {state.moves_left}")
        checkmate_text = None
        if is_checkmate:
            winner = "white" if turn == "black" else "black"
            checkmate_text = f"Checkmate: {winner} wins"
            status_lines.append(checkmate_text)
        elif board.is_in_check(turn):
            status_lines.append("Check")

        screen.fill((20, 20, 20))
        animation_payload = None
        if card_animation:
            elapsed = pygame.time.get_ticks() - card_animation["start"]
            if elapsed > card_animation["duration"]:
                card_animation = None
            else:
                animation_payload = {
                    "name": card_animation["name"],
                    "progress": elapsed / card_animation["duration"],
                }

        discard_top = deck.discard_pile[-1] if deck.discard_pile else None
        opponent = players[0] if player is players[1] else players[1]
        renderer.draw(
            screen,
            selected=selected,
            hover_square=hover_square,
            turn=turn,
            status_lines=status_lines,
            moves=board.move_history,
            hand=player.hand,
            opponent_hand_count=len(opponent.hand),
            selected_card_index=selected_card_index,
            hover_card_index=hover_card_index,
            show_play=True,
            animation=animation_payload,
            deck_count=len(deck.draw_pile),
            discard_top=discard_top,
            check_color=turn if board.is_in_check(turn) else None,
            checkmate=checkmate_text,
            board_offset=board_offset,
        )
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
