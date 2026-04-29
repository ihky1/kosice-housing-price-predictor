from bs4 import BeautifulSoup
import requests, time

NUM_OF_SCRAPPED_PAGES = 5
BASE_URL = "https://www.nehnutelnosti.sk/vysledky/byty/kosice/prenajom"

prices_data = []
location_data = []
rooms_data = []

for page in range(1, NUM_OF_SCRAPPED_PAGES + 1):
    print(f"=== PAGE {page} ===")
    
    url = BASE_URL if page == 1 else f"{BASE_URL}?page={page}"

    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    all_text = soup.find_all("p", attrs={"data-test-id": "text"})

    page_prices_data = []
    page_location_data = []
    page_rooms_data = []

    for p in all_text:
        if len(p.text) > 6 and "€/mes." in p.text[-6:] and 'mui-pc6no8' in p.parent.parent.get("class"):
            page_prices_data.append(p.text)
        if 'mui-5t198y' in p.get("class") and 'mui-1blo5z7' in p.parent.get("class"):
            page_location_data.append(p.text)
        if 'mui-16di0u5' in p.get("class") and 'mui-1blo5z7' in p.parent.get("class"):
            page_rooms_data.append(p.text)

    prices_data.extend(page_prices_data)
    location_data.extend(page_location_data)
    rooms_data.extend(page_rooms_data)

    print(f"Price data pieces scrapped: {len(page_prices_data)}")
    print(f"Location data pieces scrapped: {len(page_location_data)}")
    print(f"Room data pieces scrapped: {len(page_rooms_data)}")

    time.sleep(1)

if not (len(prices_data) == len(location_data) == len(rooms_data)):
    raise ValueError(f"Mismatch: {len(prices_data)} prices vs {len(location_data)} location data pieces")

#print(prices_data)
#print(location_data)
print(rooms_data)