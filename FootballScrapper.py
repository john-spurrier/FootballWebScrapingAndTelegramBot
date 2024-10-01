import requests
from bs4 import BeautifulSoup
import time

def scrape_matches():
    # URL of the website you want to scrape (update this with the real URL)
    url = 'https://www.ncaa.com/scoreboard/football/fbs'  # Replace with the actual URL

    # urlForFinal = 'https://www.ncaa.com/scoreboard/football/fbs/2024/05/all-conf'

    # Send a GET request to fetch the webpage content
    response = requests.get(url)

    # code for live scoring of games
    # if responseForCurrent.status_code == 200:
    #     soup = BeautifulSoup(responseForCurrent.text, 'html.parser')
    #     games = soup.find_all('div', class_='gamePod gamePod-type-game status-?')
    #     for game in games:
    #         teams = game.find_all('span', class_='gamePod-game-team-name')
    #         scores = game.find_all('span', class_='gamePod-game-team-score')
    #         if len(teams) == 2:
    #             team_1 = teams[0].text.strip()
    #             score_1 = scores[0].text.strip()
    #             team_2 = teams[1].text.strip()
    #             score_2 = scores[1].text.strip()
    #             print(f'{team_1}: {score_1} \n{team_2}: {score_2}\n')
    #         else:


    print("\n")

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup

        match_list = []
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all game elements (using 'gamePod gamePod-type-game' class)
        games = soup.find_all('div', class_='gamePod gamePod-type-game status-pre')
        # Loop through each game and extract team names
        for game in games:
            # Find all span elements containing team names
            teams = game.find_all('span', class_='gamePod-game-team-name')

            # Ensure exactly 2 teams are found
            if len(teams) == 2:
                team_1 = teams[0].text.strip()
                team_2 = teams[1].text.strip()
                match = f'Match: {team_1} vs {team_2}'
                match_list.append(match)
            else:
                print("Unexpected structure: could not find two teams")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return match_list

# Function to display and select games to track
def select_games_to_track(match_list):
    print("\nAvailable games:")
    for idx, match in enumerate(match_list):
        print(f"{idx + 1}: {match}")

    selected_indices = input("\nEnter the numbers of the games you want to track, separated by commas: ")

    # Convert the input into a list of indices (validate user input)
    try:
        selected_indices = [int(i.strip()) - 1 for i in selected_indices.split(",")]
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return []

    # Filter the matches to only the ones the user selected
    selected_matches = [match_list[i] for i in selected_indices if 0 <= i < len(match_list)]

    return selected_matches


def track_selected_games(selected_matches):
    while True:
        print("\nUpdating selected games...")

        # For demonstration purposes, we'll re-use the scrape_all_matches function
        # and only print the selected matches
        current_matches = scrape_matches()

        if not current_matches:
            print("No matches available or unable to retrieve data.")
        else:
            for match in selected_matches:
                if match in current_matches:
                    print(f"Match: {match}")
                else:
                    print(f"Match: {match} - Update not available")

        # Wait for 60 seconds before the next update
        time.sleep(60)

# Main program logic
if __name__ == "__main__":
    # Step 1: Get all matches
    all_matches = scrape_matches()

    if not all_matches:
        print("No matches found or unable to retrieve data.")
    else:
        # Step 2: Allow the user to select which games to track
        selected_games = select_games_to_track(all_matches)

        if selected_games:
            # Step 3: Track the selected games and get updates
            track_selected_games(selected_games)
        else:
            print("No games selected for tracking.")

