from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from decouple import config

import time
import csv
import os
import ast


import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_options)

STEAM_USERNAME = config('STEAM_USERNAME')
STEAM_PASSWORD = config('STEAM_PASSWORD')


def login_to_steam():
    # Abra a página de login do Steam
    driver.get('https://store.steampowered.com/login/')
    time.sleep(10)

    try:
        # Encontre os campos de entrada de nome de usuário e senha
        username_field = driver.find_element(By.XPATH, '//input[@type="text"]')
        password_field = driver.find_element(By.XPATH, '//input[@type="password"]')

        # Preencha os campos de entrada
        username_field.send_keys(STEAM_USERNAME)
        password_field.send_keys(STEAM_PASSWORD)

        # Envie o formulário (clique no botão Iniciar Sessão)
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        login_button.click()

        # Espere alguns segundos (você pode ajustar isso conforme necessário)
        time.sleep(10)

    except Exception as exc:
        print(f"Ocorreu um erro ao efetuar o login: {str(exc)}")


def create_csv_file():
    if not os.path.exists('friends_first_level.csv'):
        with open('friends_first_level.csv', 'w', newline='') as csv_file:
            fieldnames = ['Friend Id', 'Id', 'Number of Friends', 'Friends', 'Number of Games', 'Games']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()


def extract_csv_info():
    # Initialize an empty list to store data as tuples
    id_and_friends = []

    # Open and read the CSV file
    with open("steam_members.csv", mode='r', newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Extract data based on headers and append as a tuple
            id_and_friends.append((row['Id'], row['Friends']))

    return id_and_friends


def verify_user(url):
    driver.get(url)
    try:
        div_element = driver.find_element(By.XPATH, "//div[@id='mainContents']//h2")

        if div_element:
            return False
        else:
            return True
    except Exception as e:
        return True


def scrap_friends_data(profile_link):
    friend_data = []
    num_friends = 0
    try:
        user_friends_url = profile_link + '/friends'

        driver.get(user_friends_url)
        time.sleep(2)  # Esperar a página do perfil carregar

        friend_list_div = driver.find_element(By.ID, "friends_list")

        # Find all the friend elements within the friend list
        friend_elements = friend_list_div.find_elements(By.CLASS_NAME, "friend_block_v2")

        # Get the count of friends
        num_friends = len(friend_elements)

        # Iterate through the friend elements to extract names and profile URLs
        for friend_element in friend_elements:
            friend_url = friend_element.find_element(By.CLASS_NAME, "selectable_overlay").get_attribute("href")
            friend_data.append(friend_url.split('/')[-1])
    except Exception as exc:
        print('An exception occurred when retrieving friend data.', exc)
    return friend_data, num_friends


def scrap_games_data(profile_link):
    game_data = []
    num_games = 0
    try:
        user_games_url = profile_link + '/games/?tab=all'

        driver.get(user_games_url)
        time.sleep(20)  # Esperar a página dos jogos carregar

        games_list_div = driver.find_element(By.CLASS_NAME, "gameslistitems_List_3tY9v")

        # Find all the friend elements within the friend list
        game_elements = games_list_div.find_elements(By.CLASS_NAME, "gameslistitems_GamesListItemContainer_29H3o")

        # Get the count of friends
        num_games = len(game_elements)

        # Iterate through the friend elements to extract names and profile URLs
        for game_element in game_elements:
            game_url = game_element.find_element(By.CLASS_NAME, "gameslistitems_GameItemPortrait_1bAC6").get_attribute(
                "href")
            game_id = game_url.split('/')[-1]
            hours_played_element = game_element.find_element(By.CLASS_NAME, "gameslistitems_Hours_26nl3").text
            playtime = hours_played_element.split('\n')[-1].split(' ')[0]
            game_data.append((game_id, playtime))
    except Exception as exc:
        print('An exception occurred when retrieving friend data.', exc)
    return game_data, num_games


# Função para raspar e coletar informações do membro
def scrape_user_info(user_id):
    scraped_user_info = {}
    profile_link = "https://steamcommunity.com/id/" + user_id

    user_exists = verify_user(profile_link)

    if user_exists:
        friend_data, num_friends = scrap_friends_data(profile_link)
        games_data, num_games = scrap_games_data(profile_link)

        # Armazenar informações do membro em um dicionário
        scraped_user_info['id'] = user_id
        scraped_user_info['num_friends'] = num_friends
        scraped_user_info['friends'] = friend_data
        scraped_user_info['num_games'] = num_games
        scraped_user_info['games'] = games_data

    return scraped_user_info


def save_user_info_csv(friend_id, user_info_parameter):
    if len(user_info_parameter) != 0:
        with open('friends_first_level.csv', 'a', newline='') as csv_file:
            fieldnames = ['Friend Id', 'Id', 'Number of Friends', 'Friends', 'Number of Games', 'Games']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writerow({'Friend Id': friend_id,
                                 'Id': user_info_parameter['id'],
                                 'Number of Friends': user_info_parameter['num_friends'],
                                 'Friends': user_info_parameter['friends'],
                                 'Number of Games': user_info_parameter['num_games'],
                                 'Games': user_info_parameter['games']})


login_to_steam()
create_csv_file()
data = extract_csv_info()

for user in data:
    id_value, friends_value = user  # Unpack the tuple
    friends_value = ast.literal_eval(friends_value)
    for friend in friends_value:
        user_info = scrape_user_info(friend)
        save_user_info_csv(id_value, user_info)

# Fechar o navegador
driver.quit()
