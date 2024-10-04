import requests
import keys
import apiResponse
from telegram import Bot
import time
import asyncio

# Set up the Telegram bot
bot = Bot(token=keys.TELEGRAM_BOT_TOKEN)

# Function to call the API and get match details
def get_matches():
    response = apiResponse.response

    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        events = data.get('data', {}).get('events', {}).get('events', [])
        match_list = []

        for event in events:
            teams = event.get('teams', [])
            event_status = event.get('eventStatus', {}).get('name', 'Unknown')
            event_time = event.get('canonicalStartDate', {}).get('full', 'Unknown Time')

            if len(teams) == 2:
                team_1 = teams[0].get('location', 'Unknown') + " " + teams[0].get('nickname', 'Unknown')
                team_1_score = teams[0].get('score', 0)
                team_2 = teams[1].get('location', 'Unknown') + " " + teams[1].get('nickname', 'Unknown')
                team_2_score = teams[1].get('score', 0)

                match = {
                    "matchup": f"{team_1} vs {team_2}",
                    "score": f"{team_1_score} - {team_2_score}",
                    "status": event_status,
                    "time": event_time,
                    "team_1_score": team_1_score,
                    "team_2_score": team_2_score
                }
                match_list.append(match)        
        return match_list
    else:
        print(f"Failed to retrieve data from API. Status code: {response.status_code}")
        return []

# Function to display and select games to track
def select_games_to_track(match_list):
    print("\nAvailable games:")
    for idx, match in enumerate(match_list):
        print(f"{idx + 1}: {match['matchup']} | Status: {match['status']}")

    selected_indices = input("\nEnter the numbers of the games you want to track, separated by commas: ")

    try:
        selected_indices = [int(i.strip()) - 1 for i in selected_indices.split(",")]
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return []

    selected_matches = [match_list[i] for i in selected_indices if 0 <= i < len(match_list)]

    return selected_matches

# Async function to track selected games
async def track_selected_games(selected_matches):
    previous_scores = {match['matchup']: {"team_1_score": match["team_1_score"], "team_2_score": match["team_2_score"]} for match in selected_matches}

    # Send an initial message to Telegram with the list of games being tracked
    tracking_message = "Tracking the following games:\n"
    for match in selected_matches:
        tracking_message += f"{match['matchup']}\n"
    
    await bot.send_message(chat_id=keys.TELEGRAM_CHAT_ID, text=tracking_message)

    while True:
        print("\nUpdating selected games...")

        current_matches = get_matches()

        if not current_matches:
            print("No matches available or unable to retrieve data.")
        else:
            for selected_match in selected_matches:
                # Find the corresponding current match
                for current_match in current_matches:
                    if selected_match['matchup'] == current_match['matchup']:
                        prev_score = previous_scores[selected_match['matchup']]
                        current_score = {
                            "team_1_score": current_match["team_1_score"],
                            "team_2_score": current_match["team_2_score"]
                        }

                        # Check if the score has changed
                        if prev_score != current_score:
                            # Update the previous score
                            previous_scores[selected_match['matchup']] = current_score

                            # Print and send update
                            print(f"Score Update: {current_match['matchup']} | New Score: {current_match['score']} | Status: {current_match['status']} | Time: {current_match['time']}")
                            await bot.send_message(chat_id=keys.TELEGRAM_CHAT_ID, text=f"Update: {current_match['matchup']} | Score: {current_match['score']} | Status: {current_match['status']}")

        # Wait for 60 seconds before the next update
        await asyncio.sleep(60)

# Main async function
async def main():
    all_matches = get_matches()

    if not all_matches:
        print("No matches found or unable to retrieve data.")
    else:
        selected_games = select_games_to_track(all_matches)

        if selected_games:
            # Track the selected games
            await track_selected_games(selected_games)
        else:
            print("No games selected for tracking.")

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
