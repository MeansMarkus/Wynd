from cards.card import Card


class NumberCard(Card):
    def __init__(self, number):
        self.number = number
        self.name = str(number)

    def apply(self, game_state, player):
        game_state.moves_left = self.number
