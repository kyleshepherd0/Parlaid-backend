import requests
from bs4 import BeautifulSoup
import psycopg2
from sql.config import load_config  # Ensure this import is correct

def fixed_data(winner, location, loser, pts_win, pts_lose):
    if location == '@':
        home_team = loser
        away_team = winner
        home_points = int(pts_lose)
        away_points = int(pts_win)
    else:
        home_team = winner
        away_team = loser
        home_points = int(pts_win)
        away_points = int(pts_lose)

    margin = home_points - away_points
    total = home_points + away_points
    
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
                    
                    if not all([week_cell, winner_cell, loser_cell, pts_win_cell, pts_lose_cell]):
                        raise ValueError(f"Missing critical data in row: {row}")
                    
                    week = week_cell.text.strip()
                    winner = winner_cell.text.strip()
                    location = location_cell.text.strip() if location_cell else ""
                    loser = loser_cell.text.strip()
                    pts_win = pts_win_cell.text.strip()
                    pts_lose = pts_lose_cell.text.strip()

                    if not all([week, winner, loser, pts_win, pts_lose]):
                        raise ValueError(f"Empty data found in row: {row}")
                    
                    try:
                        home_team, away_team, home_points, away_points, margin, total = fixed_data(winner, location, loser, pts_win, pts_lose)
                    except ValueError as ve:
                        raise ValueError(f"Error converting points to int in row: {row} - {ve}")
                    
                    cur.execute("""
                        INSERT INTO nfl_schedule(year, week, home_team, away_team, home_points, away_points, margin, total)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (year, week, home_team, away_team, home_points, away_points, margin, total))
            year += 1
        print("Data scraping and insertion completed successfully.")
    except Exception as e:
        print(f"An Exception occurred: {e}")
        raise

if __name__ == '__main__':
    # Provide the relative path to the database.ini file
    config = load_config('../sql/database.ini')
    scrape_pfr(config)
