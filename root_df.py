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

scaped_df = pd.read_csv('databases/scraped_data.csv')
scaped_df.drop(columns=['Unnamed: 0'], inplace=True)

root_df = pd.read_csv('databases/api_level_0.csv')
root_df.set_index("steamid", inplace=True)

#for i in range(len(scaped_df)):
for i in range(10):
    try:
        user, user_id = getUserDataFromId(steam, scaped_df.loc[i,'Id'])

        if (user_id not in privateIdsList):
            print('Getting data of i-th root user:', i, 'whose steamid =', user_id)

            new_row = pd.DataFrame(data=user).T
            new_row.set_index("steamid", inplace=True)
            root_df = pd.concat([root_df, new_row])
            
            # Get friends
            api_url = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={API_KEY}&steamid={user_id}&relationship=friend&format=json'
            json_data = makeRequest(api_url)
            try:
                root_df.loc[user_id, 'friendsCount'] = len(json_data['friendslist']['friends'])
                root_df.loc[user_id, 'friendsList'] = str(json_data['friendslist']['friends'])

            except:
                if(user_id not in privateIdsList):
                    print('New private user found. Adding steamid = ', user_id, 'to privateIdsList')
                    privateIdsList.append(user_id)
                root_df.loc[user_id, 'friendsCount'] = np.nan
                root_df.loc[user_id, 'friendsList'] = np.nan

            # Get games
            json_data = steam.users.get_owned_games(user_id)
            try:
                root_df.loc[user_id, 'ownedGamesCount'] = len(json_data.get('games'))
                root_df.loc[user_id, 'ownedGamesList'] = str(json_data.get('games'))
            except:
                root_df.loc[user_id, 'ownedGamesCount'] = 0
                root_df.loc[user_id, 'ownedGamesList'] = np.nan
                
            root_df.to_csv("temp_root_df.csv", index=True)
        else:
            print('steamid = ', user_id, 'is private. Skipping...')
            root_df.to_csv("temp_root_df.csv", index=True)
    except:
        root_df.to_csv("temp_root_df.csv", index=True)
        

# Remove the first row of the dataframe. It contains information of a user that is not a member of the community jogosbra.
root_df = root_df.iloc[1:]

# Save results
saveData(root_df, 'root_df.csv', privateIdsList)
