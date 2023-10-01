from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
import os

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_options)


def create_csv_file():
    if not os.path.exists('steam_members.csv'):
        with open('steam_members.csv', 'w', newline='') as csv_file:
            fieldnames = ['Page', 'Username', 'Profile Link', 'Number of Friends', 'Friends']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()


def create_csv_file_without_usernames():
    if not os.path.exists('steam_members.csv'):
        with open('steam_members.csv', 'w', newline='') as csv_file:
            fieldnames = ['Page', 'Id', 'Number of Friends', 'Friends']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()


# Função para raspar e coletar informações do membro
def scrape_member_info(member_parameter):
    scraped_member_info = {}

    username = member_parameter[0]
    profile_link = member_parameter[1]
    user_id = profile_link.split('/')[-1]

    # friend_data = {}
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
            # friend_name = friend_element.find_element(By.CLASS_NAME, "friend_block_content").text.split('\n')[0]
            # friend_data[friend_name] = friend_url
            # friend_data.append(friend_url)
    except Exception as exc:
        print('An exception occurred when retrieving friend data.', exc)

    # Armazenar informações do membro em um dicionário
    scraped_member_info['id'] = user_id
    scraped_member_info['username'] = username
    scraped_member_info['profile_link'] = profile_link
    scraped_member_info['num_friends'] = num_friends
    scraped_member_info['friends'] = friend_data

    # print(scraped_member_info)
    return scraped_member_info


# Tentar continuar de onde parou
# try:
#     with open('steam_members.csv', 'r') as csv_file:
#         csv_reader = csv.DictReader(csv_file)
#         for row in csv_reader:
#             page_number = int(row['Page']) + 1
# except FileNotFoundError:
#     page_number = 1


def save_member_info_csv(member_info_parameter):
    with open('steam_members.csv', 'a', newline='') as csv_file:
        fieldnames = ['Page', 'Username', 'Profile Link', 'Number of Friends', 'Friends']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writerow({'Page': page_number, 'Username': member_info_parameter['username'],
                             'Profile Link': member_info_parameter['profile_link'],
                             'Number of Friends': member_info_parameter['num_friends'],
                             'Friends': member_info_parameter['friends']})


def save_member_info_csv_without_usernames(member_info_parameter):
    with open('steam_members.csv', 'a', newline='') as csv_file:
        fieldnames = ['Page', 'Id', 'Number of Friends', 'Friends']
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writerow({'Page': page_number,
                             'Id': member_info_parameter['id'],
                             'Number of Friends': member_info_parameter['num_friends'],
                             # 'Friends': str(member_info_parameter['friends']).replace("[", "").replace("]", "").replace(
                             #     "'", "")})
                             'Friends': member_info_parameter['friends']})


# Número da página atual
page_number = 1

# Abrir a página de membros do grupo Steam
url = "https://steamcommunity.com/groups/jogosbra/members/?p=" + str(page_number)
driver.get(url)

# Inicializar lista para armazenar informações de todos os membros
all_member_info = []

create_csv_file_without_usernames()

# Loop através das páginas de membros
while True:
    try:
        # Find the memberList div
        member_list_div = driver.find_elements(By.CSS_SELECTOR, 'div#memberList')

        # Find all the divs with class 'member_block' inside memberList
        member_blocks = driver.find_elements(By.CSS_SELECTOR, 'div.member_block')
        member_block_last = driver.find_elements(By.CSS_SELECTOR, 'div.member_block last')

        members = []
        for member_block in member_blocks:
            member = member_block.find_elements(By.CSS_SELECTOR, 'a.linkFriend')[0]
            members.append((member.text, member.get_attribute('href')))

        for member_block in member_block_last:
            member = member_block.find_elements(By.CSS_SELECTOR, 'a.linkFriend')[0]
            members.append((member.text, member.get_attribute('href')))

        for member in members:
            member_info = scrape_member_info(member)
            # Salvando informações em um arquivo CSV após cada iteração
            save_member_info_csv_without_usernames(member_info)
            all_member_info.append(member_info)

        # Navegar para a próxima página
        page_number += 1
        next_page_url = f"https://steamcommunity.com/groups/jogosbra/members/?p={page_number}"
        driver.get(next_page_url)

        # Verificar se chegou à última página
        if 'No more members to load' in driver.page_source:
            break

    except Exception as e:
        print(f"Erro na página {page_number}: {str(e)}")
        # Se ocorrer um erro, registre o número da página e faça o download do CSV gerado
        # with open('last_page_error.txt', 'w') as error_file:
        #     error_file.write(str(page_number))
        break

# Fechar o navegador
driver.quit()

# Imprimir ou salvar as informações coletadas
# for member_info in all_member_info:
#     print(f"Username: {member_info['username']}")
#     print(f"Profile Link: {member_info['profile_link']}")
#     print(f"Number of Friends: {member_info['num_friends']}")
#     print(f"Number of Games: {member_info['num_games']}")
#     print(f"Games Link: {member_info['games_link']}")
#     print("\n")
