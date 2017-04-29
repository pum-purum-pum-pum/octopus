import numpy as np
import pandas as pd
import argparse
import json
import os

epilog = \
    "EXAMPLE of usage:\n" +\
    "python strength_triangle.py --id1 19 --id2 75"

parser = argparse.ArgumentParser(description='input output files', epilog=epilog)
parser.add_argument('--id1', type=int, help="player1 id")
parser.add_argument('--id2', type=int, help="player2 id")
parser.add_argument('--tour', type=int, default=-1)
parser.add_argument('--features', type=str, default='')
args = parser.parse_args()


def solo_name(name):
    return not '/' in name

def get_win_rate(pid1, pid2):
    games_data = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/../data/games_atp.csv')
    players_data = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/../data/players_atp.csv')
    wins = pd.merge(players_data, games_data, left_on='ID_P', right_on='ID1_G').groupby('ID_P').size()
    loses = pd.merge(players_data, games_data, left_on='ID_P', right_on='ID2_G').groupby('ID_P').size()
    win_los = pd.concat([wins, loses], axis=1)
    win_los.columns = ['wins', 'loses']
    win_los['win_rate'] = win_los['wins'] / (win_los['loses'] + win_los['wins'])
    return win_los.iloc[win_los.index ==pid1]['win_rate'].values[0], \
            win_los.iloc[win_los.index ==pid2]['win_rate'].values[0]

def strength_triangle(id_1, id_2, tournament=None, other = None):
    p_data = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/../data/players_atp.csv')
    p_data = p_data.dropna(subset = ['RANK_P', 'POINT_P', 'PRIZE_P'])
    visualization_type = 'forcechart'
    rank_norm = np.max(p_data['RANK_P'].values)
    point_norm = np.max(p_data['POINT_P'].values)
    prize_norm = np.max(p_data['PRIZE_P'].values)
    rank_p1 = p_data[p_data['ID_P'] == id_1]['RANK_P'].values[0]
    rank_p2 = p_data[p_data['ID_P'] == id_2]['RANK_P'].values[0]
    point_p1 = p_data[p_data['ID_P'] == id_1]['POINT_P'].values[0]
    point_p2 = p_data[p_data['ID_P'] == id_2]['POINT_P'].values[0]
    prize_p1 = p_data[p_data['ID_P'] == id_1]['PRIZE_P'].values[0]
    prize_p2 = p_data[p_data['ID_P'] == id_2]['PRIZE_P'].values[0]
    rank_p1_norm = (rank_norm - rank_p1)/rank_norm
    rank_p2_norm = (rank_norm - rank_p2)/rank_norm
    point_p1_norm = point_p1/point_norm
    point_p2_norm = point_p2/point_norm
    prize_p1_norm = prize_p1/prize_norm
    prize_p2_norm = prize_p2/prize_norm
    wr_p1, wr_p2 =  get_win_rate(id_1, id_2)
    visualization_data = [[rank_p1_norm, point_p1_norm, prize_p1_norm, wr_p1],
                          [rank_p2_norm, point_p2_norm, prize_p2_norm, wr_p2]]
    visualization_legend = {'axis': ['Rank', 'Points', 'Prize', 'Win Rate'], 'title': 'Strength polygon'}
    r = dict(type = visualization_type, data = visualization_data, legend = visualization_legend)
    return r

if __name__ == "__main__":
    try:
        print(json.dumps(strength_triangle(args.id1, args.id2)))
    except:
        print('')
