# AI-Blackjack

## Dependencies

```commandline
$ pip install numpy matplotlib torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html 
```

## Run

Run Blackjack with customized Blasting point, user allow choosing a strategy for Dealer (Player 1) and Player (Player 2). Strategies include `Manual`, `Baseline`, `MCTS` and `NN`. After that, the game start and you can see get result shortly.

Blackjack based on Blackjack_helper.py, it has all rules for Poker, Players and states. And different strategies start with run_game function in Blackjack_helper.py. And each strategy is defined inside each file named after the strategy, and called from Blackjack.py.

```commandline
$ python Blackjack.py
```

## Test

Test is a integrated experiment module, it will create combinations of all strategies and run all of the combination 100 times, and give some figures to show the result, including win rate figure, node counts distribution figure and final score distribution figure, if applicable. Figure will be saved in /res folder.

```commandline
$ python Blackjack_Test.py
```

## Files

These are files and comments for the files.

```plain
AI-Blackjack
├ /res                      # Folder for figures
├ Blackjack.py              # Main function
├ Blackjack_helper.py       # Helper for Blackjack
├ Blackjack_manual.py       # Manual mode
├ Blackjack_baseline.py     # Baseline AI
├ Blackjack_MCTS.py         # MCTS Tree-based AI
├ Blackjack_NN.py           # TreeNN AI
├ Blackjack_NN_helper.py    # Helper for TreeNN AI
└ README.md                 # READ ME
```
