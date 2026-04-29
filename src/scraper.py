from bs4 import BeautifulSoup
import requests, time



prices = []
for page in range(1, 6):
    print(f"=== PAGE {page} ===")
    if(page == 1):
        url = "https://www.nehnutelnosti.sk/vysledky/byty/kosice/prenajom"
    else:
        url = f"https://www.nehnutelnosti.sk/vysledky/byty/kosice/prenajom?page={page}"
    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, "html.parser")
    all_text = soup.find_all("p", attrs={"data-test-id": "text"})

    page_prices = [p.text for p in all_text if len(p.text) > 6 and "€/mes." in p.text[-6:] and 'mui-pc6no8' in p.parent.parent.get("class")]
    prices.extend(page_prices)
    print(len(page_prices))
    time.sleep(1)


print(prices)