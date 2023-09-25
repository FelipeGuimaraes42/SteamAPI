from steam import Steam
from decouple import config

import pandas as pd
import numpy as np
import warnings

# No warnings please.
warnings.filterwarnings("ignore")

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

# Study the Web API documentation. Create a function for each case. Use them, test results on different occasions. See what comes of it.
# https://developer.valvesoftware.com/wiki/Steam_Web_API

def getUserDataAndId(steamid):
  user = steam.users.get_user_details(steamid)
  steam_id = user['player']['steamid']
  return user, steam_id

def createDataframeFromRoot(steamid):
  root_user, root_user_id = getUserDataAndId(steamid)
  df = pd.DataFrame(data=root_user).T
  df.set_index('steamid', inplace=True)
  new_columns = ['friendsList', 'ownedGamesCount', 'ownedGamesList', 'recentlyPlayedGamesCount', 'recentlyPlayedGamesList']
  for col_name in new_columns:
    df[col_name] = np.nan

  return df, root_user, root_user_id

# Get one of the users in the top of the steam friends ladder in https://steamladder.com/ladder/friends/
root_df, root_user, root_user_id = createDataframeFromRoot('76561198070799736')

"""## Get data from API:"""

# The api does not return all friends for a given user. It only returns a sample of up to 100 friends.

# Take user: https://steamcommunity.com/id/sazakikun/ for instance. They have over 100 friends (121 currently) but the returned object only has 100 entries.
sasakikunSteamId = '76561198119777155'
friendsListSample = steam.users.get_user_friends_list(sasakikunSteamId)
print(len(friendsListSample['friends']))

def getFriendsList(df, user_id):
  row = df.shape[0] - 1
  try:
    friendsListSample = steam.users.get_user_friends_list(user_id)
    df['friendsList'][row] = friendsListSample['friends']
    return df
  except:
    print('Could not get friends list for user with steamid =', df.index[row], 'due to privacy restriction.')
    df['friendsList'][row] = np.nan
    return df

root_df = getFriendsList(root_df, root_user_id)

def getRecentlyPlayedGamesData(df, user_id):
  row = df.shape[0] - 1
  recentlyPlayedGames = steam.users.get_user_recently_played_games(user_id)
  if recentlyPlayedGames['total_count'] == 0:
    df['recentlyPlayedGamesCount'][row] = 0
    df['recentlyPlayedGamesList'][row] = np.nan
    return df

  df['recentlyPlayedGamesCount'][row] = recentlyPlayedGames['total_count']
  df['recentlyPlayedGamesList'][row] = recentlyPlayedGames['games']
  return df

def getGamesData(df, user_id):
  try:
    row = df.shape[0] - 1
    owned_games = steam.users.get_owned_games(user_id)
    if len(owned_games) == 0:
      df['ownedGamesCount'][row] = 0
      df['ownedGamesList'][row] = np.nan
      return df

    df['ownedGamesCount'][row] = len(owned_games['games'])
    df['ownedGamesList'][row] = owned_games['games']
    df = getRecentlyPlayedGamesData(df)
    return df

  except:
    return df

root_df = getGamesData(root_df, root_user_id)

# Adding Friends of root
root_friends_list = root_df.friendsList[0]
df = root_df

for i in range(len(root_friends_list)):
  user, user_id = getUserDataAndId(root_friends_list[i]['steamid'])
  if user_id not in df.index.values:
    new_row = pd.DataFrame(data=user).T
    new_row.set_index('steamid', inplace=True)
    df = pd.concat([df, new_row])

    getFriendsList(df, user_id)
    getGamesData(df, user_id)

print(df.head())
df.to_csv('data.csv')