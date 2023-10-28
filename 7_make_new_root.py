import json
import warnings
from decouple import config

from utils.private_ids import *
from utils.api import *
from utils.dataframe_manipulation import *
from utils.treat_data import *

warnings.filterwarnings("ignore")

API_KEY = config("STEAM_API_KEY")
old_df = pd.read_parquet("databases/temp_games_data_redone.parquet")
old_df = old_df.drop_duplicates()

df = pd.DataFrame(columns=old_df.columns)
root_index = 76561198189629985
df = pd.concat([df, old_df.loc[root_index:root_index]])

output_name = f'temp_new_root'

def getFriends(df, user_id):
    api_url = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={API_KEY}&steamid={user_id}&relationship=friend&format=json'
    json_data = makeRequest(api_url)
    friends_data = json_data.get('friendslist').get('friends')
    friends_count = len(friends_data)
    friendsDataEmpty = str(type(friends_data)) == "<class 'NoneType'>"
    friendsCountEmpty = str(type(friends_count)) == "<class 'NoneType'>"

    if(friendsCountEmpty):
        df.loc[user_id, 'friendsCount'] = 0
    else:
        df.loc[user_id, 'friendsCount'] = friends_count

    if(friendsDataEmpty):
        raise Exception("No friends data received.")

    friends_data_str = json.dumps(friends_data)
    if (json.loads(friends_data_str) != friends_data):
        raise Exception("Failure converting string of ownedGames to list of objects.")
    
    df.loc[user_id, 'friendsList'] = friends_data_str

def getGames(df, user_id):
    api_url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={user_id}&format=json'
    json_data = makeRequest(api_url)
    games_data = json_data.get('response').get('games')
    games_count = json_data.get('response').get('game_count')
    gamesDataEmpty = str(type(games_data)) == "<class 'NoneType'>"
    gamesCountEmpty = str(type(games_count)) == "<class 'NoneType'>"

    if(gamesCountEmpty):
        df.loc[user_id, 'ownedGamesCount'] = 0
    else:
        df.loc[user_id, 'ownedGamesCount'] = games_count

    if(gamesDataEmpty):
        raise Exception("No game data received.")

    games_data_str = json.dumps(games_data)
    if (json.loads(games_data_str) != games_data):
        raise Exception("Failure converting string of ownedGames to list of objects.")
    
    df.loc[user_id, 'ownedGamesList'] = games_data_str

try:
    getFriends(df, root_index)
except Exception as e:
    print(e)
    df.loc[root_index, 'friendsList'] = ''
try:
    getGames(df, root_index)
except Exception as e:
    print(e)
    df.loc[root_index, 'ownedGamesList'] = ''

df = saveData(df, output_name)