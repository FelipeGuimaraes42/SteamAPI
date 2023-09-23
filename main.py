import pandas as pd
from steam import Steam
from decouple import config

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

import warnings
warnings.filterwarnings("ignore")

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
  df.head()

  return df, root_user, root_user_id

# Get one of the users in the top of the steam friends ladder in https://steamladder.com/ladder/friends/
df, root_user, root_user_id = createDataframeFromRoot('76561198070799736')

"""## Get data from API:"""

def getFriendsList(df, user_id):
  try:
    friendsList = steam.users.get_user_friends_list(user_id)
    df['friendsList'] = [friendsList['friends']]
  except:
    print('Except in Friends List')
    df['friendsList'] = {}

getFriendsList(df, root_user_id)

def getRecentlyPlayedGamesData(df, user_id):
  recentlyPlayedGames = steam.users.get_user_recently_played_games(user_id)
  if recentlyPlayedGames['total_count'] == 0:
    df['recentlyPlayedGamesCount'] = 0
    df['recentlyPlayedGamesList'] = {}
    return

  df['recentlyPlayedGamesCount'] = recentlyPlayedGames['total_count']
  df['recentlyPlayedGamesList'] = [recentlyPlayedGames['games']]

def getGamesData(df, user_id):
  try:
    owned_games = steam.users.get_owned_games(user_id)
    if len(owned_games) == 0:
      df['ownedGamesCount'] = 0
      df['ownedGamesList'] = {}
      return

    df['ownedGamesCount'] = len(owned_games)
    df['ownedGamesList'] = [owned_games['games']]
    getRecentlyPlayedGamesData(df)

  except:
    return

getGamesData(df, root_user_id)

root_friends_list = df.friendsList[0]

for i in range(len(root_friends_list)):
  user, user_id = getUserDataAndId(root_friends_list[i]['steamid'])
  if user_id not in df.index.values:
    new_row = pd.DataFrame(data=user).T
    new_row.set_index('steamid', inplace=True)

    getFriendsList(df, user_id)
    getGamesData(df, user_id)

    df = pd.concat([df, new_row])

df.friendsList[0] = root_friends_list

print(df.head())
df.to_csv('data.csv')