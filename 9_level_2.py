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

level_1 = pd.read_parquet('databases/temp_level_1.parquet')
level_1.rename_axis('steamid', inplace=True)
df = pd.read_parquet('databases/temp_backup_level_2_start_at_0.parquet')

start = 25
end_of_level_1 = len(level_1)
output_name = f'temp_level_2_start_at_{start}'
backup_name = f'temp_backup_level_2_start_at_{start}'

successCheck = 0
operationsCount = 0
successfullOperationsCount = 0

log_file_path = 'log.txt'

# For each friend of the root user:
for i in range(start, end_of_level_1):
    index = level_1.index[i]

    # Try converting friendsList string to json. Continue if any error occurs or if the list is empty.
    try:
        if str(type(level_1.loc[index, 'friendsList'])) == "<class 'NoneType'>" or level_1.loc[index, 'friendsList'] == '':
            continue
        friendsList = json.loads(level_1.loc[index, 'friendsList'])
    except Exception as e:
        print(e)
        continue

    # For each friend of said friend of the root user:
    for j in range(len(friendsList)):
        
        try:
            if str(type(friendsList[j])) == "<class 'NoneType'>" or friendsList[j] == '':
                continue

            friend_idx = np.int64(friendsList[j].get('steamid'))
            if friend_idx in df.index.values:
                print('User already added')
                continue
        except Exception as e:
            print(e)
            continue

        successCheck = 0

        # Making a new row.
        try:
            user, user_id = getUserDataFromId(steam, friendsList[j]['steamid'])

            logText = 'Getting data of j-th friend:', j, 'whose steamid =', user_id, 'from the list of friends of the i-th root user:', i, 'whose steamid = ', index, 'oppCount =', operationsCount, '. successCount = ', successfullOperationsCount

            with open(log_file_path, 'a') as file:
                file.write(logText)

            print(logText)

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
            successCheck += 1
        # If it fails for any reason
        except Exception as e:
            print(e)
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

        if (successCheck == 3):
            successfullOperationsCount += 1
        # Save a backup periodically
        if (operationsCount % 100 == 0):
            print('Total number of operations ==', operationsCount,'. Saving backup.')
            df.drop_duplicates(inplace=True)
            df = saveData(df, backup_name)
            time.sleep(1)
    # Save data at the end of each i-th root user friendList.
    print('\ni-th root user:', i, 'whose steamid = ', index, 'collection DONE.\n')
    df.drop_duplicates(inplace=True)
    df = saveData(df, output_name)

df.drop_duplicates(inplace=True)
df = saveData(df, output_name)