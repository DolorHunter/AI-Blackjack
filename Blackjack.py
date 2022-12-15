import Blackjack_baseline
from Blackjack_helper import *
from Blackjack_manual import *
from Blackjack_baseline import *
from Blackjack_MCTS import *
from Blackjack_NN import *


BLASTPOINT = 21
STRATEGY = [manual, baseline, MCTS, NN]

def main():
    inp = input("Input Blast Point (defalut 21): ")
    blast_point = int(inp) if inp else BLASTPOINT

    strategies = []
    for i, role in enumerate(["Player", "Dealer"]):
        cur_strategy = -1
        while cur_strategy < 1 or cur_strategy > 4:
            cur_strategy = int(input("""
Input Strategy for {} (Player {})
1. Manual
2. Baseline
3. MCTS
4. NN
""").format(role, i+1))
        strategies.append(cur_strategy-1)

    player_stategy = STRATEGY[strategies[0]]
    dealer_stategy = STRATEGY[strategies[1]]

    p = Poker()
    p.shuffle()
    dealer = Player(blast_point)
    player = Player(blast_point)

    initial_state(p, dealer, player)
    print('dealer： %s' % dealer.str_cards_on_hand)
    print('playerhand： %s' % player.str_cards_on_hand)

    while player.is_alive and dealer.is_alive:
        if not player.is_stop and p._turn:  # p1 not stop
            player_stategy(p, player, dealer, False)
            p._turn = not p._turn
        elif not dealer.is_stop:  # p1 stop, p2 not stop
            dealer_stategy(p, player, dealer, True)
            p._turn = not p._turn
        else:  # p1, p2 stop
            # cmp
            print('Dealer point：%s \n Player point：%s' % (dealer.point_count(), player.point_count()))
            if dealer.point_count() > player.point_count():
                print('Dealer win')
                return -1
            elif dealer.point_count() < player.point_count():
                print('Player win')
                return 1
            else:
                print('Tie')
                return 0
    else:  # p1 or p2 lost
        if not player.is_alive:
            print('Player Blast , Dealer win')
            return -1
        else:
            print('Dealer blast, Player win ')
            return 1


if __name__ == '__main__':
    main()
