from bs4 import BeautifulSoup
from pathlib import Path
import requests, time, pandas as pd

NUM_OF_SCRAPPED_PAGES = 5
BASE_URL = "https://www.nehnutelnosti.sk/vysledky/byty/kosice/prenajom"

ROOT = Path(__file__).parent.parent
OUTPUT_PATH = ROOT / "data" / "processed" / "kosice_housing_prices_data.csv"

# == SCRAPE DATA ==
raw_prices_data = []
raw_location_data = []
raw_rooms_data = []
raw_area_data = []

for page in range(1, NUM_OF_SCRAPPED_PAGES + 1):
    print(f"=== PAGE {page} ===")
    
    url = BASE_URL if page == 1 else f"{BASE_URL}?page={page}"

    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    all_text = soup.find_all("p", attrs={"data-test-id": "text"})

    page_prices_data = []
    page_location_data = []
    page_rooms_data = []
    page_area_data = []

    for p in all_text:
        if len(p.text) > 6 and "€/mes." in p.text[-6:] and 'mui-pc6no8' in p.parent.parent.get("class"):
            page_prices_data.append(p.text)
        if 'mui-5t198y' in p.get("class") and 'mui-1blo5z7' in p.parent.get("class"):
            page_location_data.append(p.text)
        if 'mui-16di0u5' in p.get("class") and 'mui-1blo5z7' in p.parent.get("class"):
            page_rooms_data.append(p.text)

    # search data for area if it's there
    cards = soup.find_all("div", class_="mui-10x79uu")
    for card in cards:
        area_el = card.find("div", class_="mui-45ozih")
        if area_el:
            page_area_data.append(area_el.find("p").text)
        else:
            page_area_data.append(None)

    raw_prices_data.extend(page_prices_data)
    raw_location_data.extend(page_location_data)
    raw_rooms_data.extend(page_rooms_data)
    raw_area_data.extend(page_area_data[::2])

    print(f"Price data pieces scrapped: {len(page_prices_data)}")
    print(f"Location data pieces scrapped: {len(page_location_data)}")
    print(f"Room data pieces scrapped: {len(page_rooms_data)}")
    print(f"Area data pieces scrapped: {len(page_area_data[::2])}")

    time.sleep(1)

if not (len(raw_prices_data) == len(raw_location_data) == len(raw_rooms_data) == len(raw_area_data)):
    raise ValueError(f"Mismatch: some data is missing.")

# print(raw_prices_data)
# print(raw_location_data)
# print(raw_rooms_data)
# print(raw_area_data)

# == CLEAN DATA ==

## CLEAN PRICES
clean_prices_data = []
for price in raw_prices_data:
    try:
        clean_price = int(price.replace("\xa0", "").strip(" €/mes."))
        clean_prices_data.append(clean_price)
    except ValueError:
        print(f"Could not parse: {price}")
# print(clean_prices_data)

## CLEAN LOCATION
clean_district_data = []
clean_county_data = []

for location in raw_location_data:
    clean_location = location.split(', ')
    if(len(clean_location) == 2):
        clean_district_data.append(clean_location[0].replace("Košice-", ""))
        clean_county_data.append(clean_location[1])
    else:
        clean_district_data.append(clean_location[1].replace("Košice-", ""))
        clean_county_data.append(clean_location[2])
# print(clean_district_data)
# print(clean_county_data)

## CLEAN ROOMS
clean_rooms_data = []
for rooms in raw_rooms_data:
    if rooms == "Garsónka" or rooms == "Mezonet" or rooms == "Apartmán":
        clean_rooms_data.append(rooms)
    else:
        clean_rooms_data.append(int(rooms[0]))
#print(clean_rooms_data)

## CLEAN AREA
clean_area_data = [
    float(area.replace(" m²", "")) if area is not None else None
    for area in raw_area_data
]

## == EXPORT DATA ==
data = {
    "price": clean_prices_data,
    "district": clean_district_data,
    "county": clean_county_data,
    "rooms": clean_rooms_data,
    "area": clean_area_data
}

df = pd.DataFrame(data=data)
print(df.head(50))
df.to_csv(OUTPUT_PATH, index=False)