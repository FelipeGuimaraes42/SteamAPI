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

root_df = pd.read_csv('databases/api_root_df.csv')
root_df = prepareRootDataframe(root_df)

for i in range(len(root_df)):
    user_id = root_df.index[i]
    # If a friendsList dictionary is incomplete, remove the incomplete bits.
    friendsListAsString = root_df.loc[user_id, 'friendsList']
    if(not friendsListAsString.endswith(']')):
        modified_friendsList = treatIncompleteDictionary(friendsListAsString)
        root_df.loc[user_id, 'friendsList'] = modified_friendsList

    # If an ownedGamesList dictionary is incomplete, remove the incomplete bits.
    ownedGamesListAsString = root_df.loc[user_id, 'ownedGamesList']

    try:
        if(not ownedGamesListAsString.endswith(']')):
            modified_ownedGamesList = treatIncompleteDictionary(ownedGamesListAsString)
            root_df.loc[user_id, 'ownedGamesList'] = modified_ownedGamesList
    except:
        continue

# Save results
saveData(root_df, 'prepared_root_df.csv', privateIdsList)
