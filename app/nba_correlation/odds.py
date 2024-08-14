import requests
import os
from dotenv import load_dotenv

prop_identifier = {
    1: "Points",
    2: "Rebounds",
    3: "Assists",
    4: "Steals",
    5: "Blocks",
    6: "Turnovers",
    7: "Field Goals Made",
    8: "Field Goals Attempted",
    9: "Three-Point Field Goals Made",
    10: "Three-Point Field Goals Attempted",
    11: "Free Throws Made",
    12: "Free Throws Attempted",
    13: "Personal Fouls",
    14: "Minutes Played",
    16: "Points + Rebounds + Assists",
    17: "Points + Rebounds",
    18: "Points + Assists",
    19: "Rebounds + Assists",
    20: "Double-Double",
    21: "Triple-Double",
}


# Load environment variables from the .env.local file
load_dotenv(dotenv_path='.env.local')

def init_data():
    API_KEY = os.environ['API_KEY']
    SPORT = '' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports
    REGIONS = 'us' # uk | us | eu | au. Multiple can be specified if comma delimited
    MARKETS = '' # h2h | spreads | totals. Multiple can be specified if comma delimited
    ODDS_FORMAT = 'decimal' # decimal | american
    DATE_FORMAT = 'iso' # iso | unix

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    #
    # First get a list of in-season sports
    #   The sport 'key' from the response can be used to get odds in the next request
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    odds_response = requests.get(
        f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
        params={
            'api_key': API_KEY,
            'regions': REGIONS,
            'markets': MARKETS,
            'oddsFormat': ODDS_FORMAT,
            'dateFormat': DATE_FORMAT,
        }
    )

    if odds_response.status_code != 200:
        print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

    else:
        odds_json = odds_response.json()
        print('Number of events:', len(odds_json))
        print(odds_json)

        # Check the usage quota
        print('Remaining requests', odds_response.headers['x-requests-remaining'])
        print('Used requests', odds_response.headers['x-requests-used'])
