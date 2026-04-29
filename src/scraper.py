from bs4 import BeautifulSoup
import requests, time



prices = []
location_data = []

for page in range(1, 6):
    print(f"=== PAGE {page} ===")
    if(page == 1):
        url = "https://www.nehnutelnosti.sk/vysledky/byty/kosice/prenajom"
    else:
        url = f"https://www.nehnutelnosti.sk/vysledky/byty/kosice/prenajom?page={page}"
    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    all_text = soup.find_all("p", attrs={"data-test-id": "text"})

    # page_prices = [p.text for p in all_text if len(p.text) > 6 and "€/mes." in p.text[-6:] and 'mui-pc6no8' in p.parent.parent.get("class")]
    page_prices = []
    page_location_data = []
    for p in all_text:
        if len(p.text) > 6 and "€/mes." in p.text[-6:] and 'mui-pc6no8' in p.parent.parent.get("class"):
            page_prices.append(p.text)
        if 'mui-5t198y' in p.get("class") and 'mui-1blo5z7' in p.parent.get("class"):
            page_location_data.append(p.text)
    prices.extend(page_prices)
    location_data.extend(page_location_data)
    print(len(page_prices))
    print(len(page_location_data))
    time.sleep(1)

if(len(prices) != len(location_data)):
    raise ValueError(f"Mismatch: {len(prices)} prices vs {len(location_data)} location data pieces")

print(prices)
print(location_data)