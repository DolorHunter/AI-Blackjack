import Blackjack_baseline
from Blackjack_helper import *
from Blackjack_manual import *
from Blackjack_baseline import *
from Blackjack_MCTS import *
from Blackjack_NN import *
import itertools
from matplotlib import pyplot as plt


BLASTPOINT = 21
NUM_TEST = 100
STRATEGY = [manual, baseline, MCTS, NN]
STRATEGY_HEADER = ["manual", "baseline", "MCTS", "NN"]


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
    """.format(role, i + 1)))
        strategies.append(cur_strategy - 1)

    dealer_strategy = STRATEGY[strategies[0]]
    player_strategy = STRATEGY[strategies[1]]
    dealer_strategy_header = STRATEGY_HEADER[strategies[0]]
    player_strategy_header = STRATEGY_HEADER[strategies[1]]

    dealer_win_ct, player_win_ct = 0, 0
    dealer_win_rate, player_win_rate = [], []
    dealer_node_sum_list, player_node_sum_list = [], []
    dealer_node_score_list, player_node_score_list = [], []

    for i in range(NUM_TEST):
        ret = run_game(blast_point, player_strategy, dealer_strategy, silence_mode=True, is_auto=True)
        score, dealer_node_sum, player_node_sum, dealer_node_score, player_node_score = ret

        if score == 1:
            dealer_win_ct += 1
        else:
            player_win_ct += 1
        dealer_win_rate.append(dealer_win_ct / (i+1))
        player_win_rate.append(player_win_ct / (i+1))

        dealer_node_sum_list.append(dealer_node_sum) if strategies[0] == 2 or strategies[0] == 3 else None
        player_node_sum_list.append(player_node_sum) if strategies[1] == 2 or strategies[1] == 3 else None
        dealer_node_score_list.append(dealer_node_score) if strategies[0] == 2 or strategies[0] == 3 else None
        player_node_score_list.append(player_node_score) if strategies[1] == 2 or strategies[1] == 3 else None
        dealer_node_score_list.append(score) if strategies[0] == 0 or strategies[1] == 1 else None
        player_node_score_list.append(score) if strategies[1] == 0 or strategies[1] == 1 else None

        # draw result of test result
        keys = [i for i in range(NUM_TEST)]
        # win rate figure
        plt.figure()
        plt.grid()
        plt.plot(keys, dealer_win_rate, label=dealer_strategy_header)
        plt.plot(keys, player_win_rate, label=player_strategy_header)
        plt.legend()
        plt.title("Dealer (Player 1) {} vs Player (Player 2) {} Size={}".format(dealer_strategy_header,
                                                                                player_strategy_header,
                                                                                blast_point))
        plt.xlabel("Number of Test")
        plt.ylabel("Win Rate")
        plt.savefig("res/WinRate {} vs {} Size{}".format(dealer_strategy_header, player_strategy_header, blast_point))
        plt.show()

        # node sum figure (tree based AI)
        if strategies[0] == 2 or strategies[1] == 2:
            if strategies[0] == 2:
                plt.hist(dealer_node_sum_list, label=dealer_strategy_header)
            if strategies[1] == 2:
                plt.hist(player_node_sum_list, label=player_strategy_header)
            plt.legend()
            plt.grid()
            plt.title("Dealer (Player 1) {} vs Player (Player 2) {} Size={}".format(dealer_strategy_header,
                                                                                    player_strategy_header,
                                                                                    blast_point))
            plt.xlabel("Node Sum")
            plt.ylabel("Times")

            plt.savefig("res/NodeSum {} vs {} Size{}".format(dealer_strategy_header, player_strategy_header, blast_point))
            plt.show()

        # node final score figure (baseline AI and tree based AI)
        if (strategies[0] == 1 or strategies[0] == 2) or (strategies[1] == 1 or strategies[1] == 2):
            if strategies[0] == 1 or strategies[0] == 2:
                plt.hist(dealer_node_score_list, label=dealer_strategy_header)
            if strategies[1] == 1 or strategies[1] == 2:
                plt.hist(player_node_score_list, label=player_strategy_header)
            plt.legend()
            plt.grid()
            plt.title("Dealer (Player 1) {} vs Player (Player 2) {} Size={}".format(dealer_strategy_header,
                                                                                    player_strategy_header,
                                                                                    blast_point))
            plt.xlabel("Node Final Score")
            plt.ylabel("Times")
            plt.savefig("res/FinScore {} vs {} Size{}".format(dealer_strategy_header, player_strategy_header, blast_point))
            plt.show()


if __name__ == '__main__':
    main()
