from Blackjack_helper import *


def baseline(poker, player, dealer, is_dealer):
    role = 'Dealer' if is_dealer else 'Player'
    cur_player = player if not is_dealer else dealer
    dealer_blast = cur_player._blast_point - 4
    if cur_player.point < dealer_blast:
        cur_player.get(poker.next)
        print(role + ' get %s On hands\n %s' % (cur_player.cards_on_hand[-1],
                                                cur_player.str_cards_on_hand))
    else:
        cur_player._is_stop = True
    print(role + ' stop.')
