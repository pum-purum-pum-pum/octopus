import numpy as np
import pandas as pd
import argparse
import json
import os


def get_bookmakers_coef(cursor, player1, player2):
    query = 'select * from odds_atp where ID1_O={id1_} AND ID2_O={id2_}'
    query = query.format(id1_=player1, id2_=player2)
    data = cursor.execute(query).fetchall()
    reversed = False
    if len(data) == 0:
        query = 'select * from odds_atp where ID1_O={id1_} AND ID2_O={id2_}'
        query = query.format(id1_=player2, id2_=player1)
        data = cursor.execute(query).fetchall()
        reversed = True
    k1 = []
    k2 = []
    for line in data:
        if line[5] is not None and line[6] is not None:
            k1.append(float(line[5]))
            k2.append(float(line[6]))
    coef = (float(np.mean(k1)), float(np.mean(k2)))
    if reversed:
        coef = coef[::-1]
    if np.isnan(coef[0]) or np.isnan(coef[1]):
        return (json.dumps
               ({'type': 'piechart',
                 'data': [0.5, 0.5],
                 'legend': {'title': 'Average odds of bookmakers'}
               }))
    return json.dumps({'type': 'piechart',
                       'data': [coef[0], coef[1]],
                       'legend': {'title': 'Average odds of bookmakers'}
                       })

if __name__ == "__main__":
    epilog = \
        "EXAMPLE of usage:\n" + \
        "python bookmakers.py --id1 9 --id2 27"

    parser = argparse.ArgumentParser(description='input output files', epilog=epilog)
    parser.add_argument('--id1', type=int, help="player1 id")
    parser.add_argument('--id2', type=int, help="player2 id")
    parser.add_argument('--tour', type=int, default=-1)
    parser.add_argument('--features', type=str, default='')
    args = parser.parse_args()

    data_book_makers = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/../data/odds_atp.csv')
    koef = data_book_makers.loc[(data_book_makers['ID1_O'] == args.id1)\
                         & (data_book_makers['ID2_O'] == args.id2)][['K1', 'K2']].mean(axis=0)
    if np.isnan(koef[0]) or np.isnan(koef[1]):
        print (json.dumps
               ({'type': 'piechart',
                 'data': [0.5, 0.5],
                 'legend': {'title': 'Average odds of bookmakers'}
               }))
    else:
        print(json.dumps
               ({'type': 'piechart',
                 'data': [koef[0], koef[1]],
                 'legend': {'title': 'Average odds of bookmakers'}
               }))