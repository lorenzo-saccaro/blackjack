from deck import Deck
from dealer import Dealer
from auto_player import Player


def gameplay(percentage):

    # percentage = float(input('Insert percentage of balance to bet: '))
    # start_ammount = int(input('Insert start ammount: '))

    # player = Player(start_ammount)
    player = Player(100)
    dealer = Dealer()

    wins = 0
    losses = 0
    ties = 0

    while True:
        game_ended = False

        deck = Deck()
        deck.shuffle()

        player.hand.add_card(deck.draw())
        player.hand.add_card(deck.draw())

        dealer.hand.add_card(deck.draw())
        dealer.hand.add_card(deck.draw())

        bet = player.place_bet(percentage)

        # dealer.show_hand(True)
        # player.show_hand()
        # print('\n')

        score = player.hand.hand_value()
        deal_score, soft17 = dealer.hand.hand_value()

        if score == 21:  # check for blackjack
            # dealer.show_hand()
            # player.show_hand()
            # print('\n')
            if deal_score == 21:  # only case where that could be a draw
                # print('Tie')
                ties += 1
                player.balance += bet
            else:
                # print('You win')
                player.balance += 2*bet
                wins += 1
            game_ended = True

        else:  # UNDER case player turn
            while score <= 18:  # implement player strategy
                player.hand.add_card(deck.draw())
                # dealer.show_hand(True)
                # player.show_hand()
                # print('\n')
                score = player.hand.hand_value()
                if score > 21:
                    # print("BUST")
                    losses += 1
                    game_ended = True
                    break
                elif score == 21:
                    # print("You win")
                    player.balance += 2*bet
                    wins += 1
                    game_ended = True
                    break

        if not game_ended:  # dealer turn
            # dealer.show_hand()
            # player.show_hand()
            # print('\n')
            while deal_score <= 17:
                while deal_score < 17:
                    dealer.hand.add_card(deck.draw())
                    # dealer.show_hand()
                    # player.show_hand()
                    # print('\n')
                    deal_score, sof17 = dealer.hand.hand_value()
                if soft17:
                    dealer.hand.add_card(deck.draw())
                    # dealer.show_hand()
                    # player.show_hand()
                    # print('\n')
                    deal_score, sof17 = dealer.hand.hand_value()
                else:
                    break
            if deal_score > 21 or score > deal_score:
                # print("You win")
                wins += 1
                player.balance += 2*bet

            elif deal_score == score:
                # print('Tie')
                ties += 1
                player.balance += bet

            else:
                # print("You lose")
                losses += 1

        # print(f'Player balance now is: {player.balance}$')
        if player.balance < 1:
            # print('Game over: you are broke!')
            break
        else:
            player = Player(player.balance)
            dealer = Dealer()

    # print(f'{wins}\t{losses}\t{ties}\t{wins+losses+ties}')
    return wins, losses, ties


if __name__ == '__main__':
    file = open('simple_logic.txt', 'w')
    progress = 0
    for perc in range(1, 11):
        N = 0
        while N < 10000:
            wins, losses, ties = gameplay(0.01*perc)
            file.write(f'{wins}\t{losses}\t{ties}\t{wins+losses+ties}\n')
            N += 1
            if N % 100 == 1:
                progress += 1
                print('{:4.1f}%'.format(0.1*progress))
        file.write('#\t#\t#\t#')
    file.close()
