import sqlite3
import sys
sys.path.append("..")
con = sqlite3.connect('../data/on_court.db')
cursor = con.cursor()
from math import sqrt
from trueskill import BETA
from trueskill.backends import cdf
import progressbar
import numpy as np
import pandas as pd
from trueskill import Rating, rate_1vs1

def win_probability(player_rating, opponent_rating):
    delta_mu = player_rating.mu - opponent_rating.mu
    denom = sqrt(2 * (BETA * BETA) + pow(player_rating.sigma, 2) + pow(opponent_rating.sigma, 2))
    return cdf(delta_mu / denom)


if __name__ == "__main__":
    odds = pd.read_csv('../data/odds_atp.csv')
    games = pd.read_csv('../data/games_atp.csv')
    games_with_odds = pd.merge(odds, games, how='inner',
                               left_on=['ID1_O', 'ID2_O', 'ID_T_O', 'ID_R_O'],
                               right_on=['ID1_G', 'ID2_G', 'ID_T_G', 'ID_R_G'])
    games = games.as_matrix()
    max_id = max(games[:, 0].max(), games[:, 1].max()) + 1
    ratings = [Rating() for i in range(max_id)]
    bar = progressbar.ProgressBar(max_value=len(games))
    for ii, i in enumerate(games):
        bar.update(ii)
        ratings[i[0]], ratings[i[1]] = rate_1vs1(ratings[i[0]], ratings[i[1]])
    data_ar_to_csv = []
    for ii, i in enumerate(ratings):
        data_ar_to_csv.append([ii, i.mu, i.sigma])
    npar_data = np.array(data_ar_to_csv)
    csv_to_save = pd.DataFrame(data=npar_data, columns=['ID', 'mu', 'sigma'])
    csv_to_save.to_csv('octorate.csv')
    print ('complete')