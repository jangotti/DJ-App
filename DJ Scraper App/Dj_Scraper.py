
# DJ Scraper - First Draft to Pull Real Data (excluding Ticketmaster)
# This is a backend companion to the React Native mobile app

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# --- SCRAPER: Resident Advisor (very basic example for educational use only) ---

def scrape_resident_advisor(city_slug="washington-dc"):
    url = f"https://ra.co/clubs/{city_slug}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch data from RA")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    events = []

    # Simplified parsing (since RA pages are dynamic and often require selenium for full scraping)
    for item in soup.find_all("div", class_="Box-omzyfs-0 event-item"):
        title = item.find("h3").text.strip() if item.find("h3") else ""
        date = item.find("time").text.strip() if item.find("time") else ""
        venue = item.find("div", class_="VenueText-sc-1sqrc1n-0").text.strip() if item.find("div", class_="VenueText-sc-1sqrc1n-0") else ""
        events.append({
            "venue": venue,
            "city": city_slug.replace("-", " ").title(),
            "date": date,
            "dj": title,
            "genre": "",
            "link": "https://ra.co" + item.find("a")["href"]
        })
    return events

# --- SCRAPER: Eventbrite (public API still requires OAuth normally) ---

def scrape_eventbrite():
    # You can use the Eventbrite API here if you create a token
    # For now, we'll simulate this with empty data
    return []

# --- SCRAPER: NTS Radio (highly structured and easier to parse)

def scrape_nts():
    url = "https://www.nts.live/shows"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch data from NTS")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    shows = []
    for show in soup.find_all("a", class_="show-card"):
        title = show.find("div", class_="title").text.strip()
        link = "https://www.nts.live" + show['href']
        shows.append({
            "venue": "NTS Radio",
            "city": "Various",
            "date": "Upcoming",
            "dj": title,
            "genre": "",
            "link": link
        })
    return shows

# --- COMBINE ALL ---
def aggregate_data():
    data = []
    data.extend(scrape_resident_advisor())
    data.extend(scrape_eventbrite())
    data.extend(scrape_nts())
    return data

if __name__ == "__main__":
    data = aggregate_data()
    print(json.dumps(data, indent=2))
