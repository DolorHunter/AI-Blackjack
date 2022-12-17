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
    for i, role in enumerate(["Dealer", "Player"]):
        cur_strategy = -1
        while cur_strategy < 1 or cur_strategy > 4:
            cur_strategy = int(input("""
Input Strategy for {} (Player {})
1. Manual
2. Baseline
3. MCTS
4. NN
""".format(role, i+1)))
        strategies.append(cur_strategy-1)

    dealer_stategy = STRATEGY[strategies[0]]
    player_stategy = STRATEGY[strategies[1]]

    run_game(blast_point, player_stategy, dealer_stategy, silence_mode=False, is_auto=False)


if __name__ == '__main__':
    main()
