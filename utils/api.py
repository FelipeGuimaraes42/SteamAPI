import requests
import pandas as pd
import numpy as np


def makeRequest(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"API request failed with status code: {response.status_code}")


def getUserDataAndId(steam, steamid):
    user = steam.users.get_user_details(steamid)
    steam_id = user["player"]["steamid"]
    return user, steam_id


def createDataframeFromRoot(steam, steamid):
    root_user, root_user_id = getUserDataAndId(steam, steamid)
    df = pd.DataFrame(data=root_user).T
    df.set_index("steamid", inplace=True)
    new_columns = [
        "friendsList",
        "ownedGamesList",
    ]
    for col_name in new_columns:
        df[col_name] = np.nan

    return df, root_user, root_user_id


def getFriendsList(df, user_id, privateIdsList, API_KEY):
    row = df.shape[0] - 1
    try:
        api_url = f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={API_KEY}&steamid={user_id}&relationship=friend&format=json'
        json_data = makeRequest(api_url)
        df['friendsList'][row] = json_data['friendslist']['friends']
        return df
    except Exception as e:
        privateIdsList.append(df.index[row])
        df['friendsList'][row] = np.nan
        return df


def getGamesData(steam, df, user_id):
    try:
        row = df.shape[0] - 1
        owned_games = steam.users.get_owned_games(user_id)
        if len(owned_games["games"]) == 0:
            df["ownedGamesList"][row] = np.nan
            return df

        df["ownedGamesList"][row] = owned_games["games"]
        return df

    except Exception as e:
        return df
