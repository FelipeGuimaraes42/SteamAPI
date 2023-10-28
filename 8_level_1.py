import json
import time
import warnings
from steam import Steam
from decouple import config

from utils.private_ids import *
from utils.api import *
from utils.dataframe_manipulation import *
from utils.treat_data import *


API_KEY = config("STEAM_API_KEY")
steam = Steam(API_KEY)

warnings.filterwarnings("ignore")

API_KEY = config("STEAM_API_KEY")

df = pd.read_parquet('databases/temp_new_root.parquet')
df.rename_axis('steamid', inplace=True)
root_index = 76561198189629985

output_name = f'temp_level_1'
backup_name = f'temp_backup_level_1'

successCheck = 0
operationsCount = 0
successfullOperationsCount = 0

root_friends_list = json.loads(df.loc[root_index, 'friendsList'])

# For each friend of the root user:
for i in range(len(root_friends_list)):
    successCheck = 0
    user, user_id = getUserDataFromId(steam, root_friends_list[i]['steamid'])
    
    print('Getting games for i-th user,', i,'with steamid =', user_id,'. oppCount =', operationsCount, '. successCount = ', successfullOperationsCount)

    # Making a new row.
    try:
        new_row = pd.DataFrame(data=user).T
        new_row.set_index("steamid", inplace=True)
        df = pd.concat([df, new_row])

        columns_to_keep = [
            "loccityid",
            "loccountrycode",
            "locstatecode",
            "personastate",
            "profileurl",
            "timecreated",
            "friendsCount",
            "friendsList",
            "ownedGamesCount",
            "ownedGamesList",
        ]
        df = df[columns_to_keep]
    # If it fails for any reason
    except:
        print('Getting new row data (basic user data) failed. Skipping user.')
        continue

    # Getting data
    try:
        #Getting friends
        try:
            api_url = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={API_KEY}&steamid={user_id}&relationship=friend&format=json'
            json_data = makeRequest(api_url)
            operationsCount += 1
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
            successCheck += 1
        except Exception as e:
            print(e)
            df.loc[user_id, 'friendsList'] = ''
        # Getting Games
        try:
            api_url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={user_id}&format=json'
            json_data = makeRequest(api_url)
            operationsCount += 1
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
            successCheck += 1
        except Exception as e:
            print(e)
            df.loc[user_id, 'ownedGamesList'] = ''
    # If an unforeseen error occurs when getting more data, save what you currently have.
    except:
        df.drop_duplicates(inplace=True)
        df = saveData(df, output_name)

    if (successCheck == 2):
        successfullOperationsCount += 1
    # Save a backup periodically
    if (operationsCount % 100 == 0):
        print('Total number of operations ==', operationsCount,'. Saving backup.')
        df.drop_duplicates(inplace=True)
        df = saveData(df, backup_name)
        time.sleep(1)

df.drop_duplicates(inplace=True)
df = saveData(df, output_name)