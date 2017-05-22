
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import argparse
import json
import os
import sqlite3

epilog = \
        "EXAMPLE of usage:\n" + \
        "python bookmakers.py --id1 9 --id2 27"
        
parser = argparse.ArgumentParser(description='input output files', epilog=epilog)
parser.add_argument('--id1', type=int, help="player1 id")
parser.add_argument('--id2', type=int, help="player2 id")
parser.add_argument('--tour', type=int, default=-1)
parser.add_argument('--features', type=str, default='')
args = parser.parse_args()


def players_pair_stats(cursor, id1, id2, id_t=None, features_dict=None):
    id_p1 = "({}, {})".format(id1, id2)
    id_p2 = "({}, {})".format(id2, id1)
    
    schema = cursor.fetchall()
    query1 = 'select * from pairs where id_p = "{id_p1_}" or id_p = "{id_p2_}"'
    query1 = query1.format(id_p1_=id_p1, id_p2_=id_p2)
    pair_features = cursor.execute(query1).fetchall()

    query2 = 'select * from players where id = "{id1_}"'
    query3 = 'select * from players where id = "{id2_}"'
    query2 = query2.format(id1_=id1, id2_ = id2)
    query3 = query3.format(id1_=id1, id2_ = id2)
    features1 = cursor.execute(query2).fetchall()
    features2 = cursor.execute(query3).fetchall()
    query4 = 'select * from games_atp where (ID1_G={id1_} AND ID2_G={id2_}) or (ID1_G={id2_} AND ID2_G={id1_})'
    query4 = query4.format(id1_=id1, id2_ = id2)
    games_history = cursor.execute(query4).fetchall()

    legend_data1 = {"axis": ["Player ID", "Rating", "Rank", "Recent games results1", "Recent games results2", "Recent games results3", "Recent games results4", "Recent games results5", "Games count", "Winrate", "Days after last game"], "Title": "Individual features"}
    legend_data2 = {"axis": ["player ID", "Rating difference", "Rank difference", "Games amount difference", "Winrate Difference", "Days after last game difference", "Meetings count", "Pair winrate", "Recent meeting results1", "Recent meeting results2", "Recent meeting results3", "Recent meeting results4", "Recent meeting results5", "Indirect score"], "Title": "Players pair features"}
    legend_data3 = {"axis": ["1st player ID", "2nd player ID", "Tournament ID", "Round ID", "Game result", "Date"], "Title": "Recent games history"}

    return [{"type": "side_to_side", "data": [features1, features2], "legend": legend_data1},
                {"type": "table", "data": pair_features, "legend": legend_data2},
                {"type": "history", "data": games_history, "legend": legend_data3}]

if __name__ == "__main__":
    with sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + '/../data/on_court.db') as con:
        cursor = con.cursor()
    print(json.dumps(players_pair_stats(cursor, args.id1, args.id2)))


