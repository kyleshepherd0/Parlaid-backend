import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from config import Config

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

def scrape_teams():
    url = 'https://www.pro-football-reference.com/teams/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    teams_table = soup.find('table', {'id': 'teams'})
    teams_data = pd.read_html(str(teams_table))[0]

    teams = teams_data[['Team', 'First Season']].dropna()
    teams.columns = ['name', 'first_season']
    teams['abbreviation'] = teams['name'].apply(lambda x: x.split()[-1])
    teams.to_sql('team', engine, if_exists='replace', index=False)
    print("Teams data scraped and stored in the database.")
