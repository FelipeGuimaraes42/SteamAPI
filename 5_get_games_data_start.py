import json
import warnings
from decouple import config

from utils.private_ids import *
from utils.api import *
from utils.dataframe_manipulation import *
from utils.treat_data import *

warnings.filterwarnings("ignore")

API_KEY = config("STEAM_API_KEY")
df = pd.read_parquet("temp_api_level_1_ate_500_treated.parquet")
df = df.drop('ownedGamesList', axis=1)
df['ownedGamesList'] = ['' for _ in range(len(df))]
privateIdsList = getPrivateIdsList()

output_name = 'temp_final'
backup_name = 'temp_final_backup'

start = 0
end = len(df)
end=10
successfullOperationsCount = 0

for i in range(start, end):
    user_id = df.index[i]

    if(user_id in privateIdsList):
        continue
    
    print('Getting games for i-th user,', i,'with steamid =', user_id,'. successfullOperationsCount =', successfullOperationsCount)

    try:
        api_url = f'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={user_id}&format=json'
        json_data = makeRequest(api_url)
        games_data = json_data.get('response').get('games')
        print(games_data)
        try:
            if(str(type(games_data)) == "<class 'NoneType'>"):
                continue

            games_data_str = json.dumps(games_data)
            if (json.loads(games_data_str) != games_data):
                raise Exception("Failure converting string of ownedGames to list of objects.")
            
            df.loc[user_id, 'ownedGamesCount'] = json_data.get('response').get('game_count')
            df.loc[user_id, 'ownedGamesList'] = games_data_str
            successfullOperationsCount += 1
        except Exception as e:
            print(e)
            df.loc[user_id, 'ownedGamesCount'] = 0
            df.loc[user_id, 'ownedGamesList'] = ''

        # Save an immediate backup for the sake of visibility.
        if (successfullOperationsCount == 1):
            df = saveData(df, output_name)
        # Save a backup every 100 successfull operations.
        if (successfullOperationsCount) % 100 == 0:
            print('Total number of successfull operations ==', successfullOperationsCount,'. Saving backup.')
            savePrivateIds(privateIdsList)
            df = saveData(df, backup_name)
    except:
        savePrivateIds(privateIdsList)
        df = saveData(df, output_name)

# Save results
savePrivateIds(privateIdsList)
df = saveData(df, output_name)