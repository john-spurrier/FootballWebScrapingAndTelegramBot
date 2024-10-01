import requests
from bs4 import BeautifulSoup

# URL of the website you want to scrape (update this with the real URL)
url = 'https://www.ncaa.com/scoreboard/football/fbs'  # Replace with the actual URL

# Send a GET request to fetch the webpage content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all game elements (using 'gamePod gamePod-type-game' class)
    games = soup.find_all('div', class_='gamePod gamePod-type-game status-pre')
    print(f'Found {len(games)} games')
    # Loop through each game and extract team names
    for game in games:
        # Find all span elements containing team names
        teams = game.find_all('span', class_='gamePod-game-team-name')

        # Ensure exactly 2 teams are found
        if len(teams) == 2:
            team_1 = teams[0].text.strip()
            team_2 = teams[1].text.strip()
            print(f'Match: {team_1} vs {team_2}')
        else:
            print("Unexpected structure: could not find two teams")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
