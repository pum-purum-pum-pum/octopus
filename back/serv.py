from flask import Flask
from flask import request
from Visualization.bookmakers import get_bookmakers_coef
from Visualization.individual_features import win_rate
from Model.octorate import win_prob

import pandas as pd
import numpy as np
import sqlite3
app = Flask(__name__)
con = sqlite3.connect('../data/on_court.db')
cursor = con.cursor()
# cursor.execute("SELECT * FROM sqlite_master")


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/bookmakers', methods=['GET'])
def get_bookmakers():
    player1 = request.args.get('player1')
    player2 = request.args.get('player2')
    return get_bookmakers_coef(cursor, player1, player2)


@app.route('/win_rate', methods=['GET'])
def get_win_rate():
    player1 = request.args.get('player1')
    player2 = request.args.get('player2')
    return win_rate(cursor, player1, player2)


@app.route('/prob', methods=['GET'])
def get_win_prob():
    player1 = request.args.get('player1')
    player2 = request.args.get('player2')
    return win_prob(cursor, player1, player2)