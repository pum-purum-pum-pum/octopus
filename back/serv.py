from flask import Flask
from flask import request
from Visualization.bookmakers import get_bookmakers_coef
import pandas as pd
import numpy as np
import sqlite3
app = Flask(__name__)
con = sqlite3.connect('../data/on_court.db')


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/bookmakers', methods=['GET'])
def get_bookmakers():
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master")
    player1 = request.args.get('player1')
    player2 = request.args.get('player2')
    print(player1, player2)
    return get_bookmakers_coef(cursor, player1, player2)
