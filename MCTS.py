import numpy as np
from Blackjack import *

# Similar tic-tac-toe implementation to minimax
# state[r,c] is the content at position (r,c) of the board: "_", "X", or "O"
def state_string(state):
    return "\n".join(["".join(row) for row in state])

def score(state):
    for player, value in (("X", 1), ("O", -1)):
        if (state == player).all(axis=0).any(): return value
        if (state == player).all(axis=1).any(): return value
        if (np.diag(state) == player).all(): return value
        if (np.diag(np.rot90(state)) == player).all(): return value
    return 0

def get_player(state):
    return "XO"[
        np.count_nonzero(state == "O") < np.count_nonzero(state == "X")]

def children_of(state):
    symbol = get_player(state)
    children = []
    for r in range(state.shape[0]):
        for c in range(state.shape[1]):
            if state[r,c] == "_":
                child = state.copy()
                child[r,c] = symbol
                children.append(child)
    return children

def is_leaf(state):
    children = children_of(state)
    value = score(state)
    return len(children) == 0 or value != 0


# MCTS to solve tic-tac-toe
# TODO: implement exploration strategy
class Node:
    def __init__(self, state):
        self.p, self.dealer, self.player = state
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
        sign = +1 if get_player(self.state) == "X" else -1

        # empirical average child utilities
        # special case to handle 0 denominator for never-visited children
        Q = [sign * c.score_total / (c.visit_count+1) for c in children]
        # Q = [sign * c.score_total / max(c.visit_count, 1) for c in children]

        return Q

# exploit strategy: choose the best child for the current player
def exploit(node):
    return node.children()[np.argmax(node.Q_values())]

# explore strategy: choose the least-visited child
def explore(node):
    return node.children()[np.argmin(node.N_values())] # TODO: replace with exploration

# upper-confidence bound strategy
def uct(node):
    # max_c Qc + sqrt(ln(Np) / Nc)
    Q = np.array(node.Q_values())
    N = np.array(node.N_values())
    U = Q + np.sqrt(np.log(node.visit_count + 1) / (N + 1)) # +1 for 0 edge case
    return node.children()[np.argmax(U)]

# choose_child = exploit
# choose_child = explore
choose_child = uct

def rollout(node):
    if is_leaf(node.state): result = score(node.state)
    else: result = rollout(choose_child(node))
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

