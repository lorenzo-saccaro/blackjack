# six decks setup
# reshuffle after 70-85% is drawn

import random


class Deck():

    def __init__(self):
        self.cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']*24
        self.fraction = random.uniform(0.7,0.85)
        self.total_cards = len(self.cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

    def check_reshuffle(self):
        if len(self.cards) < (1.0-self.fraction)*self.total_cards:
            self.cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']*24
            self.shuffle()
            self.fraction = random.uniform(0.7,0.85)

# add reset function?
