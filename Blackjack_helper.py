import random


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

    def __init__(self, blast_point):
        self._cards_on_hand = []
        self._point = 0
        self._is_alive = True
        self._is_stop = False
        self._blast_point = blast_point
        self._action = None
        self._score_estimate = 0

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
            if self._point + 10 <= self._blast_point:
                self._point = self._point + 10
        if self.point > self._blast_point:
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


def run_game(blast_point, player_stategy, dealer_stategy, silence_mode, is_auto):
    p = Poker()
    p.shuffle()
    dealer = Player(blast_point)
    player = Player(blast_point)

    initial_state(p, dealer, player)
    print('dealer： %s' % dealer.str_cards_on_hand) if not silence_mode else None
    print('playerhand： %s' % player.str_cards_on_hand) if not silence_mode else None

    dealer_node_ct, player_node_ct = [], []
    dealer_node_score, player_node_score = 0, 0

    while player.is_alive and dealer.is_alive:
        if not dealer.is_stop and p._turn:  # p1 not stop
            ret1 = dealer_stategy(p, player, dealer, True, is_auto)
            if ret1:
                node_ct, dealer_node_score = ret1
                dealer_node_ct.append(node_ct)
            p._turn = not p._turn
        elif not player.is_stop:  # p1 stop, p2 not stop
            ret2 = player_stategy(p, player, dealer, False, is_auto)
            if ret2:
                node_ct, player_node_score = ret2
                player_node_ct.append(node_ct)
            p._turn = not p._turn
        else:  # p1, p2 stop
            # cmp
            print('Dealer point：%s \n Player point：%s' % (dealer.point_count(), player.point_count())) if not silence_mode else None
            if dealer.point_count() > player.point_count():
                print('Dealer win. Dealer Score: 1. Player Score: -1.') if not silence_mode else None
                return 1, sum(dealer_node_ct), sum(player_node_ct), dealer_node_score, player_node_score
            elif dealer.point_count() < player.point_count():
                print('Player win. Dealer Score: -1. Player Score: 1.') if not silence_mode else None
                return -1, sum(dealer_node_ct), sum(player_node_ct), dealer_node_score, player_node_score
            else:
                print('Tie. Dealer Score: 0. Player Score: 0.') if not silence_mode else None
                return 0, sum(dealer_node_ct), sum(player_node_ct), dealer_node_score, player_node_score
    else:  # p1 or p2 lost
        if not player.is_alive:
            print('Player Blast, Dealer win. Dealer Score: 1. Player Score: -1.') if not silence_mode else None
            return 1, sum(dealer_node_ct), sum(player_node_ct), dealer_node_score, player_node_score
        else:
            print('Dealer blast, Player win. Dealer Score: -1. Player Score: 1.') if not silence_mode else None
            return -1, sum(dealer_node_ct), sum(player_node_ct), dealer_node_score, player_node_score
