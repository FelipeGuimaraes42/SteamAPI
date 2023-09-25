from steam import Steam
from decouple import config

import pandas as pd
import numpy as np
import warnings

# No warnings please.
warnings.filterwarnings("ignore")

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)


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


def getFriendsDataRecursive(df, user_id, level, max_level):
    if level > max_level:
        return df

    row = df.shape[0] - 1
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

            # Recursively fetch friends data for the next level
            df = getFriendsDataRecursive(df, friend_user_id, level + 1, max_level)

    return df


root_df, root_user, root_user_id = createDataframeFromRoot('76561198070799736')
root_df = getFriendsDataRecursive(root_df, root_user_id, 1, 3)

print(root_df.head())
root_df.to_csv('data.csv')
