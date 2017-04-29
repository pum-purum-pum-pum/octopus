import pandas as pd
import numpy as np
import datetime as dt
from collections import defaultdict, OrderedDict
import xgboost as xgb
import  os
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss, accuracy_score
import pickle
script_path = os.path.dirname(os.path.realpath(__file__))

class Dataset:
    def __init__(self, games, players, odds, ratings):
        self.games = games
        self.players = players
        self.odds = odds
        self.ratings = ratings

def solo_name(name):
    return '/' not in name

def get_description_to_id_dict(games_data):
    """
    description is a set of 4 ids:
    1) id of the first player
    2) id of the second player
    3) tournament id
    4) round id
    This 4 ids uniquely determine the game.
    :return: correspondence (dict) between game description and game id
    """
    description_to_id = {}
    for id_game, id_p1, id_p2, id_t, id_r in games_data[['ID_G', 'ID1_G', 'ID2_G', 'ID_T_G', 'ID_R_G']].values:
        description_to_id[id_p1, id_p2, id_t, id_r] = id_game
        description_to_id[id_p2, id_p1, id_t, id_r] = id_game
    return description_to_id

def get_id_to_description_dict(games_data):
    id_to_description = {}
    for id_game, id_p1, id_p2, id_t, id_r in games_data[['ID_G', 'ID1_G', 'ID2_G', 'ID_T_G', 'ID_R_G']].values:
        id_to_description[id_game] = (id_p1, id_p2, id_t, id_r)
    return id_to_description

def get_matches_players_id(games_data):
    return games_data[['ID1_G', 'ID2_G']].as_matrix()

def get_dict_from_id_to_name(players_data):
    return dict((i[0], i[1]) for i in players_data[['ID_P', 'NAME_P']].as_matrix())

def get_dict_from_name_to_id(players_data):
    return dict((i[1], i[0]) for i in players_data[['ID_P', 'NAME_P']].as_matrix())

def read_players_table(filename, enc, clear_two_names):
    players_data = pd.read_csv(filename, encoding=enc)
    if clear_two_names:
        select_names = np.array([solo_name(i) for i in players_data['NAME_P']])
        players_data = players_data[select_names]
        
    return players_data

def read_games_table(filename, enc):
    """
    Reads games table from csv file. Adds ID column and replaces DATE_G string with datetime.date object
    """
    games_data = pd.read_csv(filename, encoding=enc)
    games_data['ID_G'] = games_data.index.set_names('ID_G')
    games_data.DATE_G = games_data.DATE_G.apply(lambda date: np.nan if date is np.nan else
                                                dt.datetime.strptime(date, '%m/%d/%y %H:%M:%S').date())
    games_data.sort_values("DATE_G", inplace=True)
    
    return games_data

def read_odds_table(filename, games_data, enc):
    odds_data = pd.read_csv(filename, encoding=enc)
    description_to_id = get_description_to_id_dict(games_data)
    games_id = []
    for id_p1, id_p2, id_t, id_r in odds_data[['ID1_O', 'ID2_O', 'ID_T_O', 'ID_R_O']].values:
        games_id.append(description_to_id.get((id_p1, id_p2, id_t, id_r), None))
    odds_data['ID_G_O'] = games_id
    
    return odds_data

def read_ratings_table(filename, enc):
    """
    Reads ratings table from csv file. Replaces DATE_R string with datetime.date object
    """
    ratings_data = pd.read_csv(filename, encoding=enc)
    ratings_data.DATE_R = ratings_data.DATE_R.apply(lambda date: np.nan if date is np.nan else
                                                    dt.datetime.strptime(date, '%m/%d/%y %H:%M:%S').date())
    ratings_data.sort_values("DATE_R", inplace=True)
    
    return ratings_data

def load_dataset(dataset_path=script_path + '/../data/dataset/', clear_two_names=True, enc=None):
    players = read_players_table(dataset_path + 'players_atp.csv', enc, clear_two_names)
    games = read_games_table(dataset_path + 'games_atp.csv', enc)
    odds = read_odds_table(dataset_path + 'odds_atp.csv', games, enc)
    ratings = read_ratings_table(dataset_path + 'ratings_atp.csv', enc)
    return Dataset(games, players, odds, ratings)
    

