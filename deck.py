import random


class Deck():

    def __init__(self):
        self.cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']*4

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

# add reset function?
