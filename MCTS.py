import numpy as np
from Blackjack import *


def score(state):
    p, dealer, player = state
    if not player._is_alive or player._is_stop and player.point < dealer.point:
        return -1
    elif player._is_stop and player.point > dealer.point:
        return 1
    return 0

def get_player(state):
    p, dealer, player = state
    return player.is_alive and not player.is_stop  # true->player, false->dealer


def children_of(state):
    p, dealer, player = state
    children = []
    if get_player(state):  # Hit
        if player.point <= BLASTPOINT:
            player.get(p.next)
            children.append((p, dealer, player))
        else:
            player._is_alive = False
    else:
        if dealer.point <= BLASTPOINT:
            dealer.get(p.next)
            children.append((p, dealer, player))
        else:
            dealer._is_alive = False
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
        sign = +1 if get_player(self.state) else -1

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


# choose_child = exploit
# choose_child = explore
choose_child = uct


def rollout(node):
    if is_leaf(node.state):
        result = score(node.state)
    else:
        result = rollout(choose_child(node))
    node.visit_count += 1
    node.score_total += result
    node.score_estimate = node.score_total / node.visit_count
    return result


# TODO: increase number of rollouts to see effect on accuracy
if __name__ == "__main__":
    p = Poker()
    p.shuffle()
    dealer = Player()
    player = Player()

    state = initial_state(p, dealer, player)

    # gauge sub-optimality with rollouts
    num_rollouts = 10000 # TODO: vary
    node = Node(state)
    for r in range(num_rollouts):
        rollout(node)
        if r % (num_rollouts // 10) == 0: print(r, node.score_estimate)