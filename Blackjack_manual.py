from Blackjack_helper import *


def manual(poker, player, dealer, is_dealer):
    role = 'Dealer' if is_dealer else 'Player'
    cur_player = player if not is_dealer else dealer
    inp = input(role + ' action：\n Hit(H) Stop(S) \n')
    if inp == 'H':
        cur_player.get(poker.next)
        print(role + ' get %s On hands\n %s' % (player.cards_on_hand[-1], player.str_cards_on_hand))
    elif inp == 'S':
        cur_player._is_stop = True
        print(role + ' stop')
    else:
        print(role + ' error')
        manual(poker, player, dealer, is_dealer)