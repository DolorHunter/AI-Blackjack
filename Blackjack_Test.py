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

    # combination of each strategy
    strategies = list(itertools.combinations([i for i in range(4)], 2))

    for strategy in strategies:
        dealer_stategy = STRATEGY[strategy[0]]
        player_stategy = STRATEGY[strategy[1]]
        dealer_stategy_header = STRATEGY_HEADER[strategy[0]]
        player_stategy_header = STRATEGY_HEADER[strategy[1]]

        dealer_win_ct, player_win_ct = 0, 0
        dealer_win_rate, player_win_rate = [], []
        dealer_node_sum_list, player_node_sum_list = [], []
        dealer_node_score_list, player_node_score_list = [], []

        for i in range(NUM_TEST):
            ret = run_game(blast_point, player_stategy, dealer_stategy, silence_mode=True, is_auto=True)
            score, dealer_node_sum, player_node_sum, dealer_node_score, player_node_score = ret

            if score == 1:
                dealer_win_ct += 1
            else:
                player_win_ct += 1
            dealer_win_rate.append(dealer_win_ct / (i+1))
            player_win_rate.append(player_win_ct / (i+1))

            dealer_node_sum_list.append(dealer_node_sum) if strategy[0] == 2 else None
            player_node_sum_list.append(player_node_sum) if strategy[1] == 2 else None
            dealer_node_score_list.append(dealer_node_score) if strategy[0] == 2 else None
            player_node_score_list.append(player_node_score) if strategy[1] == 2 else None
            dealer_node_score_list.append(score) if strategy[0] == 1 else None
            player_node_score_list.append(score) if strategy[1] == 1 else None

        # draw result of test result
        keys = [i for i in range(NUM_TEST)]
        # win rate figure
        plt.figure()
        plt.grid()
        plt.plot(keys, dealer_win_rate, label=dealer_stategy_header)
        plt.plot(keys, player_win_rate, label=player_stategy_header)
        plt.legend()
        plt.title("Dealer (Player 1) {} vs Player (Player 2) {} Size={}".format(dealer_stategy_header,
                                                                                player_stategy_header,
                                                                                blast_point))
        plt.xlabel("Number of Test")
        plt.ylabel("Win Rate")
        plt.savefig("res/WinRate {} vs {} Size{}".format(dealer_stategy_header, player_stategy_header, blast_point))
        plt.show()

        # node sum figure (tree based AI)
        if strategy[0] == 2 or strategy[1] == 2:
            if strategy[0] == 2:
                plt.hist(dealer_node_sum_list, label=dealer_stategy_header)
            if strategy[1] == 2:
                plt.hist(player_node_sum_list, label=player_stategy_header)
            plt.legend()
            plt.grid()
            plt.title("Dealer (Player 1) {} vs Player (Player 2) {} Size={}".format(dealer_stategy_header,
                                                                                    player_stategy_header,
                                                                                    blast_point))
            plt.xlabel("Number of Test")
            plt.ylabel("Node Sum")

            plt.savefig("res/NodeSum {} vs {} Size{}".format(dealer_stategy_header, player_stategy_header, blast_point))
            plt.show()

        # node final score figure (baseline AI and tree based AI)
        if (strategy[0] == 1 or strategy[0] == 2) or (strategy[1] == 1 or strategy[1] == 2):
            if strategy[0] == 1 or strategy[0] == 2:
                plt.hist(dealer_node_score_list, label=dealer_stategy_header)
            if strategy[1] == 1 or strategy[1] == 2:
                plt.hist(player_node_score_list, label=player_stategy_header)
            plt.legend()
            plt.grid()
            plt.title("Dealer (Player 1) {} vs Player (Player 2) {} Size={}".format(dealer_stategy_header,
                                                                                    player_stategy_header,
                                                                                    blast_point))
            plt.xlabel("Number of Test")
            plt.ylabel("Node Final Score")
            plt.savefig("res/FinScore {} vs {} Size{}".format(dealer_stategy_header, player_stategy_header, blast_point))
            plt.show()


if __name__ == '__main__':
    main()
