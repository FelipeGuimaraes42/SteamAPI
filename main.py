from steam import Steam
from decouple import config
import time
import pandas as pd
import numpy as np
import warnings

# No warnings please.
warnings.filterwarnings("ignore")

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)


def getUserDataAndId(steamid):
    while True:
        try:
            user = steam.users.get_user_details(steamid)
            steam_id = user['player']['steamid']
            return user, steam_id
        except Exception as e:
            print(f"Error fetching user data for {steamid}: {str(e)}")
            time.sleep(0.5)
            continue


def createDataframeFromRoot(steamid):
    root_user, root_user_id = getUserDataAndId(steamid)
    df = pd.DataFrame(data=root_user).T
    df.set_index('steamid', inplace=True)
    new_columns = ['friendsList', 'ownedGamesCount', 'ownedGamesList', 'recentlyPlayedGamesCount', 'recentlyPlayedGamesList']
    for col_name in new_columns:
        df[col_name] = np.nan
    return df, root_user, root_user_id

def getFriendsList(df, user_id):
    while True:
        try:
            friendsListSample = steam.users.get_user_friends_list(user_id)
            df['friendsList'][0] = friendsListSample['friends']
            return df
        except Exception as e:
            print(f"Error fetching friends list for {user_id}: {str(e)}")
            time.sleep(0.5)
            continue


def getRecentlyPlayedGamesData(df, user_id):
    while True:
        try:
            recentlyPlayedGames = steam.users.get_user_recently_played_games(user_id)
            if recentlyPlayedGames['total_count'] == 0:
                df['recentlyPlayedGamesCount'][0] = 0
                df['recentlyPlayedGamesList'][0] = np.nan
            else:
                df['recentlyPlayedGamesCount'][0] = recentlyPlayedGames['total_count']
                df['recentlyPlayedGamesList'][0] = recentlyPlayedGames['games']
            return df
        except Exception as e:
            print(f"Error fetching recently played games data for {user_id}: {str(e)}")
            time.sleep(0.5)
            continue


def getGamesData(df, user_id):
    while True:
        try:
            owned_games = steam.users.get_owned_games(user_id)
            if len(owned_games) == 0:
                df['ownedGamesCount'][0] = 0
                df['ownedGamesList'][0] = np.nan
            else:
                df['ownedGamesCount'][0] = len(owned_games['games'])
                df['ownedGamesList'][0] = owned_games['games']
                getRecentlyPlayedGamesData(df, user_id)
            return df
        except Exception as e:
            print(f"Error fetching games data for {user_id}: {str(e)}")
            time.sleep(0.5)
            continue


def getFriendsDataRecursive(df, user_id, level, max_level):
    if level > max_level:
        return df

    while True:
        try:
            friendsListSample = steam.users.get_user_friends_list(user_id)
            friends = friendsListSample['friends']

            for friend in friends:
                friend_user_id = friend['steamid']
                if friend_user_id not in df.index.values:
                    user, _ = getUserDataAndId(friend_user_id)
                    new_row = pd.DataFrame(data=user).T
                    new_row.set_index('steamid', inplace=True)
                    df = pd.concat([df, new_row])

                    getFriendsList(df, friend_user_id)
                    getGamesData(df, friend_user_id)

                    df = getFriendsDataRecursive(df, friend_user_id, level + 1, max_level)

            return df
        except Exception as e:
            print(f"Error fetching friends data for {user_id}: {str(e)}")
            time.sleep(0.5)
            continue


root_df, root_user, root_user_id = createDataframeFromRoot('76561198070799736')
root_df = getFriendsDataRecursive(root_df, root_user_id, 1, 3)

print(root_df.head())
root_df.to_csv('data.csv')
