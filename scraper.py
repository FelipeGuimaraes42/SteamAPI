from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the Selenium WebDriver (you may need to specify the path to your webdriver)
driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

# Open the Steam group members' page
url = "https://steamcommunity.com/groups/jogosbra/members/?p=1"
driver.get(url)


# Function to scrape and collect member information
def scrape_member_info(member_block):
    member_info = {}

    # Extract member's profile link and username
    profile_link = member_block.find_element(By.CSS_SELECTOR, 'a.linkFriend').get_attribute('href')
    username = member_block.find_element(By.CSS_SELECTOR, 'a.linkFriend').text

    # Click on the member's profile to get additional information
    member_block.find_element(By.CSS_SELECTOR, 'a.linkFriend').click()
    time.sleep(2)  # Wait for the profile page to load

    # Get the number of friends
    friends_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Amigos")
    num_friends = int(friends_link.find_element(By.CLASS_NAME, 'profile_count_link_total').text.replace(',', ''))

    # Get the number of games and link to games
    games_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Jogos")
    num_games = int(games_link.find_element(By.CLASS_NAME, 'profile_count_link_total').text.replace(',', ''))
    games_url = games_link.get_attribute('href')

    # Store member information in a dictionary
    member_info['username'] = username
    member_info['profile_link'] = profile_link
    member_info['num_friends'] = num_friends
    member_info['num_games'] = num_games
    member_info['games_link'] = games_url

    return member_info


# Loop through the member pages
all_member_info = []
page_number = 1
while True:
    member_blocks = driver.find_elements(By.CSS_SELECTOR, 'div#memberList div.member_block')

    # Scraping information for each member on the page
    for member_block in member_blocks:
        member_info = scrape_member_info(member_block)
        all_member_info.append(member_info)

    # Navigate to the next page
    page_number += 1
    next_page_url = f"https://steamcommunity.com/groups/jogosbra/members/?p={page_number}"
    driver.get(next_page_url)

    # Check if we have reached the last page
    if 'No more members to load' in driver.page_source:
        break

# Close the browser
driver.quit()

# Print or save the collected information
for member_info in all_member_info:
    print(f"Username: {member_info['username']}")
    print(f"Profile Link: {member_info['profile_link']}")
    print(f"Number of Friends: {member_info['num_friends']}")
    print(f"Number of Games: {member_info['num_games']}")
    print(f"Games Link: {member_info['games_link']}")
    print("\n")
