import sys
import pandas as pd
from trueskill import Rating
import argparse

sys.path.append("..")
from Model.octorate import win_probability_by_rate
def win_prob_from_csv(octorate, pid1, pid2):
    p1 = octorate[octorate['ID']==pid1].as_matrix()[0]
    p2 = octorate[octorate['ID']==pid2].as_matrix()[0]
    return win_probability_by_rate(Rating(mu=p1[1], sigma=p1[2]), Rating(mu=p2[1], sigma=p2[2]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='input output files')
    parser.add_argument('--id1', type=int, help="player1 id")
    parser.add_argument('--id2', type=int, help="player2 id")

    args = parser.parse_args()
    octorate = pd.read_csv('octorate.csv')
    print(win_prob_from_csv(octorate, args.id1, args.id2))