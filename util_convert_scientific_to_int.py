import warnings
from decouple import config

from utils.private_ids import *
from utils.api import *
from utils.dataframe_manipulation import *

warnings.filterwarnings("ignore")

df = pd.read_csv("databases/temp_api_level_1_ate_285.csv")
columns_to_keep = [
    "steamid",
    "communityvisibilitystate",
    "loccityid",
    "loccountrycode",
    "locstatecode",
    "personastate",
    "profileurl",
    "timecreated",
    "friendsCount",
    "friendsList",
    "ownedGamesCount",
    "ownedGamesList",
    "commentpermission",
]
df = df[columns_to_keep]

def convert_sci_notation_to_int(value):
    try:
        return int(float(value))
    except ValueError:
        return value


# Convert from scientific notation to integer.
df["steamid"] = df["steamid"].apply(convert_sci_notation_to_int)
df_no_duplicates = prepareRootDataframe(df)

print("df len =", len(df))
print("df_no_duplicates len =", len(df_no_duplicates))

df_no_duplicates.to_csv("tempo.csv", index=True)
