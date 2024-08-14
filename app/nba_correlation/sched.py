import time
import requests
from bs4 import BeautifulSoup
import psycopg2
from sql.config import load_config
from datetime import datetime

def parse_date(date_str):
    """Convert date string to YYYY-MM-DD format."""
    try:
        return datetime.strptime(date_str, "%a, %b %d, %Y").strftime("%Y-%m-%d")
    except ValueError as ve:
        raise ValueError(f"Error parsing date: {date_str} - {ve}")

def scrape_basketball_reference(config):
    try:
        with psycopg2.connect(**config) as conn:
            cur = conn.cursor()
            for year in range(2022, 2026):  # Scrape from 2022 to 2025 seasons
                cur.execute("DELETE FROM nba_schedule")
                conn.commit()

                URL = f"https://www.basketball-reference.com/leagues/NBA_{year}_games.html"
                print(f"Fetching URL: {URL}")

                retry_attempts = 3
                for attempt in range(retry_attempts):
                    try:
                        response = requests.get(URL, timeout=10)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.content, 'html.parser')
                        break  # Exit retry loop on success
                    except requests.exceptions.RequestException as e:
                        print(f"Request failed (attempt {attempt+1}/{retry_attempts}): {e}")
                        time.sleep(10)  # Wait before retrying
                else:
                    print(f"Failed to fetch {URL} after {retry_attempts} attempts.")
                    continue

                for month_table in soup.select('table#schedule tbody'):
                    for row in month_table.find_all('tr'):
                        if row.find('th', {'scope': 'col'}):
                            continue

                        try:
                            date_cell = row.find('th', {'data-stat': 'date_game'})
                            visitor_team_cell = row.find('td', {'data-stat': 'visitor_team_name'})
                            home_team_cell = row.find('td', {'data-stat': 'home_team_name'})
                            visitor_pts_cell = row.find('td', {'data-stat': 'visitor_pts'})
                            home_pts_cell = row.find('td', {'data-stat': 'home_pts'})

                            if not all([date_cell, visitor_team_cell, home_team_cell, visitor_pts_cell, home_pts_cell]):
                                print(f"Missing critical data in row: {row}")
                                continue

                            date = parse_date(date_cell.text.strip())
                            visitor_team = visitor_team_cell.text.strip()
                            home_team = home_team_cell.text.strip()
                            visitor_pts = int(visitor_pts_cell.text.strip())
                            home_pts = int(home_pts_cell.text.strip())

                            margin = home_pts - visitor_pts
                            total = home_pts + visitor_pts

                            cur.execute("""
                                INSERT INTO nba_schedule(year, date, home_team, away_team, home_points, away_points, margin, total)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """, (year, date, home_team, visitor_team, home_pts, visitor_pts, margin, total))

                        except Exception as e:
                            print(f"Error processing row: {row}, Error: {e}")
                            continue

                conn.commit()

                # Delay between requests
                time.sleep(10)  # Adjust this delay as needed

            print("NBA data scraping and insertion completed successfully.")
    except Exception as e:
        print(f"An exception occurred: {e}")
        raise

if __name__ == '__main__':
    config = load_config()
    scrape_basketball_reference(config)