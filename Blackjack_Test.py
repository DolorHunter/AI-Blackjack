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

        for i in range(NUM_TEST):
            ret = run_game(blast_point, player_stategy, dealer_stategy, silence_mode=True, is_auto=True)
            if ret == 1:
                dealer_win_ct += 1
            else:
                player_win_ct += 1
            dealer_win_rate.append(dealer_win_ct / (i+1))
            player_win_rate.append(player_win_ct / (i+1))

        # draw result of test result
        keys = [i for i in range(NUM_TEST)]
        plt.figure()
        plt.grid()
        plt.plot(keys, dealer_win_rate, label=dealer_stategy_header)
        plt.plot(keys, player_win_rate, label=player_stategy_header)
        plt.legend()
        plt.title("Dealer (Player 1) {} vs Player (Player 2) {}".format(dealer_stategy_header, player_stategy_header))
        plt.xlabel("Number of Test")
        plt.ylabel("Win Rate")
        plt.savefig("res/{} vs {}".format(dealer_stategy_header, player_stategy_header))
        plt.show()


if __name__ == '__main__':
    main()
