from steam import Steam
from decouple import config

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)


def foo():
    print(steam.users.search_user("zelourin"))
    print(steam.users.get_owned_games("76561198070799736"))
    print(steam.users.get_user_recently_played_games("76561198070799736"))


if __name__ == '__main__':
    foo()
