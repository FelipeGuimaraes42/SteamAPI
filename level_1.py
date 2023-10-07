import warnings
from decouple import config
from steam import Steam

from utils.private_ids import *
from utils.api import *
from utils.dataframe_manipulation import *

warnings.filterwarnings("ignore")

# Study the Web API documentation. Create a function for each case. Use them, test results on different occasions. See what comes of it.
# https://developer.valvesoftware.com/wiki/Steam_Web_API

API_KEY = config("STEAM_API_KEY")
steam = Steam(API_KEY)

privateIdsList = (
    getPrivateIdsList()
)  # List has steamid's of users that we cannot get friends lists from.

level_0 = pd.read_csv("level_0.csv")
level_0 = prepareImportedDataframe(level_0)
level_1 = level_0

root_friends_list = level_0.iloc[0].friendsList

# Adding Friends of root -> level 1
for i in range(len(root_friends_list)):
    user, user_id = getUserDataAndId(steam, root_friends_list[i]["steamid"])
    print('Getting data of i-th friend:', i,'whose steamid =', user_id)
    level_1 = addNewRow(level_1, user, user_id)

    # Get friends
    api_url = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={API_KEY}&steamid={user_id}&relationship=friend&format=json'
    json_data = makeRequest(api_url)

    if (user_id not in privateIdsList):
        try:
            level_1.loc[user_id, 'friendsCount'] = len(json_data['friendslist']['friends'])
            level_1.loc[user_id, 'friendsList'] = str(json_data['friendslist']['friends'])

        except:
            if(user_id not in privateIdsList):
                print('New private user found. Adding steamid = ',user_id,'to privateIdsList')
                privateIdsList.append(user_id)
            level_1.loc[user_id, 'friendsCount'] = np.nan
            level_1.loc[user_id, 'friendsList'] = np.nan

        # Get games
        json_data = steam.users.get_owned_games(user_id)
        try:
            level_1.loc[user_id, 'ownedGamesCount'] = len(json_data.get('games'))
            level_1.loc[user_id, 'ownedGamesList'] = str(json_data.get('games'))
        except:
            level_1.loc[user_id, 'ownedGamesCount'] = 0
            level_1.loc[user_id, 'ownedGamesList'] = np.nan
    else:
        print('steamid = ',user_id,'is private. Skipping...')

# Save results
saveData(level_1, 'level_1.csv', privateIdsList)
    
