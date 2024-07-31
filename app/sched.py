import requests
from bs4 import BeautifulSoup
import psycopg2

games = []

def scrape_pfr():
    year = 2020
    while year < 2024:
        URL = f"https://www.pro-football-reference.com/years/{year}/games.htm"
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        conn = psycopg2.connect(database = "parlay_perfector", 
                        user = "kshepherd", 
                        host= 'localhost',
                        password = "KyleJames1",
                        port = 5432)
        cur = conn.cursor()

        for row in soup.select('table#games tbody tr'):
            if 'thead' in row.get('class', []):
                continue
            
            week_cell = row.find('th', {'data-stat': 'week_num'})
            winner_cell = row.find('td', {'data-stat': 'winner'})
            location_cell = row.find('td', {'data-stat': 'game_location'})
            loser_cell = row.find('td', {'data-stat': 'loser'})
            pts_win_cell = row.find('td', {'data-stat': 'pts_win'})
            pts_lose_cell = row.find('td', {'data-stat': 'pts_lose'})
            
            if week_cell and winner_cell and location_cell and loser_cell and pts_win_cell and pts_lose_cell:
                week = week_cell.text
                winner = winner_cell.text
                location = location_cell.text.strip()  # This can be '@' or empty
                loser = loser_cell.text
                pts_win = pts_win_cell.text
                pts_lose = pts_lose_cell.text  

                home_teamm, away_team, home_points, away_points, margin, total = fixed_data(winner, location, loser, pts_win, pts_lose)

                cur.execute(f"INSERT INTO nfl_schedule(year, week, home_team, away_team, home_points, away_points, margin, total) VALUES({year}, {week}, {home_teamm}, {away_team},{home_points}, {away_points}, {margin}, {total})")
                
            else:
                print(f"Missing data in row: {row}")
        year += 1

    print(games)
    return

def fixed_data(winner, location, loser, pts_win, pts_lose):
    if location == '@':
        home = loser
        away = winner
        pts_home = pts_lose
        pts_away = pts_win
        margin = pts_home - pts_away
        total = pts_home + pts_away
    else:
        home = winner
        away = loser
        pts_home = pts_win
        pts_away = pts_lose
        margin = pts_home - pts_away
        total = pts_home + pts_away

    return home, away, pts_home, pts_away, margin, total
