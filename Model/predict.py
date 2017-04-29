from model import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--id1', type=int, help="player1 id")
parser.add_argument('--id2', type=int, help="player2 id")
args = parser.parse_args()


if __name__ == "__main__":
    p = predict(args.id1, args.id2)[0][1]
    print(p)
