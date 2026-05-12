from cards.card import Deck
from cards.number import NumberCard
from cards.plus_two import PlusTwoCard
from cards.reverse import ReverseCard
from game.board import Board
from game.game_manager import GameManager
from game.game_state import GameState
from game.turn_manager import TurnManager
from players.player import Player


def build_deck():
    cards = []
    cards.extend(ReverseCard() for _ in range(2))
    cards.extend(PlusTwoCard() for _ in range(3))
    for number in range(1, 6):
        cards.extend(NumberCard(number) for _ in range(2))
    return Deck(cards)


def main():
    board = Board()
    board.setup_initial()

    players = [Player("White", "white"), Player("Black", "black")]
    turn_manager = TurnManager(players)
    deck = build_deck()

    for player in players:
        player.draw(deck, count=3)

    state = GameState(board, players, turn_manager, deck)
    manager = GameManager(state)
    manager.run()


if __name__ == "__main__":
    main()
        