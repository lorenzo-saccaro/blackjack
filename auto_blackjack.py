from deck import Deck
from dealer import Dealer
from auto_player import Player


def logic(dealer, player, hit):
    face_up = dealer.hand.hand[0]
    cards = player.hand.hand
    score = player.hand.hand_value()
    if 'A' in cards and not hit:  # soft cases
        if '9' in cards:
            return 's'
        elif '8' in cards:
            if face_up == '6':
                return 'd'
            else:
                return 's'
        elif '7' in cards:
            if face_up in ["2", "3", "4", "5", "6"]:
                return 'd'
            elif face_up in ["7", "8"]:
                return 's'
            else:
                return 'h'
        elif '6' in cards:
            if face_up in ['3', '4', '5', '6']:
                return 'd'
            else:
                return 'h'
        elif '5' in cards or '4' in cards:
            if face_up in ['4','5','6']:
                return 'd'
            else:
                return 'h'
        elif '2' in cards or '3' in cards:
            if face_up in ['5','6']:
                return 'd'
            else:
                return 'h'
        else:
            return 'h'
    else:  # hard cases
        if 17 <= score <= 21:
            return 's'
        elif 13 <= score <= 16:
            if face_up in ['2', '3', '4', '5', '6']:
                return 's'
            else:
                return 'h'
        elif score == 12:
            if face_up in ['4', '5', '6']:
                return 's'
            else:
                return 'h'
        elif score == 11:
            return 'd'
        elif score == 10:
            if face_up in ['10', 'J', 'Q', 'K', 'A']:
                return 'h'
            else:
                return 'd'
        elif score == 9:
            if face_up in ['3', '4', '5', '6']:
                return 'd'
            else:
                return 'h'
        else:
            return 'h'


# noinspection DuplicatedCode,DuplicatedCode
def gameplay(percentage):

    player = Player(100)
    dealer = Dealer()

    wins = 0
    losses = 0
    ties = 0

    deck = Deck()
    deck.shuffle()

    while True:
        game_ended = False

        deck.check_reshuffle()

        player.hand.add_card(deck.draw())
        player.hand.add_card(deck.draw())

        dealer.hand.add_card(deck.draw())
        dealer.hand.add_card(deck.draw())

        bet = player.place_bet(percentage)

        score = player.hand.hand_value()
        deal_score, soft17 = dealer.hand.hand_value()

        if dealer.hand.hand[0] == 'A' and deal_score == 21:
            if score == 21:
                ties += 1
                player.balance += bet
            else:
                losses += 1
            game_ended = True

        elif score == 21:  # check for blackjack
            if deal_score == 21:  # only case where that could be a draw
                ties += 1
                player.balance += bet
            else:
                player.balance += 2.5*bet
                wins += 1
            game_ended = True

        else:  # UNDER case player turn
            ans = logic(dealer, player, False)
            if ans == 'd':
                player.balance -= bet
                bet = 2 * bet
                player.hand.add_card(deck.draw())
                score = player.hand.hand_value()
                if score > 21:
                    losses += 1
                    game_ended = True
                elif score == 21:
                    game_ended = False
            elif ans == 's':
                game_ended = False
            else:
                while ans == 'h' or ans == 'd':
                    player.hand.add_card(deck.draw())
                    score = player.hand.hand_value()
                    if score > 21:
                        losses += 1
                        game_ended = True
                        break
                    elif score == 21:
                        game_ended = False
                        break
                    ans = logic(dealer, player, True)

        if not game_ended:  # dealer turn
            while deal_score <= 17:
                while deal_score < 17:
                    dealer.hand.add_card(deck.draw())
                    deal_score, sof17 = dealer.hand.hand_value()
                if soft17:
                    dealer.hand.add_card(deck.draw())
                    deal_score, sof17 = dealer.hand.hand_value()
                else:
                    break
            if deal_score > 21 or score > deal_score:
                wins += 1
                player.balance += 2*bet

            elif deal_score == score:
                ties += 1
                player.balance += bet

            else:
                losses += 1

        if player.balance < 1:
            break
        else:
            player = Player(player.balance)
            dealer = Dealer()

    return wins, losses, ties


if __name__ == '__main__':
    file = open('simple_logic.txt', 'w')
    progress = 0
    max_iteration = 100
    max_range = 2
    for perc in range(1, max_range):
        N = 0
        while N < max_iteration:
            wins, losses, ties = gameplay(0.01*perc)
            file.write(f'{wins}\t{losses}\t{ties}\t{wins+losses+ties}\n')
            N += 1
            if N % 100 == 1:
                progress += 100/(max_iteration*len(range(1,max_range)))
                print('{:4.1f}%'.format(100*progress))
        file.write('#\t#\t#\t#')
    file.close()
