import numpy as np
import pandas as pd
import argparse
import json
import os

epilog = \
    "EXAMPLE of usage:\n" +\
    "python bookmakers.py --id1 9 --id2 27"

parser = argparse.ArgumentParser(description='input output files', epilog=epilog)
parser.add_argument('--id1', type=int, help="player1 id")
parser.add_argument('--id2', type=int, help="player2 id")
parser.add_argument('--tour', type=int, default=-1)
parser.add_argument('--features', type=str, default='')
args = parser.parse_args()


def get_win_rate(pid1, pid2, games_data, players_data):
    wins = pd.merge(players_data, games_data, left_on='ID_P', right_on='ID1_G').groupby('ID_P').size()
    loses = pd.merge(players_data, games_data, left_on='ID_P', right_on='ID2_G').groupby('ID_P').size()
    win_los = pd.concat([wins, loses], axis=1)
    win_los.columns = ['wins', 'loses']
    win_los['win_rate'] = win_los['wins'] / (win_los['loses'] + win_los['wins'])
    if len(win_los.iloc[win_los.index ==pid1]['win_rate'].values) == 0 or\
    len(win_los.iloc[win_los.index ==pid2]['win_rate'].values) == 0:
        return []
    return win_los.iloc[win_los.index ==pid1]['win_rate'].values[0], \
            win_los.iloc[win_los.index ==pid2]['win_rate'].values[0]


if __name__ == "__main__":
    games_data = pd.read_csv('../data/games_atp.csv')
    players_data = pd.read_csv('../data/players_atp.csv')
    tours_data = pd.read_csv('../data/tours_atp.csv')
    games_data = pd.merge(tours_data, games_data, left_on='ID_T', right_on='ID_T_G')
    id_to_name = {1: "Hard", 2: "Clay", 3: "I.hard", 4: "Carpet", 5: "Grass", 6: "Acrylic"}
    court_type = []
    wr1 = []
    wr2 = []
    for i in id_to_name.keys():
        wr = get_win_rate(19, 75, games_data[games_data['ID_C_T'] == i], players_data)
        if len(wr) > 0:
            wr1.append(wr[0])
            wr2.append(wr[1])
            court_type.append(id_to_name[i] + ' win rate')
    visualization_data = [wr1, wr2]
    visualization_legend = {'axis': court_type, 'title': 'Individual features'}
    r = dict(type='side_to_side', data=visualization_data, legend=visualization_legend)
    print (json.dumps(r))