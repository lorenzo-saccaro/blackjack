import os
from deck import Deck
from player import Player
from dealer import Dealer


# ==================================================================================================
# da migliorare print delle mani con seme e punteggio e compattare gameplay logic
# implmentare regole avanzate, gestione dei mazzi  e più giocatori
# ==================================================================================================


def welcome():
    print('Welcome to Blackjack or 21!')
    print('The aim of the game is to get as close as possible to 21 without going over it.')
    print('Cards have their pip values while figures have value 10.')
    print('Aces can be 1 or 11 (choice is automatic).')
    print('Rules of the house: ')
    print('- The dealer has 1 card face up and 1 face down.')
    print('- The player has 2 cards face up, he can choose to hit (get a card) or stay.')
    print('- If he goes over 21 (BUST) the hand is over and he loses the bet.')
    print('- In case of 21 the player wins immediately')
    print('- Execption: if the 21 is dealt the dealer show his hands to see if he can tie the hand')
    print('- Otherwise the dealer has to hit until his score is at least 17.')
    print('- If the dealear\'s score is 17 with an ace with value 11, he has to hit.')
    print('- When the dealer stops hitting (if he has not busted), the higher value hand wins.')
    print('- If the hand ends with a tie the player gets his bet back, if he wins double of it')

    print('\n\n Future versions aim to implement actions such as split, double down and insurance')

    while True:
        try:
            buy_in = int(input('Insert the buyin ammount: $'))
            if buy_in < 0:
                raise ValueError
        except ValueError:
            print('Please insert only a positive ammount')
            continue
        else:
            return buy_in


def replay():
    while True:
        ans = input('Do you want to keep playing (y or n)? ')
        if ans == 'y':
            return True
        if ans == 'n':
            return False
        else:
            continue


def gameplay():

    player = Player(welcome())
    dealer = Dealer()

    while True:
        game_ended = False

        deck = Deck()
        deck.shuffle()

        player.hand.add_card(deck.draw())
        player.hand.add_card(deck.draw())

        dealer.hand.add_card(deck.draw())
        dealer.hand.add_card(deck.draw())

        bet = player.place_bet()

        dealer.show_hand(True)
        player.show_hand()
        print('\n')

        score = player.hand.hand_value()
        deal_score, soft17 = dealer.hand.hand_value()

        if score == 21:  # check for blackjack
            dealer.show_hand()
            player.show_hand()
            print('\n')
            if deal_score == 21:  # only case where that could be a draw
                print('Tie')
                player.balance += bet
            else:
                print('You win')
                player.balance += 2*bet
            game_ended = True

        else:  # UNDER case player turn
            ans = ''
            while not ans == 'stay':
                ans = player.hit_or_stay()
                if ans == 'hit':
                    player.hand.add_card(deck.draw())
                    dealer.show_hand(True)
                    player.show_hand()
                    print('\n')
                    score = player.hand.hand_value()
                    if score > 21:
                        print("BUST")
                        game_ended = True
                        break
                    elif score == 21:
                        print("You win")
                        player.balance += 2*bet
                        game_ended = True
                        break
                continue

        if not game_ended:  # dealer turn
            dealer.show_hand()
            player.show_hand()
            print('\n')
            while deal_score <= 17:
                while deal_score < 17:
                    dealer.hand.add_card(deck.draw())
                    dealer.show_hand()
                    player.show_hand()
                    print('\n')
                    deal_score, sof17 = dealer.hand.hand_value()
                if soft17:
                    dealer.hand.add_card(deck.draw())
                    dealer.show_hand()
                    player.show_hand()
                    print('\n')
                    deal_score, sof17 = dealer.hand.hand_value()
                else:
                    break
            if deal_score > 21 or score > deal_score:
                print("You win")
                player.balance += 2*bet

            elif deal_score == score:
                print('Tie')
                player.balance += bet

            else:
                print("You lose")

        print(f'Player balance now is: {player.balance}$')
        if player.balance <= 0:
            print('Game over: you are broke!')
            break
        else:
            if replay():
                player = Player(player.balance)
                dealer = Dealer()
            else:
                print(f'You left the table with {player.balance}$')
                break

    os.system('PAUSE')


if __name__ == '__main__':
    gameplay()
