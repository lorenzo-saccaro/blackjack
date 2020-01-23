class Dealer:
    def __init__(self):
        self.hand = self.Hand()  # analizza comportamento

    def show_hand(self, hidden=False):
        self.hand.print_hand(hidden)

    class Hand:

        values = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                  '10': 10, 'J': 10, 'Q': 10, 'K': 10}

        def __init__(self):
            self.hand = list()

        def add_card(self, card):
            self.hand.append(card)

        # noinspection DuplicatedCode
        def hand_value(self):
            soft = False
            value = 0
            aces = 0
            for card in self.hand:
                value += self.values[card]
                if card == 'A':
                    aces += 1
            while aces > 0 and value > 21:
                value -= 10
                aces -= 1
            if value == 17 and aces > 0:
                soft = True
            return value, soft

        def print_hand(self, hidden):
            cards = ''
            for index, card in enumerate(self.hand):
                if hidden and index == 1:
                    card = 'X'
                cards += card + " "

            print("Dealer's hand: " + cards)