def generate_train_sample(dataset):
    player_history = defaultdict(list)
    for date, player, rating, rank in dataset.ratings[['DATE_R', 'ID_P_R', 'POINT_R', 'POS_R']].values:
        player_history[player].append((date, rating, rank))
    
    def get_rating_and_rank(player_id, cur_date):
        latest_rating = np.nan
        latest_rank = np.nan
        latest_date = np.nan
        for date, rating, rank in player_history[player_id]:
            if date is None or date <= cur_date:
                latest_date = date
                latest_rating = rating
                latest_rank = rank
        return latest_rating, latest_rank
        
    wins_count = defaultdict(int)
    games_count = defaultdict(int)
    player_results = defaultdict(list)
    last_game_date = {}
    opponents = defaultdict(list)
    defeated_opponents = defaultdict(list)
    
    meetings_count = defaultdict(int)
    meeting_wins_count = defaultdict(int)
    meeting_results = defaultdict(list)
    
    f_rating1 = []
    f_rank1 = []
    f_results1 = []
    f_games1 = []
    f_winrate1 = []
    f_after_game_period1 = []
    f_after_injury_period1 = []
    f_last_injury_type1 = []
    
    f_rating2 = []
    f_rank2 = []
    f_results2 = []
    f_games2 = []
    f_winrate2 = []
    f_after_game_period2 = []
    f_after_injury_period2 = []
    f_last_injury_type2 = []
    
    f_rating_diff = []
    f_rank_diff = []
    f_games_diff = []
    f_winrate_diff = []
    f_after_game_period_diff = []

    f_meetings_count = []
    f_winrate = []
    f_meeting_results = []
    f_indirect_score = []
    
    label = []
    
    for index, (p1, p2, date) in enumerate(dataset.games[['ID1_G', 'ID2_G', 'DATE_G']].values):
        if date is not np.nan:
            rating1, rank1 = get_rating_and_rank(p1, date)
            rating2, rank2 = get_rating_and_rank(p2, date)
            
            games1 = games_count[p1]
            games2 = games_count[p2]
            
            wins1 = wins_count[p1]
            wins2 = wins_count[p2]
            
            winrate1 = np.nan if games1 == 0 else wins1 / games1
            winrate2 = np.nan if games2 == 0 else wins2 / games2
            
            results1 = player_results[p1][-5:]
            results2 = player_results[p2][-5:]
            
            
            after_game_period1 = np.nan if p1 not in last_game_date else (date - last_game_date[p1]).days
            after_game_period2 = np.nan if p2 not in last_game_date else (date - last_game_date[p2]).days
            
            opponents1 = opponents[p1]
            opponents2 = opponents[p2]
            
            common_opponents = set(opponents1) & set(opponents2)
            
            defeated_opponents1 = defeated_opponents[p1]
            defeated_opponents2 = defeated_opponents[p2]
            
            defeated_common_opponents1 = [op for op in defeated_opponents1 if op in common_opponents]
            defeated_common_opponents2 = [op for op in defeated_opponents2 if op in common_opponents]
            
            meetings = meetings_count[min(p1, p2), max(p1, p2)]
            wins = wins_count[(p1, p2)]
            winrate = np.nan if meetings == 0 else wins / meetings
            pair_results = np.array(meeting_results[(p1, p2)][-5:])
            
            
            if len(common_opponents) == 0:
                indirect_score = np.nan
            else:
                indirect_score = (len(defeated_common_opponents1) - len(defeated_common_opponents2)) / len(common_opponents)
                
            ''' ******************************************************************  '''
            
            f_rating1.append(rating1)
            f_rank1.append(rank1)
            f_results1.append(results1)
            f_games1.append(games1)
            f_winrate1.append(winrate1)
            f_after_game_period1.append(after_game_period1)
            
            f_rating2.append(rating2)
            f_rank2.append(rank2)
            f_results2.append(results2)
            f_games2.append(games2)
            f_winrate2.append(winrate2)
            f_after_game_period2.append(after_game_period2)
            
            f_rating_diff.append(rating1 - rating2)
            f_rank_diff.append(rank1 - rank2)
            f_games_diff.append(games1 - games2)
            f_winrate_diff.append(winrate1 - winrate2)
            f_after_game_period_diff.append(after_game_period1 - after_game_period2)
            
            f_meetings_count.append(meetings)
            f_winrate.append(winrate)
            f_meeting_results.append(pair_results)
            f_indirect_score.append(indirect_score) 
            
            label.append(1)
            
            ''' ******************************************************************  '''
            
            f_rating1.append(rating2)
            f_rank1.append(rank2)
            f_results1.append(results2)
            f_games1.append(games2)
            f_winrate1.append(winrate2)
            f_after_game_period1.append(after_game_period2)
            
            f_rating2.append(rating1)
            f_rank2.append(rank1)
            f_results2.append(results1)
            f_games2.append(games1)
            f_winrate2.append(winrate1)
            f_after_game_period2.append(after_game_period1)
            
            f_rating_diff.append(rating2 - rating1)
            f_rank_diff.append(rank2 - rank1)
            f_games_diff.append(games2 - games1)
            f_winrate_diff.append(winrate2 - winrate1)
            f_after_game_period_diff.append(after_game_period2 - after_game_period1)
            
            f_meetings_count.append(meetings)
            f_winrate.append(1 - winrate)
            f_meeting_results.append(1 - pair_results)
            f_indirect_score.append(-indirect_score) 
            
            label.append(0)
            
            ''' ******************************************************************  '''
            
            
            games_count[p1] += 1
            games_count[p2] += 1
            
            wins_count[p1] += 1
            
            player_results[p1].append(1)
            player_results[p2].append(0)
            
            last_game_date[p1] = date
            last_game_date[p2] = date
            
            opponents[p1].append(p2)
            opponents[p2].append(p1)
            
            defeated_opponents[p1].append(p2)
            
            meetings_count[min(p1, p2), max(p1, p2)] += 1
            wins_count[(p1, p2)] += 1
            meeting_results[(p1, p2)].append(1)
            meeting_results[(p2, p1)].append(0)
            
    f_results1 = np.array([[np.nan if 5 - i > len(result) else result[-5 + i] for i in range(5)] 
                          for result in f_results1])
    f_results2 = np.array([[np.nan if 5 - i > len(result) else result[-5 + i] for i in range(5)] 
                          for result in f_results2])
    f_meeting_results = np.array([[np.nan if 5 - i > len(result) else result[-5 + i] for i in range(5)] 
                                 for result in f_meeting_results])
        
    sample = pd.DataFrame(OrderedDict({'rating1': f_rating1, 
                                       'rank1': f_rank1, 
                                       'results11': f_results1[:, 0],
                                       'results12': f_results1[:, 1],
                                       'results13': f_results1[:, 2],
                                       'results14': f_results1[:, 3],
                                       'results15': f_results1[:, 4],
                                       'games1': f_games1,
                                       'winrate1': f_winrate1,
                                       'afret_game_period1': f_after_game_period1,
                                       
                                       'rating2': f_rating2, 
                                       'rank2': f_rank2, 
                                       'results21': f_results2[:, 0],
                                       'results22': f_results2[:, 1],
                                       'results23': f_results2[:, 2],
                                       'results24': f_results2[:, 3],
                                       'results25': f_results2[:, 4],
                                       'games2': f_games2,
                                       'winrate2': f_winrate2,
                                       'afret_game_period2': f_after_game_period2,
                                       
                                       'rating_diff': f_rating_diff,
                                       'rank_diff': f_rank_diff,
                                       'games_diff': f_games_diff,
                                       'winrate_diff': f_winrate_diff,
                                       'after_game_period_diff': f_after_game_period_diff,
                                       
                                       'meetings': f_meetings_count,
                                       'winrate': f_winrate,
                                       'meeting_retults1': f_meeting_results[:, 0],
                                       'meeting_retults2': f_meeting_results[:, 1],
                                       'meeting_retults3': f_meeting_results[:, 2],
                                       'meeting_retults4': f_meeting_results[:, 3],
                                       'meeting_retults5': f_meeting_results[:, 4],
                                       'indirect_score': f_indirect_score,
                                       
                                       'label': label}))
    
    
    indices = np.arange(sample.shape[0])
    np.random.shuffle(indices)
    
    return sample.ix[indices]

