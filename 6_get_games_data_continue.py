import json
import warnings
from decouple import config

from utils.private_ids import *
from utils.api import *
from utils.dataframe_manipulation import *
from utils.treat_data import *

warnings.filterwarnings("ignore")

API_KEY = config("STEAM_API_KEY")
df = pd.read_parquet("databases/temp_final_backup.parquet")

privateIdsList = getPrivateIdsList()
start = 7400
end = len(df)
output_name = f'temp_final_start_at_{start}'
backup_name = f'temp_final_backup_start_at_{start}'
operationsCount = 0

for i in range(start, end):
    user_id = df.index[i]

    if(user_id in privateIdsList):
        continue
    
    print('Getting games for i-th user,', i,'with steamid =', user_id,'. operationsCount =', operationsCount)

    try:
        api_url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={user_id}&format=json'
        json_data = makeRequest(api_url)
        operationsCount += 1
        games_data = json_data.get('response').get('games')
        try:
            if(str(type(games_data)) == "<class 'NoneType'>"):
                continue

            games_data_str = json.dumps(games_data)
            if (json.loads(games_data_str) != games_data):
                raise Exception("Failure converting string of ownedGames to list of objects.")
            
            df.loc[user_id, 'ownedGamesCount'] = json_data.get('response').get('game_count')
            df.loc[user_id, 'ownedGamesList'] = games_data_str
        except Exception as e:
            print(e)
            df.loc[user_id, 'ownedGamesCount'] = 0
            df.loc[user_id, 'ownedGamesList'] = ''

        # Save an immediate backup for the sake of visibility.
        if (operationsCount == 1):
            df = saveData(df, output_name)
        # Save a backup every 100 operations.
        if (operationsCount) % 100 == 0:
            print('Total number of operations ==', operationsCount,'. Saving backup.')
            savePrivateIds(privateIdsList)
            df = saveData(df, backup_name)
    except:
        savePrivateIds(privateIdsList)
        df = saveData(df, output_name)

# Save results
savePrivateIds(privateIdsList)
df = saveData(df, output_name)