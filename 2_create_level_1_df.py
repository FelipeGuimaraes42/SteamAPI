import warnings
from decouple import config
from steam import Steam

from utils.private_ids import *
from utils.api import *
from utils.dataframe_manipulation import *

warnings.filterwarnings("ignore")

API_KEY = config("STEAM_API_KEY")
steam = Steam(API_KEY)

privateIdsList = getPrivateIdsList() # List has steamid's of users that we cannot get friends lists from.

df = pd.read_csv('databases/api_prepared_root_df.csv')
df.set_index("steamid", inplace=True)

# Workaround to lists of dictionaries representing friends to a given dataframe cell.
friends = []
for i in range(len(df)):
    user_id = df.index[i]
    try:
        friends.append(ast.literal_eval(df.iloc[i].friendsList))
    except Exception as e:
        print(e)
        print('Error on row i=',i,'and steamid=',user_id)
        print('There should be no errors when converting lists to dictionaries.')

df['friendsList'] = friends
# ----------------------------------------------------------------------------------

start = 0

for i in range(start, len(df)):
#for i in range(1):
    index = df.index[i]
    friendsList = df.iloc[i].friendsList
    
    for j in range(len(friendsList)):
    #for j in range(3):
        try:
            user, user_id = getUserDataFromId(steam, friendsList[j]['steamid'])

            if (user_id not in privateIdsList and user_id not in df.index.values):
                print('Getting data of j-th friend:', j, 'whose steamid =', user_id, 'from the list of friends of the i-th root user:', i, 'whose steamid = ', index)

                new_row = pd.DataFrame(data=user).T
                new_row.set_index("steamid", inplace=True)
                df = pd.concat([df, new_row])
                
                # Get friends
                api_url = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={API_KEY}&steamid={user_id}&relationship=friend&format=json'
                json_data = makeRequest(api_url)
                try:
                    df.loc[user_id, 'friendsCount'] = len(json_data['friendslist']['friends'])
                    df.loc[user_id, 'friendsList'] = str(json_data['friendslist']['friends'])

                except:
                    if(user_id not in privateIdsList):
                        print('New private user found. Adding steamid = ', user_id, 'to privateIdsList')
                        privateIdsList.append(user_id)
                    df.loc[user_id, 'friendsCount'] = np.nan
                    df.loc[user_id, 'friendsList'] = np.nan

                # Get games
                json_data = steam.users.get_owned_games(user_id)
                try:
                    df.loc[user_id, 'ownedGamesCount'] = len(json_data.get('games'))
                    df.loc[user_id, 'ownedGamesList'] = str(json_data.get('games'))
                except:
                    df.loc[user_id, 'ownedGamesCount'] = 0
                    df.loc[user_id, 'ownedGamesList'] = np.nan

                columns_to_drop = ['avatar', 'avatarfull', 'avatarhash', 'avatarmedium', 'personaname', 'realname']
                df.drop(columns=columns_to_drop, inplace=True)
                df.to_csv("temp_level_1.csv", index=True)
            else:
                print('steamid = ', user_id, 'is private. Skipping...')
                df.to_csv("temp_level_1.csv", index=True)
        except:
            df.to_csv("temp_level_1.csv", index=True)

# Save results
saveData(df, 'level_1.csv', privateIdsList)