def train_model(dataset):
    sample = generate_train_sample(dataset)
    X = sample[sample.columns[:-1]].values
    y = sample[sample.columns[-1]].values
    model = xgb.XGBClassifier(n_estimators=1000)
    model.fit(X_train, y_train)
    
    return model

def save_model(model, filename):
    pickle.dump(model, open(filename, 'wb'))
    
def load_model(filename):
    return pickle.load(open(filename, 'rb'))

def generate_features(dataset):
    player_history = defaultdict(list)
    for date, player, rating, rank in dataset.ratings[['DATE_R', 'ID_P_R', 'POINT_R', 'POS_R']].values:
        player_history[player].append((date, rating, rank))

    def get_rating_and_rank(player_id, cur_date):
        latest_rating = np.nan
        latest_rank = np.nan
        latest_date = np.nan
        for date, rating, rank in player_history[player_id]:
            if date is None or date <= cur_date:
                latest_date = date
                latest_rating = rating
                latest_rank = rank
        return latest_rating, latest_rank

    wins_count = defaultdict(int)
    games_count = defaultdict(int)
    player_results = defaultdict(list)
    last_game_date = {}
    opponents = defaultdict(list)
    defeated_opponents = defaultdict(list)

    meetings_count = defaultdict(int)
    meeting_wins_count = defaultdict(int)
    meeting_results = defaultdict(list)

    f_rating = defaultdict(lambda: np.nan)
    f_rank = defaultdict(lambda: np.nan)
    f_results = defaultdict(lambda: np.array([np.nan] * 5))
    f_games = defaultdict(lambda: np.nan)
    f_winrate = defaultdict(lambda: np.nan)
    f_after_game_period = defaultdict(lambda: np.nan)

    f_rating_diff = defaultdict(lambda: np.nan)
    f_rank_diff = defaultdict(lambda: np.nan)
    f_games_diff = defaultdict(lambda: np.nan)
    f_winrate_diff = defaultdict(lambda: np.nan)
    f_after_game_period_diff = defaultdict(lambda: np.nan)

    f_meetings_count = defaultdict(lambda: np.nan)
    f_pair_winrate = defaultdict(lambda: np.nan)
    f_meeting_results = defaultdict(lambda: np.array([np.nan] * 5))
    f_indirect_score = defaultdict(lambda: np.nan)

    for index, (p1, p2, date) in enumerate(dataset.games[['ID1_G', 'ID2_G', 'DATE_G']].values):
        if date is not np.nan:

            rating1, rank1 = get_rating_and_rank(p1, date)
            rating2, rank2 = get_rating_and_rank(p2, date)

            games1 = games_count[p1]
            games2 = games_count[p2]

            wins1 = wins_count[p1]
            wins2 = wins_count[p2]

            winrate1 = np.nan if games1 == 0 else wins1 / games1
            winrate2 = np.nan if games2 == 0 else wins2 / games2

            results1 = player_results[p1][-5:]
            results2 = player_results[p2][-5:]


            after_game_period1 = np.nan if p1 not in last_game_date else (date - last_game_date[p1]).days
            after_game_period2 = np.nan if p2 not in last_game_date else (date - last_game_date[p2]).days

            opponents1 = opponents[p1]
            opponents2 = opponents[p2]

            common_opponents = set(opponents1) & set(opponents2)

            defeated_opponents1 = defeated_opponents[p1]
            defeated_opponents2 = defeated_opponents[p2]

            defeated_common_opponents1 = [op for op in defeated_opponents1 if op in common_opponents]
            defeated_common_opponents2 = [op for op in defeated_opponents2 if op in common_opponents]

            meetings = meetings_count[min(p1, p2), max(p1, p2)]
            wins = wins_count[(p1, p2)]
            winrate = np.nan if meetings == 0 else wins / meetings
            pair_results = np.array(meeting_results[(p1, p2)][-5:])


            if len(common_opponents) == 0:
                indirect_score = np.nan
            else:
                indirect_score = (len(defeated_common_opponents1) - len(defeated_common_opponents2)) / len(common_opponents)



            f_rating[p1] = rating1
            f_rank[p1] = rank1
            f_results[p1] = results1
            f_games[p1] = games1
            f_winrate[p1] = winrate1
            f_after_game_period[p1] = after_game_period1

            f_rating[p2] = rating2
            f_rank[p2] = rank2
            f_results[p2] = results2
            f_games[p2] = games2
            f_winrate[p2] = winrate2
            f_after_game_period[p2] = after_game_period2

            f_rating_diff[(p1, p2)] = rating1 - rating2
            f_rating_diff[(p2, p1)] = rating2 - rating1
            f_rank_diff[(p1, p2)] = rank1 - rank2
            f_rank_diff[(p2, p1)] = rank2 - rank1
            f_games_diff[(p1, p2)] = games1 - games2
            f_games_diff[(p2, p1)] = games2 - games1
            f_winrate_diff[(p1, p2)] = winrate1 - winrate2
            f_winrate_diff[(p2, p1)] = winrate2 - winrate1
            f_after_game_period_diff[(p1, p2)] = after_game_period1 - after_game_period2
            f_after_game_period_diff[(p2, p1)] = after_game_period2 - after_game_period1

            f_pair_winrate[(p1, p2)] = winrate
            f_pair_winrate[(p2, p1)] = 1 - winrate

            f_meetings_count[(p1, p2)] = meetings
            f_meetings_count[(p2, p1)] = meetings

            f_meeting_results[(p1, p2)] = pair_results
            f_meeting_results[(p2, p1)] = 1 - pair_results

            f_indirect_score[(p1, p2)] = indirect_score
            f_indirect_score[(p2, p1)] = indirect_score



            games_count[p1] += 1
            games_count[p2] += 1

            wins_count[p1] += 1

            player_results[p1].append(1)
            player_results[p2].append(0)

            last_game_date[p1] = date
            last_game_date[p2] = date

            opponents[p1].append(p2)
            opponents[p2].append(p1)

            defeated_opponents[p1].append(p2)

            meetings_count[min(p1, p2), max(p1, p2)] += 1
            wins_count[(p1, p2)] += 1
            meeting_results[(p1, p2)].append(1)
            meeting_results[(p2, p1)].append(0)


    f_results = defaultdict(lambda: np.array([np.nan] * 5), 
                            {player: [np.nan if 5 - i > len(result) else result[-5 + i] for i in range(5)] 
                                      for player, result in f_results.items()})
    f_meeting_results = defaultdict(lambda: np.array([np.nan] * 5), 
                                    {pair: [np.nan if 5 - i > len(result) else result[-5 + i] for i in range(5)] 
                                            for pair, result in f_meeting_results.items()})


    players = list(dataset.players.ID_P.unique())
    f_rating = np.array([f_rating[player] for player in players]).reshape(-1, 1)
    f_rank = np.array([f_rank[player] for player in players]).reshape(-1, 1)
    f_results = np.array([f_results[player] for player in players]).reshape(-1, 5)
    f_games = np.array([f_games[player] for player in players]).reshape(-1, 1)
    f_winrate = np.array([f_winrate[player] for player in players]).reshape(-1, 1)
    f_after_game_period = np.array([f_after_game_period[player] for player in players]).reshape(-1, 1)

    pairs = list(f_rating_diff.keys())
    f_rating_diff = np.array([f_rating_diff[pair] for pair in pairs]).reshape(-1, 1)
    f_rank_diff = np.array([f_rank_diff[pair] for pair in pairs]).reshape(-1, 1)
    f_games_diff = np.array([f_games_diff[pair] for pair in pairs]).reshape(-1, 1)
    f_winrate_diff = np.array([f_winrate_diff[pair] for pair in pairs]).reshape(-1, 1)
    f_after_game_period_diff = np.array([f_after_game_period_diff[pair] for pair in pairs]).reshape(-1, 1)
    f_meetings_count = np.array([f_meetings_count[pair] for pair in pairs]).reshape(-1, 1)
    f_pair_winrate = np.array([f_pair_winrate[pair] for pair in pairs]).reshape(-1, 1)
    f_meeting_results = np.array([f_meeting_results[pair] for pair in pairs]).reshape(-1, 5)
    f_indirect_score = np.array([f_indirect_score[pair] for pair in pairs]).reshape(-1, 1)

    player_features = np.hstack([f_rating, f_rank, f_results, f_games, f_winrate, f_after_game_period])
    pair_features = np.hstack([f_rating_diff, f_rank_diff, f_games_diff, f_winrate_diff, 
                               f_after_game_period_diff, f_meetings_count, f_pair_winrate, 
                               f_meeting_results, f_indirect_score])

    player_features = pd.DataFrame(player_features, index=players, 
                                   columns=['rating', 'rank', 'results1', 'results3',
                                            'results3', 'results4', 'results5', 'games', 
                                            'winrate', 'after_game_period'])

    pair_features = pd.DataFrame(pair_features, index=pairs, 
                                 columns=['rating_diff', 'rank_diff', 'games_diff', 
                                          'winrate_diff', 'after_game_period_diff', 
                                          'meetings_count', 'pair_winrate', 
                                          'meeting_results1', 'meeting_results2',
                                          'meeting_results3', 'meeting_results4',
                                          'meeting_results5', 'indirect_score'])
    
    return player_features, pair_features


def predict(p1, p2):
    model = load_model(script_path + '/../data/model')
    
    player_features = pd.read_csv(script_path + '/../data/players.csv', index_col=0)
    pair_features = pd.read_csv(script_path + '/../data/pairs.csv', index_col=0)
    
    if p1 in player_features.index:
        player1_features = player_features[player_features.index == p1].values[0]
    else:
        player1_features = [np.nan] * player_features.shape[1]
        
    if p2 in player_features.index:
        player2_features = player_features[player_features.index == p2].values[0]
    else:
        player2_features = [np.nan] * player_features.shape[1]
        
    
    key = '({}, {})'.format(p1, p2)
    if key in pair_features.index:
        pair_features = pair_features[pair_features.index == key].values[0]
    else:
        pair_features = [np.nan] * pair_features.shape[1]
        
    return model.predict_proba([np.concatenate([player1_features, player2_features, pair_features])])
