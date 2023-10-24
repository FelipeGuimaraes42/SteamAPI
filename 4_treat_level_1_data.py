import warnings
from utils.private_ids import *
from utils.api import *
from utils.dataframe_manipulation import *
from utils.treat_data import *

warnings.filterwarnings("ignore")

df = pd.read_parquet("temp_api_level_1_ate_500.parquet")

df.reset_index(inplace=True)
df.drop_duplicates(subset=['steamid'], inplace=True)
df.dropna(subset=['friendsList'], inplace=True)
df.set_index('steamid', inplace=True)

for i in range(len(df)):
    user_id = df.index[i]
    # If a friendsList dictionary is incomplete, remove the incomplete bits.
    friendsListAsString = df.loc[user_id, 'friendsList']
    if(not friendsListAsString.endswith(']')):
        modified_friendsList = treatIncompleteDictionary(friendsListAsString)
        df.loc[user_id, 'friendsList'] = modified_friendsList

    # If an ownedGamesList dictionary is incomplete, remove the incomplete bits.
    ownedGamesListAsString = df.loc[user_id, 'ownedGamesList']

    try:
        if(not ownedGamesListAsString.endswith(']')):
            modified_ownedGamesList = treatIncompleteDictionary(ownedGamesListAsString)
            df.loc[user_id, 'ownedGamesList'] = modified_ownedGamesList
    except:
        continue

treatAndSaveData(df, 'temp_api_level_1_ate_500_treated')