from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# import time
import csv

import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=chrome_options)

# Número da página atual
page_number = 2

# Abrir a página de membros do grupo Steam
url = "https://steamcommunity.com/groups/jogosbra/members/?p=" + str(page_number)
driver.get(url)


# Função para raspar e coletar informações do membro
def scrape_member_info(scraped_member_block):
    scraped_member_info = {}

    # Extrair link do perfil e nome de usuário
    profile_link = scraped_member_block.find_element(By.CSS_SELECTOR, 'a.linkFriend').get_attribute('href')
    user_id = profile_link.split('/')[-1]
    username = scraped_member_block.find_element(By.CSS_SELECTOR, 'a.linkFriend').text

    # Clicar no perfil do membro para obter informações adicionais
    scraped_member_block.find_element(By.CSS_SELECTOR, 'a.linkFriend').click()
    # time.sleep(2)  # Esperar a página do perfil carregar

    # Create a dictionary to store friend names and their profile URLs
    friend_data = {}
    num_friends = 0
    try:
        user_friends_url = profile_link + '/friends'
        driver.get(user_friends_url)
        friend_list_div = driver.find_element(By.ID, "friends_list")

        # Find all the friend elements within the friend list
        friend_elements = friend_list_div.find_elements(By.CLASS_NAME, "friend_block_v2")

        # Get the count of friends
        num_friends = len(friend_elements)
        print(num_friends)

        # Iterate through the friend elements to extract names and profile URLs
        for friend_element in friend_elements:
            friend_name = friend_element.find_element(By.CLASS_NAME, "friend_block_content").text.split('\n')[0]
            friend_url = friend_element.find_element(By.CLASS_NAME, "selectable_overlay").get_attribute("href")
            friend_data[friend_name] = friend_url
    except Exception as exc:
        print('An exception occurred when retrieving friend data.', exc)

    # try:
    #     # Obter o número de amigos
    #     friends_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Amigos")
    #     num_friends = int(friends_link.find_element(By.CLASS_NAME, 'profile_count_link_total').text.replace(',', ''))
    # except Exception as e:
    #     num_friends = 0
    #
    # try:
    #     # Obter o número de jogos e o link para os jogos
    #     games_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Jogos")
    #     num_games = int(games_link.find_element(By.CLASS_NAME, 'profile_count_link_total').text.replace(',', ''))
    #     games_url = games_link.get_attribute('href')
    # except Exception as e:
    #     num_games = 0
    #     games_url = ""

    # Armazenar informações do membro em um dicionário
    scraped_member_info['id'] = user_id
    scraped_member_info['username'] = username
    scraped_member_info['profile_link'] = profile_link
    scraped_member_info['num_friends'] = num_friends
    scraped_member_info['friends'] = friend_data

    print(scraped_member_info)
    return scraped_member_info


# Inicializar lista para armazenar informações de todos os membros
all_member_info = []

# Tentar continuar de onde parou
try:
    with open('steam_members.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            page_number = int(row['Page']) + 1
except FileNotFoundError:
    page_number = 1

# Loop através das páginas de membros
while True:
    try:
        member_blocks = driver.find_elements(By.CSS_SELECTOR, 'div#memberList div.member_block')

        # Coletando informações para cada membro na página
        for member_block in member_blocks:
            member_info = scrape_member_info(member_block)
            all_member_info.append(member_info)

        # Salvando informações em um arquivo CSV após cada iteração
        with open('steam_members.csv', 'w', newline='') as csv_file:
            fieldnames = ['Page', 'Username', 'Profile Link', 'Number of Friends', 'Number of Games', 'Games Link']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()
            for idx, member_info in enumerate(all_member_info):
                csv_writer.writerow({'Page': page_number, 'Username': member_info['username'],
                                     'Profile Link': member_info['profile_link'],
                                     'Number of Friends': member_info['num_friends'],
                                     'Number of Games': member_info['num_games'],
                                     'Games Link': member_info['games_link']})

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
        with open('last_page_error.txt', 'w') as error_file:
            error_file.write(str(page_number))
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
