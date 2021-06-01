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


class Player:
    global result_dir
    properties = ['name', 'rating', 'wins', 'losses']

    def __init__(self, name, rating=START_RATING, wins=0, losses=0):
        if name == 'game':
            name = 'game1'
            print("dont use player name 'game'")
        self.name = name
        self.rating = rating
        self.file = result_dir.joinpath(name + '.json')
        self.wins = wins
        self.losses = losses

    def make_file(self):
        self.file.touch(0o777)

    def add_win(self):
        self.wins += 1

    def add_loss(self):
        self.losses += 1

    def get_score(self, score: str):
        return getattr(self, score)

    def save(self):
        file = self.file
        data = {
            'rating': self.rating,
            'wins': self.wins,
            'losses': self.losses
        }
        with open(file, 'w') as f:
            json.dump(data, f)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()


class Game:
    global result_dir, AUTOSAVE
    properties = Player.properties

    def __init__(self, players, k=K_FACTOR, start_rating=START_RATING):
        self.players = players
        self.k = k
        self.start_rating = start_rating
        self.file = result_dir.joinpath('game.json')
        self.backup_folder = result_dir.joinpath('_backup')

        self.autosave()

    def update(self, p1, p2, win):
        winner, loser = (p1, p2) if win else (p2, p1)

        winner.add_win()
        loser.add_loss()

        Ra, Rb = p1.rating, p2.rating
        k = self.k
        new_Ra, new_Rb = elo_rating(Ra, Rb, k, win)

        # round down to 3 decimal places
        p1.rating = round(new_Ra, 3)
        p2.rating = round(new_Rb, 3)

        self.autosave()

    def get_players_by_player_names(
            self, player_names: List[str]) -> List[Player]:
        players = [self.get_player_by_name(s) for s in player_names]
        return players

    def get_player_by_name(self, name: str):
        for p in self.players:
            if p.name == name:
                return p

    def save(self):
        """Save data of self

        In most scenarios, `.autosave()` will be the better option as it
        respects user autosave preference.
        """
        file = self.file
        data = {
            'k': self.k
        }
        with open(file, 'w') as f:
            json.dump(data, f)
        for p in self.players:
            p.save()

    def autosave(self):
        """Save data of game if AUTOSAVE is True

        Returns:
            bool: whether data was saved or not
        """
        if AUTOSAVE:
            self.save()
            return True
        return False

    def make_backup(self, overwrite=False):
        # dont backup unnecessarily
        # use it as a means to preserve state before current session to revert
        if overwrite:
            self.delete_backup()
            copytree(result_dir, self.backup_folder, dirs_exist_ok=True)
        else:
            if self.backup_folder.exists():
                print('backup already exists. not overwriting')
            else:
                copytree(result_dir, self.backup_folder, dirs_exist_ok=True)

    def delete_backup(self):
        if self.backup_folder.exists():
            rmtree(self.backup_folder)

    def restore_backup(self):
        self.delete_current_files()  # delete existing files
        # copy backup files
        copytree(self.backup_folder, result_dir, dirs_exist_ok=True)
        # self.delete_backup()

    def delete_current_files(self):
        for i in os.listdir(result_dir):
            # dont delete _backup folder
            if i == '_backup':
                continue
            file_path = result_dir.joinpath(i)
            os.remove(file_path)

    def i_add_player(self):
        name = input('give the single-word player name: ').strip()
        rating = input(
            f'give the rating of player (default - {START_RATING}): ').strip()
        rating = rating if rating else START_RATING

        print()
        confirm = input('Confirm [Y/n]? ')
        if confirm in ("n", "N"):
            self.i_add_player()
            return

        print()
        self.add_player(name, rating)

    def add_player(self, name, rating):
        p = Player(name=name, rating=rating)
        self.players.append(p)

        self.autosave()

    def i_add_match(self):
        p1_name = input('give the name of the first player: ').strip()
        p2_name = input('give the name of the second player: ').strip()
        win = int(input(
            'give the number of the winning player' +
            f', i.e., 0 if {p1_name} won OR 1 if {p2_name} won: '
        ).strip())

        print()
        confirm = input('Confirm [Y/n]? ')
        if confirm in ("n", "N"):
            self.i_add_match()
            return

        print()
        self.add_match(p1_name, p2_name, win)

    def add_match(self, p1_name, p2_name, win):
        p1 = self.get_player_by_name(p1_name)
        p2 = self.get_player_by_name(p2_name)
        self.update(p1, p2, win)

    def i_display_info(self):
        str_properties = ','.join([p for p in Game.properties])
        str_property_indices = ','.join(
            [str(i + 1) for i in range(len(Game.properties))])

        # sort = index of the property in Game.properties
        # or, Game.properties[sort] = desired property
        sort = input('which property to sort by?\nchoose one of ' +
                     '(' + str_properties + ') by using numbers (' +
                     str_property_indices + ') ' +
                     'respectively (default 0): ').strip()
        sort = int(sort) - 1 if sort else 0

        print('which players\' info to show in table?\n')
        print(f'all players:\n    {self.players}\n')
        player_names = input('type their names seperated by space ' +
                             '(for all, leave empty): ')
        if player_names == '':
            player_names = None
        else:
            player_names = player_names.strip().split()

        print()
        self.display_info(sort, player_names)

    def display_info(self, sort: int = 0,
                     player_names: List[str] = None):
        # sort is the index of the property in Game.properties
        t = PrettyTable()
        t.field_names = ["Players", "Rating", "Wins", "Losses"]
        data = []
        if not player_names:
            players = self.players
        else:
            players = self.get_players_by_player_names(player_names)
        for p in players:
            # get the properties as stated in Game.properties
            row = [getattr(p, prop) for prop in Game.properties]
            data.append(row)
        data.sort(key=lambda x: x[sort], reverse=True)
        t.add_rows(data)
        t.align = "c"
        print(t)

    def i_reset_scores(self):
        # not 'name' property
        str_properties = ','.join([p for p in Game.properties if p != 'name'])

        # scores = properties in Game.properties
        scores = input('which score to reset?\nchoose out of ' +
                       '(' + str_properties + ') by typing the value ' +
                       '(default all, leave empty)\n' +
                       'choose multiple options by seperating with space: ')
        if not scores:
            scores = None
        else:
            scores = scores.strip().split()

        print()
        print('which player\'s score to reset?\n')
        print(f'all players:\n    {self.players}\n')
        player_names = input('type the name: ').strip()

        print()
        confirm = input('Confirm [Y/n]? ')
        if confirm in ("n", "N"):
            self.i_reset_scores()
            return

        print()
        self.reset_scores(player_names, scores)

    def reset_scores(self, player_name: str, scores: List[str] = None):
        # scores - list of properties from Game.properties to reset
        # if empty, choose all
        if not scores:
            scores = list(Game.properties)
        if 'name' in scores:
            scores = scores.remove('name')  # dont use 'name' property

        player = self.get_player_by_name(player_name)

        for s in scores:
            if s == 'rating':
                setattr(player, s, self.start_rating)
            elif s == 'wins' or s == 'losses':
                setattr(player, s, 0)

        self.autosave()

    def i_exit(self):
        save = input('do you want to save game before exiting [Y/n]: ').strip()
        save = False if save in ("n", "N") else True
        if not save:
            print()
            confirm = input('not saving will DISCARD ALL CHANGES ' +
                            'made in this session.\nAre you sure? [Y/n]')
            confirm = False if save in ("n", "N") else True

            if not confirm:
                print()
                print('Returning ...')
                return

        print()
        self.exit(save=save)

    def exit(self, save=True):
        if save:
            self.save()
        else:
            self.restore_backup()
        print()
        print('Exiting ...')
        exit()
