import random

BLASTPOINT = 21
DEALERBLAST = 17

class Card(object):
    # 1 card

    def __init__(self, suite, face):
        self._face = face
        self._suite = suite

    @property
    def face(self):
        return self._face

    def __str__(self):
        return '%s%s' % (self._suite, self._face)


all_cards = [Card(suite, face)
             for suite in '♠♥♣♦'
             for face in list(range(2, 14)) + ['A', 'J', 'Q', 'K']]


class Poker(object):
    
    #one deck 
    def __init__(self):
        self._cards = [Card(suite, face)
                       for suite in '♠♥♣♦'
                       for face in list(range(2, 11)) + ['A', 'J', 'Q', 'K']]
        self._current = 0
        self._turn = True

    @property
    def cards(self):
        return self._cards

    def shuffle(self):
        
        self._current = 0
        random.shuffle(self._cards)

    @property
    def next(self):
        card = self._cards[self._current]
        self._current += 1
        return card

    @property
    def has_next(self):
        
        return self._current < len(self._cards)


class Player(object):

    def __init__(self):
        self._cards_on_hand = []
        self._point = 0
        self._is_alive = True
        self._is_stop = False

    @property
    def name(self):
        return self.name

    @property
    def cards_on_hand(self):
        return self._cards_on_hand

    @property
    def point(self):
        return self._point

    @property
    def is_alive(self):
        return self._is_alive

    @property
    def is_stop(self):
        return self._is_stop

    @property
    def str_cards_on_hand(self):
        card_list = [str(i) for i in self.cards_on_hand]
        return ' '.join(card_list)

    def point_count(self):
        self._point = 0
        has_ace = False
        for k in self.cards_on_hand:
            if k.face == 'J' or k.face == 'Q' or k.face == 'K':
                k_count = 10
            elif k.face == 'A':
                has_ace = True
                k_count = 1
            else:
                k_count = int(k.face)
            self._point += k_count
        if has_ace is True:
            if self._point + 10 <= BLASTPOINT:
                self._point = self._point + 10
        if self.point > BLASTPOINT:
            self._is_alive = False
        return self._point

    def get(self, card):
        self._cards_on_hand.append(card)
        self.point_count()

    def arrange(self, card):
        self._cards_on_hand.sort(key=card.face)


def initial_state(p, dealer, player):
    dealer.get(p.next)
    dealer.get(p.next)
    player.get(p.next)
    player.get(p.next)
    return p, dealer, player


def choice(poker, player, is_dealer):
    role = 'Dealer' if is_dealer else 'Player'
    inp = input(role + ' action：\n Hit(H) Stop(S) \n')
    if inp == 'H':
        player.get(poker.next)
        print(role + ' get %s On hands\n %s' % (player.cards_on_hand[-1], player.str_cards_on_hand))
    elif inp == 'S':
        player._is_stop = True
        print(role + ' stop')
    else:
        print(role + ' error')
        choice(poker, player, is_dealer)
