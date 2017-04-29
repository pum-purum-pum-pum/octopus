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

def players_pair_stats(id1, id2, id_t=None, features_dict=None):
    
    ind_features = pd.read_csv("../data/players.csv")
    pair_features = pd.read_csv("../data/pairs.csv")
    games = pd.read_csv("../data/games_atp.csv")
    
    features1 = ind_features[(ind_features["ID"] == id1)]
    features2 = ind_features[(ind_features["ID"] == id2)]
    games_history = games[(games["ID1_G"] == id1) & (games["ID2_G"] == id2)]
    
    legend_data1 = {"Title": "Individual features", "Player1": "Player 1", "Player2": "Player 2"}
    legend_data2 = {"Title": "Players pair features"}
    legend_data3 = {"Title": "Recent games history"}
    
    return [{"type": "side_to_side", "data": [features1, fetures2], "legend": legend_data1},
            {"type": "table", "data": pair_features, "legend": legend_data2},
            {"type": "history", "data": games_history, "legend": legend_data3}]


if __name__ == "__main__":
    ind_features = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/../data/players.csv')
    pair_features = pd.read_csv(os.path.dirname(od.path.realpath(__file__)) +'/../data/pairs.csv')
    games = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) +'/../data/games_atp.csv')
    
    print(json.dumbs(players_pair_stats(args.id1, args.id2)
