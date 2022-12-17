import numpy as np
import copy
from Blackjack_helper import *
from Blackjack_NN_helper import *

# 1 for dealer win; -1 for player win
def score(state):
    p, dealer, player = state
    if not player._is_alive:
        return 1
    if not dealer._is_alive:
        return -1

    if player._is_stop and dealer._is_stop:
        if player.point <= dealer.point:
            return -1
        else:
            return 1
    return 0


def get_player(state, is_turn):
    p, dealer, player = state
    p._turn = not p._turn if is_turn else p._turn
    return not p._turn  # true->dealer, false->player


def children_of(state):
    children = []
    cp_state = copy.deepcopy(state)
    p, dealer, player = cp_state
    if get_player(cp_state, True):
        if dealer.point <= dealer._blast_point:
            if not dealer._is_stop:
                # Hit
                cp_p, cp_dealer, cp_player = copy.deepcopy(cp_state)
                cp_dealer.get(cp_p.next)
                cp_dealer._action = 'H'
                children.append((cp_p, cp_dealer, cp_player))
            # Stop
            cp_p, cp_dealer, cp_player = copy.deepcopy(cp_state)
            cp_dealer._is_stop = True
            cp_dealer._action = 'S'
            children.append((cp_p, cp_dealer, cp_player))
    else:
        if player.point <= player._blast_point:
            if not player._is_stop:
                # Hit
                cp_p, cp_dealer, cp_player = copy.deepcopy(cp_state)
                cp_player.get(cp_p.next)
                cp_player._action = 'H'
                children.append((cp_p, cp_dealer, cp_player))
            # Stop
            cp_p, cp_dealer, cp_player = copy.deepcopy(cp_state)
            cp_player._is_stop = True
            cp_player._action = 'S'
            children.append((cp_p, cp_dealer, cp_player))
    return children


def is_leaf(state):
    children = children_of(state)
    value = score(state)
    return len(children) == 0 or value != 0


# MCTS to solve tic-tac-toe
# TODO: implement exploration strategy
class Node:
    def __init__(self, state):
        self.state = state
        self.visit_count = 0
        self.score_total = 0
        self.score_estimate = 0
        self.child_list = None
        self.action = None

    def children(self):
        # Only generate children the first time they are requested and memoize
        if self.child_list == None:
            self.child_list = list(map(Node, children_of(self.state)))
        # Return the memoized child list thereafter
        return self.child_list

    # Helper to collect child visit counts into a list
    def N_values(self):
        return [c.visit_count for c in self.children()]

    # Helper to collect child estimated utilities into a list
    # Utilities are from the current player's perspective
    def Q_values(self):
        children = self.children()

        # negate utilities for min player "O"
        sign = +1 if get_player(self.state, False) else -1

        # empirical average child utilities
        # special case to handle 0 denominator for never-visited children
        Q = [sign * c.score_total / (c.visit_count + 1) for c in children]
        # Q = [sign * c.score_total / max(c.visit_count, 1) for c in children]

        return Q


# exploit strategy: choose the best child for the current player
def exploit(node):
    return node.children()[np.argmax(node.Q_values())]


# explore strategy: choose the least-visited child
def explore(node):
    return node.children()[np.argmin(node.N_values())]  # TODO: replace with exploration


# upper-confidence bound strategy
def uct(node):
    # max_c Qc + sqrt(ln(Np) / Nc)
    Q = np.array(node.Q_values())
    N = np.array(node.N_values())
    U = Q + np.sqrt(np.log(node.visit_count + 1) / (N + 1))  # +1 for 0 edge case
    return node.children()[np.argmax(U)]


# TreeNN strategy to get best children
def TreeNN(node, is_dealer):
    cnn.load_state_dict(tr.load("model/CNN.pkl"))
    #cnn2.load_state_dict(tr.load("model/CNN2.pkl"))
    # input:  dealer._point, player._point, dealer._action, dealer._blast_point, is_dealer
    dealer, player = node.state[1], node.state[2]
    cur_player_index = 1 if is_dealer else 2
    node.action = node.state[cur_player_index]._action
    is_dealer = 1 if is_dealer else 0
    action = 1 if node.action == 'H' else 0
    inp = tr.tensor(np.array([[dealer._point, player._point, action, dealer._blast_point, is_dealer]]).reshape(1,5), dtype=tr.float).to(device)
    out = float(cnn(inp))
    node.state[cur_player_index].score_estimate = out
    return node.children()[np.argmax(out)]


# choose_child = exploit
# choose_child = explore
choose_child = uct
choose_child2 = TreeNN


def rollout(node):
    if is_leaf(node.state):
        result = score(node.state)
    else:
        result = rollout(choose_child(node))
    node.visit_count += 1
    node.score_total += result
    node.score_estimate = node.score_total / node.visit_count
    return result


def rollout2(node, is_dealer):
    if is_leaf(node.state):
        result = score(node.state)
    else:
        best_child = choose_child2(node, is_dealer)
        result = rollout(best_child)
    node.visit_count += 1
    node.score_total += result# cur_player's score always convergence to +1
    if is_dealer:
        node.score_estimate = node.score_total / node.visit_count
    else:
        node.score_estimate = (-1)*node.score_total / node.visit_count
    cur_player_index = 1 if is_dealer else 2
    node.action = best_child.state[cur_player_index]._action
    node.score_estimate = best_child.state[cur_player_index].score_estimate
    return result, node.action


def NN(poker, player, dealer, is_dealer, is_auto):
    role = 'Dealer' if is_dealer else 'Player'
    cur_player = player if not is_dealer else dealer
    state = poker, dealer, player

    node = Node(state)
    num_rollouts = 100
    for r in range(num_rollouts):
        rollout2(node, is_dealer)
        #if r % (num_rollouts // 10) == 0: print(node.score_estimate, node.action)
    if node.action == 'H':
        cur_player.get(poker.next)
        print(role + ' get %s On hands\n %s' % (cur_player.cards_on_hand[-1],
                                                cur_player.str_cards_on_hand))
    else:
        cur_player._is_stop = True
        print(role + ' stop')
    return node.visit_count, node.score_estimate


"""
# TODO: increase number of rollouts to see effect on accuracy
if __name__ == "__main__":
    p = Poker()
    p.shuffle()
    dealer = Player(21)
    player = Player(21)

    state = initial_state(p, dealer, player)

    # gauge sub-optimality with rollouts
    num_rollouts = 1000 # TODO: vary
    node = Node(state)
    for r in range(num_rollouts):
        rollout2(node, p._turn)
        if r % (num_rollouts // 10) == 0: print(r, node.score_estimate)
"""
