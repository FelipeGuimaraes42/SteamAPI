from steam import Steam
from decouple import config

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)


def foo():
    # user = steam.users.search_user("zelourin")
    user = steam.users.search_user("southrico")
    user_id = user['player']['steamid']
    # print(user_id)
    # print(steam.users.get_owned_games(user_id))
    # print(steam.users.get_user_recently_played_games(user_id))
    # print(steam.users.get_user_friends_list(user_id))
    # print(steam.users.get_owned_games(user_id))
    print(steam.users.get_user_recently_played_games(user_id))


if __name__ == '__main__':
    foo()
