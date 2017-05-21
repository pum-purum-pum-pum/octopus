import numpy as np
import pandas as pd
import argparse
import json
import os
id_to_name = {1: "Hard", 2: "Clay", 3: "I.hard", 4: "Carpet", 5: "Grass", 6: "Acrylic"}


def get_games(cursor, pid, win=1, court=1):
    query = 'select * from games_atp INNER JOIN tours_atp on\
             games_atp.ID_T_G = tours_atp.ID_T where ID{win_}_G={id1_} and ID_C_T={court_}'
    query = query.format(id1_=pid, win_=win, court_=court)
    return cursor.execute(query).fetchall()


def get_win_rate(cursor, pid1, pid2, court=1):
    p1_wins = len(get_games(cursor, pid1, win=1, court=court))
    p1_loss = len(get_games(cursor, pid1, win=2, court=court))
    p2_wins = len(get_games(cursor, pid2, win=1, court=court))
    p2_loss = len(get_games(cursor, pid2, win=2, court=court))
    if p1_loss + p1_wins == 0 or p2_loss + p2_wins == 0:
        return []
    return p1_wins / (p1_loss + p1_wins), p2_wins / (p2_loss + p2_wins)


def win_rate(cursor, pid1, pid2):
    court_type = []
    wr1 = []
    wr2 = []
    for i in id_to_name.keys():
        wr = get_win_rate(cursor, pid1, pid2, i)
        if len(wr) > 0:
            wr1.append(wr[0])
            wr2.append(wr[1])
            court_type.append(id_to_name[i] + ' win rate')
    visualization_data = [wr1, wr2]
    visualization_legend = {'axis': court_type, 'title': 'Individual features'}
    r = dict(type='side_to_side', data=visualization_data, legend=visualization_legend)
    return (json.dumps(r))

if __name__ == "__main__":
    pass