import json
import warnings
import time
from decouple import config

from utils.private_ids import *
from utils.api import *
from utils.dataframe_manipulation import *
from utils.treat_data import *

warnings.filterwarnings("ignore")

API_KEY = config("STEAM_API_KEY")
df = pd.read_parquet("databases/temp_api_level_1_ate_500_treated.parquet")
df = df.drop('ownedGamesList', axis=1)
df = df.drop_duplicates()
df['ownedGamesList'] = ['' for _ in range(len(df))]

privateIdsList = getPrivateIdsList()
start = 0
end = len(df)

operationsCount = 0
successfullOperationsCount = 0

output_name = f'temp_start_at_{start}'
backup_name = f'temp_start_at_{start}'

for i in range(start, end):
    user_id = df.index[i]

    if(user_id in privateIdsList):
        continue
    
    print('Getting games for i-th user,', i,'with steamid =', user_id,'. oppCount =', operationsCount, '. successCount = ', successfullOperationsCount)

    try:
        api_url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={user_id}&format=json'
        json_data = makeRequest(api_url)
        operationsCount += 1
        games_data = json_data.get('response').get('games')
        games_count = json_data.get('response').get('game_count')
        gamesDataEmpty = str(type(games_data)) == "<class 'NoneType'>"
        gamesCountEmpty = str(type(games_count)) == "<class 'NoneType'>"
        try:
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
            successfullOperationsCount += 1
        except Exception as e:
            print(e)
            df.loc[user_id, 'ownedGamesList'] = ''

        # Save an immediate backup for the sake of visibility.
        if (operationsCount == 1):
            df = saveData(df, output_name)
        # Save a backup periodically
        if (operationsCount % 100 == 0):
            print('Total number of operations ==', operationsCount,'. Saving backup.')
            savePrivateIds(privateIdsList)
            df = saveData(df, backup_name)
            time.sleep(5)
    except:
        savePrivateIds(privateIdsList)
        df = saveData(df, output_name)

# Save results
savePrivateIds(privateIdsList)
df = saveData(df, output_name)