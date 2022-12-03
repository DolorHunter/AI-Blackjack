from Blackjack_helper import *


def main():
    p = Poker()
    p.shuffle()
    dealer = Player()
    player = Player()

    initial_state(p, dealer, player)
    print('dealer： %s' % dealer.str_cards_on_hand)
    print('playerhand： %s' % player.str_cards_on_hand)

    while player.is_alive and dealer.is_alive:
        if not player.is_stop and p._turn:
            choice(p, player, False)
            p._turn = not p._turn
        elif not dealer.is_stop:
            choice(p, dealer, True)
            p._turn = not p._turn
        else:
            # cmp
            print('Dealer point：%s \n Player point：%s' % (dealer.point_count(), player.point_count()))
            if dealer.point_count() > player.point_count():
                print('Dealer win')
                return 0
            elif dealer.point_count() < player.point_count():
                print('Player win')
                return 1
            else:
                print('Tie')
                return 0
    else:
        if not player.is_alive:
            print('Player Blast , Dealer win')
            return -1
        else:
            print('Dealer blast, Player win ')
            return 1


if __name__ == '__main__':
    main()
