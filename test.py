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
df = pd.read_csv('databases/temp_api_level_1.csv')
df.set_index("steamid", inplace=True)
df_no_duplicates = df[~df.index.duplicated(keep='first')]

print('df len =', len(df))
print('df_no_duplicates len =',len(df_no_duplicates))