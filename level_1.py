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
#for i in range(len(root_friends_list)):
for i in range(2):
    user, user_id = getUserDataAndId(steam, root_friends_list[i]["steamid"])
    level_1 = addNewRow(level_1, user, user_id)
    # Get friends
    api_url = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={API_KEY}&steamid={user_id}&relationship=friend&format=json'
    json_data = makeRequest(api_url)
    index = level_1.index.tolist()[-1]
    level_1.loc[index, 'friendsList'] = str(json_data['friendslist']['friends'])
    # TODO: Get games - still not working
    level_1 = getGamesData(steam, level_1, user_id)

# Save results
resultFile = 'level_1.csv'
savePrivateIds(privateIdsList)
level_1.to_csv(resultFile ,index=True)
print('Root dataframe saved to', resultFile)
    
