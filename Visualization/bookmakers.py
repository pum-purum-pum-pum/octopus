import numpy as np
import pandas as pd
import argparse
import json


epilog = \
    "EXAMPLE of usage:\n" +\
    "python bookmakers.py --id1 1 --id2"

parser = argparse.ArgumentParser(description='input output files', epilog=epilog)
parser.add_argument('--id1', type=int, help="player1 id")
parser.add_argument('--id2', type=int, help="player2 id")
args = parser.parse_args()


if __name__ == "__main__":
    data_book_makers = pd.read_csv('../data/odds_atp.csv')
    koef = data_book_makers.loc[(data_book_makers['ID1_O'] == args.id1)\
                         & (data_book_makers['ID2_O'] == args.id2)][['K1', 'K2']].mean(axis=0)
    if np.isnan(koef[0]) or np.isnan(koef[1]):
        print (json.dumps([0.5, 0.5]))
    else:
        print (json.dumps([koef[0], koef[1]]))