import numpy as np
from trueskill import Rating, rate_1vs1
# import progressbar
from trueskill.backends import cdf
from math import sqrt
from trueskill import BETA
from trueskill.backends import cdf
import sqlite3
import pandas as pd

def win_probability_by_rate(player_rating, opponent_rating):
    delta_mu = player_rating.mu - opponent_rating.mu
    denom = sqrt(2 * (BETA * BETA) + pow(player_rating.sigma, 2) + pow(opponent_rating.sigma, 2))
    return cdf(delta_mu / denom)


def win_prob(cursor, pid1, pid2):
    p1 = cursor.execute('select * from octorate where ID={id_}'.format(id_=pid1)).fetchall()[0]
    p2 = cursor.execute('select * from octorate where ID={id_}'.format(id_=pid2)).fetchall()[0]
    return str(win_probability_by_rate(Rating(mu=p1[1], sigma=p1[2]), Rating(mu=p2[1], sigma=p2[2])))

if __name__ == "__main__":
    con = sqlite3.connect('../data/on_court.db')
    cursor = con.cursor()
    query = 'select * from games_atp '
    query = query.format(id1_=1, win_=1, court_=1)
    games = np.array(cursor.execute(query).fetchall())
    max_id = max(games[:, 0].max(), games[:, 1].max()) + 1
    # bar = progressbar.ProgressBar(max_value=len(games))
    ratings = [Rating() for i in range(max_id)]
    for ii, i in enumerate(games):
        bar.update(ii)
        ratings[i[0]], ratings[i[1]] = rate_1vs1(ratings[i[0]], ratings[i[1]])
    c = con.cursor()
    c.execute('drop table if exists octorate')
    c.execute('CREATE TABLE octorate (ID, mu, sigma)')
    data_ar_to_csv = []
    for ii, i in enumerate(ratings):
        data_ar_to_csv.append([ii, i.mu, i.sigma])
    npar_data = np.array(data_ar_to_csv)
    csv_to_save = pd.DataFrame(data = npar_data, columns=['ID', 'mu', 'sigma'])
    for ii, i in enumerate(ratings):
        c.execute('INSERT INTO octorate VALUES ({id_}, {mu_}, {sigma_})'.format(id_=ii, mu_=i.mu, sigma_=i.sigma))
    c.close()
