"""Chess rating program to store, access and
 modify chess rating scores for players.


Note: Autosave is on by default, ie, all changes will be saved automatically.
    To discard changes, choose exit and then choose not save.
    Alternatively, turn off for that session by passing `-d` switch.
    Then, to save changes, choose exit and then choose save.
"""

from pathlib import Path
import os
import math
import json
import argparse
from typing import Any, List
from prettytable import PrettyTable
from shutil import copytree, rmtree

try:
    from IPython import embed as enter_repl
    REPL_MODE = "ipython"
except:
    from code import interact as enter_repl
    REPL_MODE = "python"

global result_dir, K_FACTOR, START_RATING, AUTOSAVE

result_dir: Path = None

# most systems use a K factor that decreases with player experience
# to account for rate deflation
# https://en.wikipedia.org/wiki/Elo_rating_system?oldformat=true#Combating_deflation
K_FACTOR: int = 20

START_RATING: int = 1200

AUTOSAVE = True


# Function to calculate the Probability
def probability(rating1, rating2):
    return (1.0 * 1.0 /
            (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400)))


# Function to calculate Elo rating
# k is a constant.
# win=True if A wins, win=False if A loses
def elo_rating(Ra, Rb, k, win):
    # winning probability of player A
    Pa = probability(Rb, Ra)

    # winning probability of player B
    Pb = probability(Ra, Rb)

    # player A wins
    if win:
        Ra = Ra + k * (1 - Pa)
        Rb = Rb + k * (0 - Pb)

    # player A loses
    else:
        Ra = Ra + k * (0 - Pa)
        Rb = Rb + k * (1 - Pb)

    # return new ratings
    return Ra, Rb
