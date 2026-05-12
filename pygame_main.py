import sys

import pygame

from cards.card import Deck
from cards.plus_two import PlusTwoCard
from cards.reverse import ReverseCard
from game.board import Board
from game.game_state import GameState
from game.turn_manager import TurnManager
from players.player import Player
from ui.renderer import Renderer


def build_deck():
    cards = []
    cards.extend(ReverseCard() for _ in range(4))
    cards.extend(PlusTwoCard() for _ in range(4))
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
    window_height = renderer.margin * 2 + board_pixels
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Chaos Chess")

    clock = pygame.time.Clock()
    running = True
    selected = None
    selected_card_index = None
    card_animation = None
    turn_started = True

    while running:
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
            if is_checkmate:
                continue
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                hand_start_y = renderer.last_hand_start_y
                if hand_start_y is not None and renderer.play_button_hit(
                    event.pos, len(player.hand), hand_start_y
                ):
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

                card_index = None
                if hand_start_y is not None:
                    card_index = renderer.card_at_pos(event.pos, len(player.hand), hand_start_y)
                if card_index is not None:
                    if selected_card_index == card_index:
                        selected_card_index = None
                    else:
                        selected_card_index = card_index
                    continue

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
                        state.moves_left -= 1
                        if state.moves_left <= 0:
                            turn_manager.advance()
                            turn_started = True
                    except ValueError:
                        pass
                    selected = None

        status_lines = []
        status_lines.append(f"Legal moves: {board.count_legal_moves(turn)}")
        status_lines.append(f"Moves left: {state.moves_left}")
        if is_checkmate:
            winner = "white" if turn == "black" else "black"
            status_lines.append(f"Checkmate: {winner} wins")
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

        renderer.draw(
            screen,
            selected=selected,
            turn=turn,
            status_lines=status_lines,
            moves=board.move_history,
            hand=player.hand,
            selected_card_index=selected_card_index,
            show_play=True,
            animation=animation_payload,
        )
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
