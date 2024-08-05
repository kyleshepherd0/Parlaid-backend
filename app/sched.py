import requests
from bs4 import BeautifulSoup
import psycopg2
from sql.config import load_config


def fixed_data(winner, location, loser, pts_win, pts_lose):
    if location == '@':
        home_team = loser
        away_team = winner
        home_points = pts_lose
        away_points = pts_win
    else:
        home_team = winner
        away_team = loser
        home_points = pts_win
        away_points = pts_lose

    margin = int(home_points) - int(away_points)
    total = int(home_points) + int(away_points)
    
    return home_team, away_team, home_points, away_points, margin, total

def scrape_pfr(config):
    try:
        year = 2020
        while year < 2024:
            URL = f"https://www.pro-football-reference.com/years/{year}/games.htm"
            response = requests.get(URL)
            soup = BeautifulSoup(response.content, 'html.parser')

            with psycopg2.connect(**config) as conn:
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
                        location = location_cell.text.strip()
                        loser = loser_cell.text
                        pts_win = pts_win_cell.text
                        pts_lose = pts_lose_cell.text  

                        home_team, away_team, home_points, away_points, margin, total = fixed_data(winner, location, loser, pts_win, pts_lose)

                        cur.execute("""
                            INSERT INTO nfl_schedule(year, week, home_team, away_team, home_points, away_points, margin, total)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (year, week, home_team, away_team, home_points, away_points, margin, total))
                    else:
                        print(f"Missing data in row: {row}")
            year += 1
        print("Data scraping and insertion completed successfully.")
    except Exception as e:
        print(f"An Exception occurred: {e}")

if __name__ == '__main__':
    config = load_config()
    scrape_pfr(config)