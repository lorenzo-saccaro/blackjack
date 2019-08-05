class Player():
    def __init__(self, balance):
        self.balance = balance
        self.hand = self.Hand()  # analizza comportamento

    def place_bet(self):
        try:
            bet = int(input('Insert the bet ammount: '))
            if bet < 0:
                raise ValueError
            if self.balance - bet < 0:
                raise ArithmeticError
        except ArithmeticError:
            print('Not enough money')
            self.place_bet()
        except ValueError:
            print('Please insert only a positive ammount')
            self.place_bet()
        else:
            self.balance -= bet
            return bet

    def hit_or_stay(self):
        hit = set(['h', 'hit', 'Hit'])
        stay = set(['s', 'stay', 'Stay'])

        while True:
            ans = input('Hit or Stay? ')
            if ans in hit:
                return 'hit'
            elif ans in stay:
                return 'stay'
            else:
                continue

    def show_hand(self):
        self.hand.print_hand()

    class Hand():

        values = {'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                  '10': 10, 'J': 10, 'Q': 10, 'K': 10}

        def __init__(self):
            self.hand = list()

        def add_card(self, card):
            self.hand.append(card)

        def hand_value(self):
            value = 0
            aces = 0
            for card in self.hand:
                value += self.values[card]
                if card == 'A':
                    aces += 1
            while (aces > 0 and value > 21):
                value -= 10
                aces -= 1
            return value

        def print_hand(self):
            cards = ''
            for card in self.hand:
                cards += card + " "

            print("Player's hand: " + cards)
