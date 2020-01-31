from deck import Deck
from dealer import Dealer
from auto_player import Player


def logic(dealer, player, possible_split):
    face_up = dealer.hand.hand[0]
    score = player.hand.hand_value()
    soft = player.hand.hand_is_soft()
    first_card = player.hand.hand[0]
    if possible_split:
        if first_card == 'A':
            return 'split'
        elif first_card in ['10', 'J', 'Q', 'K']:
            return 's'
        elif first_card == '9':
            if face_up in ['7', '10', 'J', 'Q', 'K']:
                return 's'
            else:
                return 'split'
        elif first_card == '8':
            return 'split'
        elif first_card in ['7', '2', '3']:
            if face_up in ['2', '3', '4', '5', '6', '7']:
                return 'split'
            else:
                return 'h'
        elif first_card == '6':
            if face_up in ['2', '3', '4', '5', '6']:
                return 'split'
            else:
                return 'h'
        elif first_card == '5':
            if face_up in ['10', 'J', 'Q', 'K', 'A']:
                return 'h'
            else:
                return 'd'
        else:
            if face_up in ['5', '6']:
                return 'split'
            else:
                return 'h'

    if soft:  # soft cases
        if score-11 == 9:
            return 's'
        elif score-11 == 8:
            if face_up == '6':
                return 'd'
            else:
                return 's'
        elif score-11 == 7:
            if face_up in ["2", "3", "4", "5", "6"]:
                return 'd'
            elif face_up in ["7", "8"]:
                return 's'
            else:
                return 'h'
        elif score-11 == 6:
            if face_up in ['3', '4', '5', '6']:
                return 'd'
            else:
                return 'h'
        elif score-11 == 5 or score-11 == 4:
            if face_up in ['4','5','6']:
                return 'd'
            else:
                return 'h'
        elif score-11 == 3 or score-11 == 2:
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


def split_possible(player):
    first = player.hand.hand[0]
    second = player.hand.hand[1]

    return first == second or (first in ['10', 'J', 'Q', 'K'] and second in ['10', 'J', 'Q', 'K'])


# noinspection DuplicatedCode,DuplicatedCode
def gameplay(percentage):

    player = Player(1000)
    dealer = Dealer()

    wins = 0
    losses = 0
    ties = 0
    blackjacks = 0

    deck = Deck()
    deck.shuffle()

    while True:
        game_ended = False

        deck.check_reshuffle()

        player.hand.add_card(deck.draw())
        player.hand.add_card(deck.draw())

        dealer.hand.add_card(deck.draw())
        dealer.hand.add_card(deck.draw())

        #  bet = player.place_bet()
        bet = 1
        player.balance -= bet

        score = player.hand.hand_value()
        deal_score, soft17 = dealer.hand.hand_value()

        if dealer.hand.hand[0] == 'A' and deal_score == 21:
            if score == 21:
                ties += 1
                player.balance += bet
            else:
                losses += 1
            if player.balance <= 1:
                break
            else:
                player = Player(player.balance)
                dealer = Dealer()
                continue

        elif score == 21:  # check for blackjack
            if deal_score == 21:  # only case where that could be a draw
                ties += 1
                player.balance += bet
            else:
                player.balance += 2.5*bet
                blackjacks += 1
            if player.balance <= 1:
                break
            else:
                player = Player(player.balance)
                dealer = Dealer()
                continue

        else:  # UNDER case player turn

            if split_possible(player) and 'split' == logic(dealer, player, True) and player.balance >= 4:
                player.balance -= bet
                player.split_hand()
                bets = list()
                scores = list()
                game_status = list()
                for hand in player.hands:
                    hand.add_card(deck.draw())
                    ans = logic(dealer, player, False)
                    if ans == 'd':
                        player.balance -= bet
                        bet = 2 * bet
                        hand.add_card(deck.draw())
                        score = hand.hand_value()
                        if score > 21:
                            losses += 1
                            game_ended = True
                        elif score == 21:
                            game_ended = False
                    elif ans == 's':
                        game_ended = False
                    else:
                        while ans == 'h' or ans == 'd':
                            hand.add_card(deck.draw())
                            score = hand.hand_value()
                            if score > 21:
                                losses += 1
                                game_ended = True
                                break
                            elif score == 21:
                                game_ended = False
                                break
                            ans = logic(dealer, player, False)

                    scores.append(score)
                    game_status.append(game_ended)
                    bets.append(bet)

                for k, hand in enumerate(player.hands):
                    game_ended = game_status[k]
                    score = scores[k]
                    bet = bets[k]
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
                            player.balance += 2 * bet

                        elif deal_score == score:
                            ties += 1
                            player.balance += bet

                        else:
                            losses += 1

                if player.balance <= 1:
                    break
                else:
                    player = Player(player.balance)
                    dealer = Dealer()
                    continue

            else:

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
                        ans = logic(dealer, player, False)

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

            if player.balance <= 1:
                break
            else:
                player = Player(player.balance)
                dealer = Dealer()

    return wins, losses, ties, blackjacks


def run_gameplay(it):
    i = 0
    wins = []
    losses = []
    ties = []
    blackjacks = []

    while i < it:
        win, loss, tie, blackjack = gameplay(0.01)
        i += 1
        wins.append(win)
        losses.append(loss)
        ties.append(tie)
        blackjacks.append(blackjack)

    return wins, losses, ties, blackjacks


if __name__ == '__main__':
    from multiprocessing import Pool
    N = 12  # iterations
    P = 4  # thread

    p = Pool(P)
    results = p.imap(run_gameplay, [N//P]*P)
    wins = []
    losses = []
    ties = []
    blackjacks = []
    for obj in results:
        count = 0
        for ob in obj:
            if count % 4 == 0:
                for i in ob:
                    wins.append(i)
                count += 1
            elif count % 4 == 1:
                for i in ob:
                    losses.append(i)
                count += 1
            elif count % 4 == 2:
                for i in ob:
                    ties.append(i)
                count += 1
            else:
                for i in ob:
                    blackjacks.append(i)
                count += 1

    file = open('simple_logic.txt', 'w')

    for i in range(0, len(wins)):
        win = wins[i]
        loss = losses[i]
        tie = ties[i]
        blackjack = blackjacks[i]
        file.write(f'{win}\t{loss}\t{tie}\t{blackjack}\t{win + loss + tie + blackjack}\n')

    file.close()
