import pandas as pd
from steam import Steam
from decouple import config

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

# Study the Web API documentation. Create a function for each case. Use them, test results on different occasions. See what comes of it.
# https://developer.valvesoftware.com/wiki/Steam_Web_API

def getUserAndId(nickname):
  user = steam.users.search_user(nickname)
  steam_id = user['player']['steamid']
  return user, steam_id

def createDataframeFromRoot(nickname):
  root_user, root_user_id = getUserAndId(nickname)
  df = pd.DataFrame(data=root_user).T
  df.set_index('steamid', inplace=True)
  df.head()

  return df, root_user, root_user_id

# Get one of the users in the top of the steam friends ladder in https://steamladder.com/ladder/friends/
df, root_user, root_user_id = createDataframeFromRoot('zelourin')

"""## Get data from API:"""

def getFriendsList(df):
  try:
    friendsList = steam.users.get_user_friends_list(root_user_id)
    df['friendsList'] = [friendsList['friends']]
  except:
    df['friendsList'] = {}

def getRecentlyPlayedGamesData(df):
  recentlyPlayedGames = steam.users.get_user_recently_played_games(root_user_id)
  if recentlyPlayedGames['total_count'] == 0:
    df['recentlyPlayedGamesCount'] = 0
    df['recentlyPlayedGamesList'] = {}
    return

  df['recentlyPlayedGamesCount'] = recentlyPlayedGames['total_count']
  df['recentlyPlayedGamesList'] = [recentlyPlayedGames['games']]

def getGamesData(df):
  try:
    owned_games = steam.users.get_owned_games(root_user_id)
    if len(owned_games) == 0:
      return

    df['ownedGamesCount'] = len(owned_games)
    df['ownedGamesList'] = [owned_games['games']]
    getRecentlyPlayedGamesData(df)

  except:
    return

getFriendsList(df)
getGamesData(df)

print(df.head())
df.to_csv('data.csv')