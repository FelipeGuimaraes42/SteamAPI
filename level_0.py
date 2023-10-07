import warnings
from decouple import config
from steam import Steam

from utils.private_ids import *
from utils.api import *
from utils.dataframe_manipulation import saveData

warnings.filterwarnings("ignore")

# Study the Web API documentation. Create a function for each case. Use them, test results on different occasions. See what comes of it.
# https://developer.valvesoftware.com/wiki/Steam_Web_API

API_KEY = config("STEAM_API_KEY")
steam = Steam(API_KEY)

privateIdsList = getPrivateIdsList() # List has steamid's of users that we cannot get friends lists from.

# Get one of the users in the top of the steam friends ladder in https://steamladder.com/ladder/friends/
root_df, root_user, root_user_id = createDataframeFromRoot(steam, "76561198070799736")
root_df = getRootFriendsList(root_df, root_user_id, privateIdsList, API_KEY)
root_df = getRootGamesData(steam, root_df, root_user_id)

# Save results
saveData(root_df, 'level_0.csv', privateIdsList)
