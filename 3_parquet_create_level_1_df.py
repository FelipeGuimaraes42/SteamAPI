import warnings
from decouple import config
from steam import Steam

from utils.private_ids import *
from utils.api import *
from utils.dataframe_manipulation import *
from utils.treat_data import *

warnings.filterwarnings("ignore")

API_KEY = config("STEAM_API_KEY")
steam = Steam(API_KEY)

privateIdsList = getPrivateIdsList() # List has steamid's of users that we cannot get friends lists from.
root_df = pd.read_csv('databases/api_prepared_root_df.csv')
root_df.set_index("steamid", inplace=True)

# Workaround to lists of dictionaries representing friends to a given dataframe cell.
friends = []
for i in range(len(root_df)):
    user_id = root_df.index[i]
    try:
        friends.append(ast.literal_eval(root_df.iloc[i].friendsList))
    except Exception as e:
        print(e)
        print('Error on row i=',i,'and steamid=',user_id)
        print('There should be no errors when converting lists to dictionaries.')

root_df['friendsList'] = friends

# ----------------------------------------------------------------------------------

# Database must be stored as temp because we cannot version files larger than 100mb in github.
start = 444
# Iterate only the first 500 rows. Otherwise the dataframe will be too large. 
end = 500

level_1 = pd.read_parquet(f'databases/temp_api_level_1_ate_{start}.parquet')
output_name = f'temp_api_level_1_ate_{end}'
backup_name = f'temp_api_level_1_ate_{end}_backup'

operationCount = 0

# Iterate only the first 500 rows. Otherwise the dataframe will be too large. 
for i in range(start, end):
    index = root_df.index[i]
    friendsList = root_df.iloc[i].friendsList
    
    for j in range(len(friendsList)):
        try:
            user, user_id = getUserDataFromId(steam, friendsList[j]['steamid'])

            if(user_id in privateIdsList or user_id in level_1.index.values):
                print('Data of j-th friend:', j, 'whose steamid =', user_id, 'skipped.')
                continue

            print('Getting data of j-th friend:', j, 'whose steamid =', user_id, 'from the list of friends of the i-th root user:', i, 'whose steamid = ', index)

            new_row = pd.DataFrame(data=user).T
            new_row.set_index("steamid", inplace=True)
            level_1 = pd.concat([level_1, new_row])
            
            # Get friends
            api_url = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={API_KEY}&steamid={user_id}&relationship=friend&format=json'
            json_data = makeRequest(api_url)
            try:
                level_1.loc[user_id, 'friendsCount'] = len(json_data['friendslist']['friends'])
                level_1.loc[user_id, 'friendsList'] = str(json_data['friendslist']['friends'])
            except:
                if(user_id not in privateIdsList):
                    # print('New private user found. Adding steamid = ', user_id, 'to privateIdsList')
                    privateIdsList.append(user_id)
                    savePrivateIds(privateIdsList)
                level_1.loc[user_id, 'friendsCount'] = np.nan
                level_1.loc[user_id, 'friendsList'] = np.nan

            # Get games
            json_data = steam.users.get_owned_games(user_id)
            try:
                # OwnedGamesCount not working correctly. Remebemr to add it according at a later moment.
                level_1.loc[user_id, 'ownedGamesCount'] = len(json_data.get('games'))
                level_1.loc[user_id, 'ownedGamesList'] = str(json_data.get('games'))
            except:
                level_1.loc[user_id, 'ownedGamesCount'] = 0
                level_1.loc[user_id, 'ownedGamesList'] = np.nan

            operationCount += 1
            # Save an immediate backup for the sake of visibility.
            if (operationCount == 1):
                level_1 = treatAndSaveData(level_1, output_name)
            # Save a backup every 100 operations.
            if (operationCount) % 100 == 0:
                print('Total number of operations ==', operationCount,'. Saving backup.')
                savePrivateIds(privateIdsList)
                level_1 = treatAndSaveData(level_1, backup_name)

        except:
            savePrivateIds(privateIdsList)
            level_1 = treatAndSaveData(level_1, output_name)

# Save results
savePrivateIds(privateIdsList)
level_1 = treatAndSaveData(level_1, output_name)
